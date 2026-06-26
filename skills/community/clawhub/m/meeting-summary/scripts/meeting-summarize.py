#!/usr/bin/env python3
"""
Meeting Summarizer - orchestration-first meeting processing pipeline.

Preferred path:
- Step file transcription for text
- pyannote community-1 for speaker turns when available
- known voiceprints for real-name mapping
- placeholder speakers for unresolved diarization identities

Fallback path:
- local energy-vad segmentation + lightweight clustering
"""

import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import wave
from typing import Dict, List, Optional, Tuple

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
WORKSPACE = os.environ.get("MEETING_SUMMARY_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
CACHE_DIR = os.path.join(WORKSPACE, "cache", "meeting-summary")
ASR_SCRIPT = os.path.join(SCRIPT_DIR, "transcribe.py")
VOICEPRINT_SCRIPT = os.path.join(SCRIPT_DIR, "voiceprint-manager.py")
PYANNOTE_SCRIPT = os.path.join(SCRIPT_DIR, "pyannote-diarize.py")
PYANNOTE_PYTHON = os.environ.get(
    "MEETING_SUMMARY_PYANNOTE_PYTHON",
    os.path.expanduser("~/.venv-pyannote/bin/python"),
)

DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1
MATCH_THRESHOLD = 0.50
STRONG_MATCH_THRESHOLD = 0.58
MATCH_MARGIN = 0.08
UNKNOWN_CLUSTER_THRESHOLD = 0.72
LOW_CONFIDENCE_THRESHOLD = 0.55
PROFILE_MERGE_THRESHOLD = 0.84
CHUNK_DURATION_MS = 5 * 60 * 1000
CHUNK_OVERLAP_MS = 15 * 1000
MIN_CHUNK_SPEECH_MS = 12 * 1000
MONOLOGUE_MAX_REGIONS = 3
MONOLOGUE_DOMINANCE_THRESHOLD = 0.78
STEP_CHAT_COMPLETIONS_URL = os.environ.get("MEETING_SUMMARY_LLM_URL", "https://api.stepfun.com/v1/chat/completions")
STEP_LLM_MODEL = os.environ.get("MEETING_SUMMARY_LLM_MODEL", "step-3.5-flash")


def run_command(cmd: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def preprocess_audio(audio_path: str) -> Tuple[str, Dict[str, object]]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
        normalized_path = handle.name

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        audio_path,
        "-ac",
        str(DEFAULT_CHANNELS),
        "-ar",
        str(DEFAULT_SAMPLE_RATE),
        normalized_path,
    ]
    result = run_command(cmd, timeout=300)
    if result.returncode != 0:
        safe_unlink(normalized_path)
        raise RuntimeError(f"Audio preprocessing failed: {result.stderr.strip()}")

    metadata = {
        "stage": "preprocess",
        "backend": "ffmpeg-normalize",
        "sample_rate": DEFAULT_SAMPLE_RATE,
        "channels": DEFAULT_CHANNELS,
    }
    return normalized_path, metadata


def run_step_transcription(audio_path: str, language: str = "zh", transport: str = "transcriptions") -> Dict[str, object]:
    cmd = [
        sys.executable,
        ASR_SCRIPT,
        audio_path,
        "--transport",
        transport,
        "--language",
        language,
        "--json",
        "--no-stream",
    ]
    result = run_command(cmd, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Step ASR {transport} failed")

    output = result.stdout.strip()
    if not output:
        raise RuntimeError(f"Step ASR {transport} returned empty output")

    try:
        data = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse Step ASR JSON: {exc}") from exc

    data.setdefault("usage", {})
    data.setdefault("segments", [])
    data.setdefault("transport", transport)
    return data


def run_pyannote_diarization(audio_path: str, num_speakers: Optional[int] = None) -> Dict[str, object]:
    if not os.path.exists(PYANNOTE_PYTHON):
        raise RuntimeError(f"Pyannote python not found: {PYANNOTE_PYTHON}")
    if not os.path.exists(PYANNOTE_SCRIPT):
        raise RuntimeError(f"Pyannote script not found: {PYANNOTE_SCRIPT}")

    cmd = [
        PYANNOTE_PYTHON,
        PYANNOTE_SCRIPT,
        "--audio",
        audio_path,
    ]
    if num_speakers:
        cmd.extend(["--num-speakers", str(num_speakers)])
    result = run_command(cmd, timeout=1800)
    if result.returncode != 0:
        raise RuntimeError(result.stdout.strip() or result.stderr.strip() or "pyannote diarization failed")
    try:
        data = json.loads(result.stdout.strip())
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse pyannote JSON: {exc}") from exc
    if data.get("error"):
        raise RuntimeError(data["error"])
    return data


def write_wav(path: str, audio: np.ndarray, sr: int) -> None:
    clipped = np.clip(audio, -1.0, 1.0)
    pcm = (clipped * 32767.0).astype(np.int16)
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sr)
        handle.writeframes(pcm.tobytes())


def analyze_chunk(audio: np.ndarray, sr: int, start_ms: int, end_ms: int) -> Dict[str, object]:
    start = max(0, int(start_ms / 1000 * sr))
    end = min(len(audio), max(start + 1, int(end_ms / 1000 * sr)))
    chunk = audio[start:end]
    duration_ms = max(1, end_ms - start_ms)
    if chunk.size == 0:
        return {
            "speech_ms": 0,
            "speech_ratio": 0.0,
            "region_count": 0,
            "largest_region_ratio": 0.0,
            "should_skip": True,
            "mode": "skip",
        }

    frame_ms = 300
    frame_len = max(1, int(sr * frame_ms / 1000))
    threshold = 0.01
    regions: List[Tuple[int, int]] = []
    region_start = None
    for idx in range(0, len(chunk), frame_len):
        frame = chunk[idx: idx + frame_len]
        if frame.size == 0:
            continue
        rms = float(np.sqrt(np.mean(np.square(frame))))
        if rms >= threshold:
            if region_start is None:
                region_start = idx
        elif region_start is not None:
            region_end = idx
            if region_end > region_start:
                regions.append((region_start, region_end))
            region_start = None
    if region_start is not None:
        regions.append((region_start, len(chunk)))

    speech_ms = sum(samples_to_ms(end_idx - start_idx, sr) for start_idx, end_idx in regions)
    speech_ratio = speech_ms / duration_ms if duration_ms else 0.0
    largest_region_ms = max((samples_to_ms(end_idx - start_idx, sr) for start_idx, end_idx in regions), default=0)
    largest_region_ratio = largest_region_ms / speech_ms if speech_ms else 0.0

    should_skip = speech_ms < MIN_CHUNK_SPEECH_MS or speech_ratio < 0.12
    is_monologue = (
        not should_skip
        and len(regions) <= MONOLOGUE_MAX_REGIONS
        and largest_region_ratio >= MONOLOGUE_DOMINANCE_THRESHOLD
    )
    mode = "skip" if should_skip else ("mono" if is_monologue else "multi")
    return {
        "speech_ms": speech_ms,
        "speech_ratio": round(speech_ratio, 4),
        "region_count": len(regions),
        "largest_region_ratio": round(largest_region_ratio, 4),
        "should_skip": should_skip,
        "mode": mode,
    }


def build_chunk_plan(audio: np.ndarray, sr: int, duration_ms: int) -> List[Dict[str, object]]:
    chunks = []
    start_ms = 0
    idx = 0
    step_ms = max(1, CHUNK_DURATION_MS - CHUNK_OVERLAP_MS)
    while start_ms < duration_ms:
        end_ms = min(duration_ms, start_ms + CHUNK_DURATION_MS)
        analysis = analyze_chunk(audio, sr, start_ms, end_ms)
        chunks.append(
            {
                "chunk_index": idx,
                "start_time": start_ms,
                "end_time": end_ms,
                **analysis,
            }
        )
        if end_ms >= duration_ms:
            break
        start_ms += step_ms
        idx += 1
    return chunks


def chunk_priority_score(chunk: Dict[str, object]) -> float:
    mode = str(chunk.get("mode", "skip"))
    if mode == "skip":
        return -1.0
    speech_ratio = float(chunk.get("speech_ratio", 0.0) or 0.0)
    region_count = int(chunk.get("region_count", 0) or 0)
    largest_region_ratio = float(chunk.get("largest_region_ratio", 0.0) or 0.0)
    multi_bonus = 2.0 if mode == "multi" else 0.5
    interaction_score = min(region_count, 12) / 12.0
    anti_monologue = 1.0 - largest_region_ratio
    return round(multi_bonus + (speech_ratio * 1.5) + interaction_score + anti_monologue, 4)


def prioritize_chunks(chunk_plan: List[Dict[str, object]]) -> List[Dict[str, object]]:
    for chunk in chunk_plan:
        chunk["priority_score"] = chunk_priority_score(chunk)
    active_chunks = [chunk for chunk in chunk_plan if str(chunk.get("mode")) != "skip"]
    return sorted(
        active_chunks,
        key=lambda chunk: (
            -float(chunk.get("priority_score", -1.0)),
            int(chunk.get("chunk_index", 0)),
        ),
    )


def merge_overlapping_pyannote_segments(segments: List[Dict[str, object]]) -> List[Dict[str, object]]:
    ordered = sorted(segments, key=lambda item: (item["start_time"], item["end_time"], item.get("speaker_hint", "")))
    merged: List[Dict[str, object]] = []
    for seg in ordered:
        if merged:
            prev = merged[-1]
            same_hint = prev.get("speaker_hint") == seg.get("speaker_hint")
            overlap = seg["start_time"] <= prev["end_time"]
            if same_hint and overlap:
                prev["end_time"] = max(prev["end_time"], seg["end_time"])
                continue
            duplicate_overlap = overlap and abs(seg["start_time"] - prev["start_time"]) <= 1000 and abs(seg["end_time"] - prev["end_time"]) <= 1000
            if duplicate_overlap:
                continue
        merged.append(dict(seg))
    return merged


def selective_chunked_diarization(
    audio_path: str,
    num_speakers: Optional[int],
    audio: np.ndarray,
    sr: int,
    max_new_chunks: Optional[int] = None,
) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    duration_ms = samples_to_ms(len(audio), sr)
    chunk_plan = build_chunk_plan(audio, sr, duration_ms)
    prioritized_chunks = prioritize_chunks(chunk_plan)
    segments: List[Dict[str, object]] = []
    executed_new_chunks = 0

    for chunk in prioritized_chunks:
        mode = str(chunk["mode"])
        if mode == "skip":
            continue

        chunk_audio = slice_audio(audio, sr, int(chunk["start_time"]), int(chunk["end_time"]))
        chunk_cache = cache_file_path(
            audio_path,
            "chunk-diarization",
            [str(num_speakers or 0), str(chunk["chunk_index"]), str(chunk["start_time"]), str(chunk["end_time"]), mode],
        )
        cached = load_json_cache(chunk_cache)
        if cached is None:
            if max_new_chunks is not None and executed_new_chunks >= max_new_chunks:
                segments.append(
                    {
                        "start_time": int(chunk["start_time"]),
                        "end_time": int(chunk["end_time"]),
                        "speaker_hint": f"UNRESOLVED_CHUNK_{int(chunk['chunk_index']):02d}",
                        "source": "chunk-unresolved",
                    }
                )
                continue
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
                chunk_wav = handle.name
            try:
                write_wav(chunk_wav, chunk_audio, sr)
                if mode == "mono":
                    chunk_result = {
                        "segments": [
                            {
                                "start_time": int(chunk["start_time"]),
                                "end_time": int(chunk["end_time"]),
                                "speaker_hint": f"CHUNK_MONO_{int(chunk['chunk_index']):02d}",
                                "source": "chunk-mono",
                            }
                        ]
                    }
                else:
                    pyannote_result = run_pyannote_diarization(chunk_wav, num_speakers=min(max(2, num_speakers or 2), 6))
                    chunk_segments = []
                    for item in pyannote_result.get("segments", []):
                        chunk_segments.append(
                            {
                                "start_time": int(chunk["start_time"]) + int(item.get("start_time", 0) or 0),
                                "end_time": int(chunk["start_time"]) + int(item.get("end_time", 0) or 0),
                                "speaker_hint": f"CHUNK_{int(chunk['chunk_index']):02d}_{item.get('speaker_hint', 'UNKNOWN')}",
                                "source": "pyannote-chunked",
                            }
                        )
                    chunk_result = {"segments": chunk_segments}
                save_json_cache(chunk_cache, chunk_result)
                cached = chunk_result
                executed_new_chunks += 1
            finally:
                safe_unlink(chunk_wav)

        segments.extend(cached.get("segments", []))

    return merge_overlapping_pyannote_segments(segments), {
        "chunk_plan": chunk_plan,
        "priority_order": [
            {
                "chunk_index": int(chunk["chunk_index"]),
                "start_time": int(chunk["start_time"]),
                "end_time": int(chunk["end_time"]),
                "mode": chunk["mode"],
                "priority_score": float(chunk.get("priority_score", 0.0)),
            }
            for chunk in prioritized_chunks
        ],
        "mode": "chunked-selective",
        "max_new_chunks": max_new_chunks,
        "executed_new_chunks": executed_new_chunks,
    }


class EnergySegmenter:
    name = "energy-vad"

    def __init__(
        self,
        frame_ms: int = 400,
        min_silence_ms: int = 600,
        min_segment_ms: int = 800,
        energy_threshold: float = 0.012,
    ):
        self.frame_ms = frame_ms
        self.min_silence_ms = min_silence_ms
        self.min_segment_ms = min_segment_ms
        self.energy_threshold = energy_threshold

    def segment(self, audio_path: str) -> List[Dict[str, int]]:
        audio, sr = load_wav(audio_path)
        frame_len = max(1, int(sr * self.frame_ms / 1000))
        silence_frames_needed = max(1, int(self.min_silence_ms / self.frame_ms))

        segments = []
        in_speech = False
        start_idx = 0
        silence_run = 0

        for idx in range(0, len(audio), frame_len):
            frame = audio[idx: idx + frame_len]
            if frame.size == 0:
                continue
            rms = float(np.sqrt(np.mean(np.square(frame))))
            is_speech = rms >= self.energy_threshold

            if is_speech:
                if not in_speech:
                    in_speech = True
                    start_idx = idx
                silence_run = 0
                continue

            if in_speech:
                silence_run += 1
                if silence_run >= silence_frames_needed:
                    end_idx = max(start_idx + 1, idx - (silence_run - 1) * frame_len)
                    if ms_between(start_idx, end_idx, sr) >= self.min_segment_ms:
                        segments.append(
                            {
                                "start_time": samples_to_ms(start_idx, sr),
                                "end_time": samples_to_ms(end_idx, sr),
                                "source": "energy-vad",
                            }
                        )
                    in_speech = False
                    silence_run = 0

        if in_speech:
            end_idx = len(audio)
            if ms_between(start_idx, end_idx, sr) >= self.min_segment_ms:
                segments.append(
                    {
                        "start_time": samples_to_ms(start_idx, sr),
                        "end_time": samples_to_ms(end_idx, sr),
                        "source": "energy-vad",
                    }
                )

        if not segments:
            duration_ms = samples_to_ms(len(audio), sr)
            segments = [{"start_time": 0, "end_time": duration_ms, "source": "energy-vad"}]

        return merge_adjacent_segments(segments, gap_ms=450, min_duration_ms=self.min_segment_ms)


class StepTranscriber:
    name = "step-asr"

    def transcribe(self, audio_path: str, language: str) -> Dict[str, object]:
        errors = []
        for transport in ("transcriptions", "sse"):
            try:
                result = run_step_transcription(audio_path, language=language, transport=transport)
                result["backend"] = f"step-{transport}"
                return result
            except RuntimeError as exc:
                errors.append(f"{transport}: {exc}")
        raise RuntimeError(" ; ".join(errors))


class PyannoteSegmenter:
    name = "pyannote-community-1"

    def __init__(self, num_speakers: Optional[int] = None):
        self.num_speakers = num_speakers

    def segment(self, audio_path: str) -> List[Dict[str, object]]:
        result = run_pyannote_diarization(audio_path, num_speakers=self.num_speakers)
        segments = result.get("segments", [])
        if not segments:
            raise RuntimeError("pyannote returned no segments")
        return segments


class SpeakerResolver:
    name = "voiceprint-cluster"

    def __init__(self):
        self._voiceprint_module = None

    @property
    def voiceprint(self):
        if self._voiceprint_module is None:
            import importlib.util

            spec = importlib.util.spec_from_file_location("voiceprint_manager", VOICEPRINT_SCRIPT)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            self._voiceprint_module = module
        return self._voiceprint_module

    def resolve(
        self,
        audio_path: str,
        segments: List[Dict[str, object]],
        speaker_map: Optional[Dict[str, str]] = None,
    ) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[str], List[Dict[str, str]], List[Dict[str, object]]]:
        audio, sr = load_wav(audio_path)
        module = self.voiceprint
        known_voiceprints = module.load_all_voiceprints()
        speaker_map = normalize_speaker_map(speaker_map or {})

        speaker_registry: Dict[str, Dict[str, object]] = {}
        confidence_flags: List[str] = []
        open_questions: List[Dict[str, str]] = []

        hint_groups: Dict[str, List[Dict[str, object]]] = collections.OrderedDict()
        fallback_segments: List[Dict[str, object]] = []
        for seg in segments:
            speaker_hint = str(seg.get("speaker_hint", "") or "").strip()
            if speaker_hint:
                hint_groups.setdefault(speaker_hint, []).append(seg)
            else:
                fallback_segments.append(seg)

        hint_profiles: List[Dict[str, object]] = []
        placeholder_names: List[str] = []
        for speaker_hint, grouped_segments in hint_groups.items():
            profile = build_hint_profile(
                speaker_hint=speaker_hint,
                grouped_segments=grouped_segments,
                audio=audio,
                sr=sr,
                voiceprint_module=module,
                known_voiceprints=known_voiceprints,
                speaker_map=speaker_map,
                placeholder_names=placeholder_names,
                confidence_flags=confidence_flags,
            )
            hint_profiles.append(profile)
        hint_profiles = merge_hint_profiles(hint_profiles, placeholder_names)

        cluster_centers: List[np.ndarray] = []
        cluster_names = list(placeholder_names)
        for seg in fallback_segments:
            start_ms = int(seg.get("start_time", 0) or 0)
            end_ms = int(seg.get("end_time", 0) or 0)
            seg_audio = slice_audio(audio, sr, start_ms, end_ms)
            speaker_name = "Speaker_A"
            source = seg.get("source", "fallback")
            confidence = 0.0
            top_matches: List[Dict[str, float]] = []
            embedding = None

            if seg_audio.size >= int(sr * 0.5):
                embedding = module.extract_embedding_from_segment(seg_audio, sr)

            if embedding is not None and known_voiceprints:
                top_matches, best_name, best_score, margin = rank_known_voiceprints(module, embedding, known_voiceprints)
                if best_score >= STRONG_MATCH_THRESHOLD or (
                    best_score >= MATCH_THRESHOLD and margin >= MATCH_MARGIN
                ):
                    speaker_name = best_name
                    source = "voiceprint"
                    confidence = best_score
                else:
                    speaker_name, confidence = assign_unknown_cluster(embedding, cluster_centers, cluster_names)
                    source = "cluster"
            elif embedding is not None:
                speaker_name, confidence = assign_unknown_cluster(embedding, cluster_centers, cluster_names)
                source = "cluster"
            else:
                speaker_name = allocate_cluster_name(cluster_names)
                cluster_names.append(speaker_name)
                cluster_centers.append(np.zeros(1, dtype=np.float32))
                source = "insufficient-audio"
                confidence_flags.append(
                    f"Segment {start_ms}-{end_ms}ms too short for reliable speaker resolution"
                )

            if speaker_name in speaker_map:
                speaker_name = speaker_map[speaker_name]
                source = "manual-map"
                confidence = max(confidence, 0.99)

            seg["speaker"] = speaker_name
            seg["speaker_source"] = source
            seg["speaker_confidence"] = round(float(confidence), 4)
            seg["speaker_candidates"] = top_matches

        for profile in hint_profiles:
            for seg in profile["segments"]:
                seg["speaker"] = profile["speaker"]
                seg["speaker_source"] = profile["source"]
                seg["speaker_confidence"] = round(float(profile["confidence"]), 4)
                seg["speaker_candidates"] = list(profile["top_matches"])

        review_items: List[Dict[str, object]] = []
        for profile in hint_profiles:
            review_items.append(
                {
                    "speaker_hint": profile["speaker_hint"],
                    "resolved_speaker": profile["speaker"],
                    "source": profile["source"],
                    "confidence": round(float(profile["confidence"]), 4),
                    "suggested_speaker": profile.get("suggested_speaker", ""),
                    "suggested_confidence": profile.get("suggested_confidence", 0.0),
                    "segment_count": len(profile["segments"]),
                    "top_candidates": profile["top_matches"],
                    "sample_quotes": collect_sample_quotes(profile["segments"]),
                }
            )

        for seg in segments:
            start_ms = int(seg.get("start_time", 0) or 0)
            end_ms = int(seg.get("end_time", 0) or 0)
            speaker_name = str(seg.get("speaker", "Speaker_A"))
            source = str(seg.get("speaker_source", "fallback"))
            confidence = float(seg.get("speaker_confidence", 0.0) or 0.0)
            registry_entry = speaker_registry.setdefault(
                speaker_name,
                {
                    "speaker": speaker_name,
                    "display_name": speaker_name,
                    "is_known": source == "voiceprint",
                    "source": source,
                    "segment_count": 0,
                    "confidence_scores": [],
                },
            )
            registry_entry["segment_count"] += 1
            registry_entry["confidence_scores"].append(float(confidence))
            registry_entry["is_known"] = registry_entry["is_known"] or source in {"voiceprint", "manual-map"}
            if source in {"voiceprint", "manual-map"}:
                registry_entry["display_name"] = speaker_name
                registry_entry["source"] = source

            if source not in {"voiceprint", "manual-map"} and speaker_name not in {item.get("speaker") for item in open_questions}:
                open_questions.append({"speaker": speaker_name, "question": f"Confirm the real identity of {speaker_name}"})

            if confidence < LOW_CONFIDENCE_THRESHOLD:
                confidence_flags.append(
                    f"Low speaker confidence for {speaker_name} at {start_ms}-{end_ms}ms ({confidence:.2f})"
                )

        speakers = []
        for _, info in sorted(speaker_registry.items()):
            scores = info.pop("confidence_scores")
            avg_conf = sum(scores) / len(scores) if scores else 0.0
            speakers.append({**info, "average_confidence": round(avg_conf, 4)})

        return segments, speakers, dedupe_strings(confidence_flags), open_questions, review_items


def build_hint_profile(
    speaker_hint: str,
    grouped_segments: List[Dict[str, object]],
    audio: np.ndarray,
    sr: int,
    voiceprint_module,
    known_voiceprints: Dict[str, np.ndarray],
    speaker_map: Dict[str, str],
    placeholder_names: List[str],
    confidence_flags: List[str],
) -> Dict[str, object]:
    embeddings: List[np.ndarray] = []
    for seg in grouped_segments:
        start_ms = int(seg.get("start_time", 0) or 0)
        end_ms = int(seg.get("end_time", 0) or 0)
        seg_audio = slice_audio(audio, sr, start_ms, end_ms)
        if seg_audio.size < int(sr * 0.5):
            continue
        embedding = voiceprint_module.extract_embedding_from_segment(seg_audio, sr)
        if embedding is not None:
            embeddings.append(embedding)

    aggregated_embedding = average_embeddings(embeddings)
    top_matches: List[Dict[str, float]] = []
    confidence = 0.7
    source = "pyannote-cluster"
    resolved_name = allocate_cluster_name(placeholder_names)
    placeholder_names.append(resolved_name)
    suggested_speaker = ""
    suggested_confidence = 0.0

    if speaker_hint in speaker_map:
        resolved_name = speaker_map[speaker_hint]
        source = "manual-map"
        confidence = 0.99
    elif aggregated_embedding is not None and known_voiceprints:
        top_matches, best_name, best_score, margin = rank_known_voiceprints(
            voiceprint_module,
            aggregated_embedding,
            known_voiceprints,
        )
        suggested_speaker = best_name
        suggested_confidence = best_score
        if best_score >= STRONG_MATCH_THRESHOLD or (
            best_score >= MATCH_THRESHOLD and margin >= MATCH_MARGIN
        ):
            resolved_name = best_name
            source = "voiceprint"
            confidence = best_score
        else:
            confidence = max(best_score, 0.7)
    else:
        if aggregated_embedding is None:
            confidence_flags.append(
                f"Speaker hint {speaker_hint} had insufficient audio for reliable voiceprint resolution"
            )

    if resolved_name in speaker_map:
        resolved_name = speaker_map[resolved_name]
        source = "manual-map"
        confidence = 0.99

    return {
        "speaker_hint": speaker_hint,
        "speaker": resolved_name,
        "source": source,
        "confidence": confidence,
        "top_matches": top_matches,
        "suggested_speaker": suggested_speaker,
        "suggested_confidence": round(float(suggested_confidence), 4),
        "embedding": aggregated_embedding,
        "segments": grouped_segments,
    }


def merge_hint_profiles(hint_profiles: List[Dict[str, object]], placeholder_names: List[str]) -> List[Dict[str, object]]:
    merged: List[Dict[str, object]] = []
    for profile in hint_profiles:
        if profile["source"] in {"manual-map", "voiceprint"}:
            merged.append(profile)
            continue

        matched = None
        for existing in merged:
            if existing["source"] in {"manual-map", "voiceprint"}:
                continue
            same_suggested = (
                profile.get("suggested_speaker")
                and profile.get("suggested_speaker") == existing.get("suggested_speaker")
                and min(float(profile.get("suggested_confidence", 0.0)), float(existing.get("suggested_confidence", 0.0))) >= MATCH_THRESHOLD
            )
            similarity = profile_similarity(profile.get("embedding"), existing.get("embedding"))
            if same_suggested or similarity >= PROFILE_MERGE_THRESHOLD:
                matched = existing
                break

        if matched is None:
            merged.append(profile)
            continue

        matched["segments"].extend(profile["segments"])
        matched["speaker_hint"] = f"{matched['speaker_hint']}+{profile['speaker_hint']}"
        matched["top_matches"] = merge_top_matches(matched.get("top_matches", []), profile.get("top_matches", []))
        matched["suggested_speaker"] = matched.get("suggested_speaker") or profile.get("suggested_speaker", "")
        matched["suggested_confidence"] = max(
            float(matched.get("suggested_confidence", 0.0)),
            float(profile.get("suggested_confidence", 0.0)),
        )
        matched["confidence"] = max(float(matched.get("confidence", 0.0)), float(profile.get("confidence", 0.0)))
        matched["embedding"] = average_embeddings([emb for emb in [matched.get("embedding"), profile.get("embedding")] if emb is not None])
        profile["speaker"] = matched["speaker"]

    return merged


def profile_similarity(left: Optional[np.ndarray], right: Optional[np.ndarray]) -> float:
    if left is None or right is None:
        return -1.0
    denom = (np.linalg.norm(left) * np.linalg.norm(right)) + 1e-10
    return float(np.dot(left, right) / denom)


def merge_top_matches(left: List[Dict[str, float]], right: List[Dict[str, float]]) -> List[Dict[str, float]]:
    merged: Dict[str, float] = {}
    for item in left + right:
        name = str(item.get("speaker", "")).strip()
        score = float(item.get("score", 0.0) or 0.0)
        if not name:
            continue
        merged[name] = max(merged.get(name, -1.0), score)
    return [
        {"speaker": name, "score": round(score, 4)}
        for name, score in sorted(merged.items(), key=lambda pair: pair[1], reverse=True)[:3]
    ]


def rank_known_voiceprints(voiceprint_module, embedding: np.ndarray, known_voiceprints: Dict[str, np.ndarray]) -> Tuple[List[Dict[str, float]], str, float, float]:
    ranked = []
    for name, stored_emb in known_voiceprints.items():
        score = float(voiceprint_module.compute_similarity(embedding, stored_emb))
        ranked.append((name, score))
    ranked.sort(key=lambda item: item[1], reverse=True)
    top_matches = [{"speaker": name, "score": round(score, 4)} for name, score in ranked[:3]]
    best_name, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else -1.0
    margin = best_score - second_score
    return top_matches, best_name, best_score, margin


def average_embeddings(embeddings: List[np.ndarray]) -> Optional[np.ndarray]:
    if not embeddings:
        return None
    stacked = np.vstack(embeddings)
    averaged = np.mean(stacked, axis=0)
    norm = np.linalg.norm(averaged) + 1e-10
    return averaged / norm


def collect_sample_quotes(segments: List[Dict[str, object]], max_quotes: int = 3) -> List[str]:
    quotes = []
    for seg in segments:
        text = " ".join(str(seg.get("text", "")).split()).strip()
        if text:
            quotes.append(text)
        if len(quotes) >= max_quotes:
            break
    return quotes


def normalize_speaker_map(raw_map: Dict[str, str]) -> Dict[str, str]:
    normalized = {}
    for key, value in raw_map.items():
        map_key = str(key).strip()
        map_value = str(value).strip()
        if map_key and map_value:
            normalized[map_key] = map_value
    return normalized


def assign_unknown_cluster(embedding: np.ndarray, cluster_centers: List[np.ndarray], cluster_names: List[str]) -> Tuple[str, float]:
    if not cluster_centers:
        name = allocate_cluster_name(cluster_names)
        cluster_names.append(name)
        cluster_centers.append(embedding.copy())
        return name, 0.0

    best_idx = -1
    best_score = -1.0
    for idx, center in enumerate(cluster_centers):
        if center.size != embedding.size:
            continue
        denom = (np.linalg.norm(center) * np.linalg.norm(embedding)) + 1e-10
        score = float(np.dot(center, embedding) / denom)
        if score > best_score:
            best_idx = idx
            best_score = score

    if best_score >= UNKNOWN_CLUSTER_THRESHOLD and best_idx >= 0:
        updated = cluster_centers[best_idx] + embedding
        cluster_centers[best_idx] = updated / (np.linalg.norm(updated) + 1e-10)
        return cluster_names[best_idx], best_score

    name = allocate_cluster_name(cluster_names)
    cluster_names.append(name)
    cluster_centers.append(embedding.copy())
    return name, best_score


PUNCT_SPLIT = re.compile(r"(?<=[。！？!?\n])")
ACTION_PATTERNS = (r"需要", r"安排", r"跟进", r"确认", r"推进", r"发送", r"同步", r"准备", r"对齐")
DECISION_PATTERNS = (r"决定", r"确定", r"先", r"就按", r"结论", r"可以", r"没问题")
RISK_PATTERNS = (r"风险", r"问题", r"待确认", r"不确定", r"还没", r"需要再")


def align_text_to_segments(full_text: str, segments: List[Dict[str, object]]) -> List[Dict[str, object]]:
    cleaned = [chunk.strip() for chunk in PUNCT_SPLIT.split(full_text) if chunk.strip()]
    if not segments:
        return []
    if not cleaned:
        for seg in segments:
            seg["text"] = ""
        return segments

    total_chars = sum(len(strip_whitespace(chunk)) for chunk in cleaned) or 1
    total_duration = sum(max(1, seg["end_time"] - seg["start_time"]) for seg in segments) or 1

    chunk_idx = 0
    carry_chars = 0
    for seg in segments:
        seg_duration = max(1, seg["end_time"] - seg["start_time"])
        seg_target_chars = max(1, round(seg_duration / total_duration * total_chars))
        pieces = []
        while chunk_idx < len(cleaned) and carry_chars < seg_target_chars:
            chunk = cleaned[chunk_idx]
            pieces.append(chunk)
            carry_chars += len(strip_whitespace(chunk)) or len(chunk)
            chunk_idx += 1
        seg["text"] = " ".join(pieces).strip()
        carry_chars = max(0, carry_chars - seg_target_chars)

    if chunk_idx < len(cleaned):
        tail = " ".join(cleaned[chunk_idx:]).strip()
        if tail:
            segments[-1]["text"] = f"{segments[-1].get('text', '')} {tail}".strip()

    return segments


def merge_adjacent_segments(segments: List[Dict[str, object]], gap_ms: int = 400, min_duration_ms: int = 0) -> List[Dict[str, object]]:
    if not segments:
        return []
    merged = [dict(segments[0])]
    for seg in segments[1:]:
        prev = merged[-1]
        if seg["start_time"] - prev["end_time"] <= gap_ms and seg.get("speaker_hint") == prev.get("speaker_hint"):
            prev["end_time"] = max(prev["end_time"], seg["end_time"])
        else:
            merged.append(dict(seg))
    if min_duration_ms <= 0:
        return merged
    return [seg for seg in merged if seg["end_time"] - seg["start_time"] >= min_duration_ms]


def consolidate_segments(segments: List[Dict[str, object]]) -> List[Dict[str, object]]:
    consolidated: List[Dict[str, object]] = []
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue
        if consolidated and consolidated[-1].get("speaker") == seg.get("speaker") and seg.get("start_time", 0) - consolidated[-1].get("end_time", 0) <= 1000:
            prev = consolidated[-1]
            prev["end_time"] = seg.get("end_time", prev["end_time"])
            prev["text"] = f"{prev['text']} {text}".strip()
            prev["speaker_confidence"] = round(max(float(prev.get("speaker_confidence", 0.0)), float(seg.get("speaker_confidence", 0.0))), 4)
            continue
        consolidated.append(dict(seg))
    return consolidated


def build_transcript(segments: List[Dict[str, object]]) -> str:
    lines = []
    for seg in segments:
        speaker = seg.get("speaker", "Unknown")
        timestamp = format_timestamp(seg.get("start_time", 0))
        text = seg.get("text", "").strip()
        if text:
            lines.append(f"[{timestamp}] {speaker}: {text}")
    return "\n".join(lines)


def build_summary(transcript_segments: List[Dict[str, object]], speakers: List[Dict[str, object]], reference_text: str, confidence_flags: List[str]) -> Dict[str, object]:
    sentences = []
    for seg in transcript_segments:
        for piece in split_summary_sentences(seg.get("text", "")):
            if piece:
                sentences.append({"speaker": seg.get("speaker", "Unknown"), "text": piece})

    key_points = unique_ordered([item["text"] for item in sentences[:8]])
    decisions = unique_ordered([item["text"] for item in sentences if contains_pattern(item["text"], DECISION_PATTERNS)])[:5]
    action_items = []
    for item in sentences:
        if contains_pattern(item["text"], ACTION_PATTERNS):
            action_items.append({"owner": item["speaker"], "task": item["text"], "deadline": "未明确"})
    action_items = dedupe_action_items(action_items)[:6]
    risks = unique_ordered([item["text"] for item in sentences if contains_pattern(item["text"], RISK_PATTERNS)])[:5]

    style_notes = ["参考了历史纪要的术语和表述风格" if reference_text else "未提供历史纪要，使用通用会议纪要模板"]
    if confidence_flags:
        style_notes.append("当前纪要基于含低置信度片段的转写结果生成")

    return {
        "participants": [speaker["display_name"] for speaker in speakers],
        "overview": key_points[:3],
        "key_points": key_points[:8],
        "decisions": decisions,
        "action_items": action_items,
        "risks_or_open_items": risks,
        "style_notes": style_notes,
    }


def build_summary_markdown(summary: Dict[str, object]) -> str:
    lines = ["# 会议纪要", ""]

    participants = summary.get("participants", [])
    if participants:
        lines.append(f"参会人：{'、'.join(str(item) for item in participants)}")
        lines.append("")

    overview = summary.get("overview", [])
    if overview:
        lines.append("## 核心结论")
        for item in overview:
            lines.append(f"- {item}")
        lines.append("")

    key_points = summary.get("key_points", [])
    if key_points:
        lines.append("## 讨论要点")
        for item in key_points:
            lines.append(f"- {item}")
        lines.append("")

    decisions = summary.get("decisions", [])
    if decisions:
        lines.append("## 结论")
        for item in decisions:
            lines.append(f"- {item}")
        lines.append("")

    action_items = summary.get("action_items", [])
    if action_items:
        lines.append("## 行动项")
        for item in action_items:
            owner = str(item.get("owner", "未明确"))
            task = str(item.get("task", "")).strip()
            deadline = str(item.get("deadline", "未明确"))
            lines.append(f"- {owner}：{task}（截止：{deadline}）")
        lines.append("")

    risks = summary.get("risks_or_open_items", [])
    if risks:
        lines.append("## 风险与待确认")
        for item in risks:
            lines.append(f"- {item}")
        lines.append("")

    style_notes = summary.get("style_notes", [])
    if style_notes:
        lines.append("## 备注")
        for item in style_notes:
            lines.append(f"- {item}")

    return "\n".join(lines).strip()


def build_fallback_summary_payload(transcript_segments: List[Dict[str, object]], speakers: List[Dict[str, object]], reference_text: str, confidence_flags: List[str]) -> Dict[str, object]:
    summary = build_summary(transcript_segments, speakers, reference_text, confidence_flags)
    return {
        "summary": summary,
        "summary_markdown": build_summary_markdown(summary),
        "summary_source": "heuristic",
    }


def load_api_key() -> str:
    for env_name in ("STEPFUN_API_KEY", "STEP_API_KEY"):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    for key_path in ("~/.stepfun_api_key", "~/.step_api_key"):
        expanded = os.path.expanduser(key_path)
        try:
            with open(expanded, "r", encoding="utf-8") as handle:
                value = handle.read().strip()
        except OSError:
            continue
        if value:
            return value
    return ""


def call_step_llm_json(system_prompt: str, user_prompt: str, response_hint: str = "json_object") -> Dict[str, object]:
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("StepFun API key is not configured for LLM enrichment")

    payload = {
        "model": STEP_LLM_MODEL,
        "temperature": 0.2,
        "response_format": {"type": response_hint},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    req = urllib.request.Request(
        STEP_CHAT_COMPLETIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Step LLM HTTP {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Step LLM connection error: {exc.reason}") from exc

    data = json.loads(raw)
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    return json.loads(str(content).strip())


def estimate_speaker_count_heuristic(full_text: str, known_names: List[str]) -> Dict[str, object]:
    cleaned = full_text[:6000]
    text_names = []
    for name in known_names:
        if name and name in cleaned:
            text_names.append(name)
    estimate = max(2, min(6, len(set(text_names)) + 2 if text_names else 4))
    return {
        "estimated_speakers": estimate,
        "likely_names": unique_ordered(text_names),
        "reasoning": "heuristic-fallback",
        "source": "heuristic",
    }


def estimate_speaker_count(full_text: str, known_names: List[str]) -> Dict[str, object]:
    clipped = full_text[:12000]
    system_prompt = (
        "你是会议结构分析助手。根据转写文本推测本场会议大约有几位说话人。"
        "不要凭空编造姓名。输出 JSON，字段必须包括 estimated_speakers(int), likely_names(array), reasoning(string)。"
    )
    user_prompt = (
        f"已知可能参会人名单：{', '.join(known_names) if known_names else '无'}\n"
        "请只根据下面的会议转写文本，判断更合理的说话人数上限/近似值。\n"
        "如果不确定，给保守估计。\n\n"
        f"{clipped}"
    )
    try:
        data = call_step_llm_json(system_prompt, user_prompt)
        estimated = int(data.get("estimated_speakers", 0) or 0)
        likely_names = data.get("likely_names", [])
        if estimated <= 0:
            raise RuntimeError("LLM returned invalid estimated_speakers")
        return {
            "estimated_speakers": max(2, min(8, estimated)),
            "likely_names": [str(item).strip() for item in likely_names if str(item).strip()],
            "reasoning": str(data.get("reasoning", "")).strip(),
            "source": "step-llm",
        }
    except Exception:
        return estimate_speaker_count_heuristic(full_text, known_names)


def summarize_with_llm(
    transcript: str,
    transcript_segments: List[Dict[str, object]],
    speakers: List[Dict[str, object]],
    reference_text: str,
    confidence_flags: List[str],
) -> Dict[str, object]:
    clipped_transcript = transcript[:20000]
    participants = [speaker["display_name"] for speaker in speakers]
    system_prompt = (
        "你是一个会议纪要助手。请把会议 transcript 提炼成结构化纪要。"
        "输出 JSON，字段必须包括 participants(array), overview(array), key_points(array), decisions(array),"
        "action_items(array of {owner, task, deadline}), risks_or_open_items(array), style_notes(array), summary_markdown(string)。"
        "要求：summary_markdown 用简洁中文，像正式会议纪要，不要照抄大量原文。"
    )
    user_prompt = (
        f"参会人候选：{', '.join(participants) if participants else '未明确'}\n"
        f"历史纪要参考：{'有' if reference_text else '无'}\n"
        f"低置信度提示：{'；'.join(confidence_flags[:8]) if confidence_flags else '无'}\n\n"
        f"会议 transcript:\n{clipped_transcript}"
    )
    try:
        data = call_step_llm_json(system_prompt, user_prompt)
        summary = {
            "participants": [str(item).strip() for item in data.get("participants", []) if str(item).strip()],
            "overview": [str(item).strip() for item in data.get("overview", []) if str(item).strip()],
            "key_points": [str(item).strip() for item in data.get("key_points", []) if str(item).strip()],
            "decisions": [str(item).strip() for item in data.get("decisions", []) if str(item).strip()],
            "action_items": [
                {
                    "owner": str(item.get("owner", "未明确")).strip() or "未明确",
                    "task": str(item.get("task", "")).strip(),
                    "deadline": str(item.get("deadline", "未明确")).strip() or "未明确",
                }
                for item in data.get("action_items", [])
                if isinstance(item, dict) and str(item.get("task", "")).strip()
            ],
            "risks_or_open_items": [str(item).strip() for item in data.get("risks_or_open_items", []) if str(item).strip()],
            "style_notes": [str(item).strip() for item in data.get("style_notes", []) if str(item).strip()],
        }
        summary_markdown = str(data.get("summary_markdown", "")).strip() or build_summary_markdown(summary)
        return {
            "summary": summary,
            "summary_markdown": summary_markdown,
            "summary_source": "step-llm",
        }
    except Exception:
        return build_fallback_summary_payload(
            transcript_segments=transcript_segments,
            speakers=speakers,
            reference_text=reference_text,
            confidence_flags=confidence_flags,
        )


def compute_audio_fingerprint(audio_path: str) -> str:
    stat = os.stat(audio_path)
    payload = f"{os.path.abspath(audio_path)}:{stat.st_size}:{int(stat.st_mtime)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def cache_file_path(audio_path: str, stage: str, extra_parts: Optional[List[str]] = None) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    parts = [compute_audio_fingerprint(audio_path), stage]
    if extra_parts:
        parts.extend(str(part) for part in extra_parts if str(part))
    filename = "--".join(parts) + ".json"
    return os.path.join(CACHE_DIR, filename)


def load_json_cache(path: str) -> Optional[Dict[str, object]]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json_cache(path: str, payload: Dict[str, object]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def load_reference_text(reference_path: Optional[str]) -> str:
    if not reference_path:
        return ""
    with open(reference_path, "r", encoding="utf-8") as handle:
        return handle.read().strip()


def load_speaker_map(speaker_map_path: Optional[str]) -> Dict[str, str]:
    if not speaker_map_path:
        return {}
    with open(speaker_map_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RuntimeError("Speaker map must be a JSON object like {\"Speaker_A\": \"浚哲\"}")
    return normalize_speaker_map(data)


def make_processing_backend(segmenter_name: str, transcriber_result: Dict[str, object], speaker_name: str) -> Dict[str, object]:
    return {"segmenter": segmenter_name, "transcriber": transcriber_result.get("backend", "unknown"), "speaker_resolver": speaker_name, "transport": transcriber_result.get("transport", "unknown")}


def strip_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)


def split_summary_sentences(text: str) -> List[str]:
    return [item.strip() for item in re.split(r"[。！？!?\n]+", text) if item.strip()]


def contains_pattern(text: str, patterns: Tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def unique_ordered(items: List[object]) -> List[object]:
    seen = set()
    output = []
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, dict) else str(item)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def dedupe_action_items(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    deduped = []
    seen = set()
    for item in items:
        key = (item["owner"], item["task"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def dedupe_strings(items: List[str]) -> List[str]:
    return unique_ordered(items)


def samples_to_ms(samples: int, sr: int) -> int:
    return int(samples / sr * 1000)


def ms_between(start: int, end: int, sr: int) -> int:
    return samples_to_ms(end - start, sr)


def slice_audio(audio: np.ndarray, sr: int, start_ms: int, end_ms: int) -> np.ndarray:
    start = max(0, int(start_ms / 1000 * sr))
    end = max(start + 1, int(end_ms / 1000 * sr))
    return audio[start:end]


def load_wav(path: str) -> Tuple[np.ndarray, int]:
    with wave.open(path, "rb") as handle:
        sr = handle.getframerate()
        sample_width = handle.getsampwidth()
        channels = handle.getnchannels()
        frames = handle.readframes(handle.getnframes())
    if sample_width != 2:
        raise RuntimeError(f"Unsupported WAV sample width: {sample_width}")
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)
    return audio, sr


def format_timestamp(value_ms: int) -> str:
    total_seconds = max(0, int(value_ms / 1000))
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


def allocate_cluster_name(existing_names: List[str]) -> str:
    idx = len(existing_names)
    return f"Speaker_{chr(ord('A') + idx)}"


def safe_unlink(path: str) -> None:
    if path and os.path.exists(path):
        try:
            os.unlink(path)
        except OSError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Meeting audio -> transcript + summary JSON")
    parser.add_argument("--audio", required=True, help="Path to meeting audio file")
    parser.add_argument("--reference", help="Optional historical meeting note for style reference")
    parser.add_argument("--speaker-map", help="Optional JSON map for manual speaker confirmation")
    parser.add_argument("--language", default="zh", help="Transcription language")
    parser.add_argument("--num-speakers", type=int, help="Optional diarization hint for total speaker count")
    parser.add_argument("--max-new-chunks", type=int, help="Only run pyannote on at most this many missing high-priority chunks")
    parser.add_argument("--out", help="Write result JSON to this path")
    parser.add_argument("--minutes-out", help="Optional markdown meeting minutes output path")
    parser.add_argument("--transcript-only", action="store_true", help="Print transcript only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not os.path.exists(args.audio):
        print(f"Error: Audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    normalized_audio = None
    segmenter_name = "energy-vad"
    normalized_audio, preprocess_meta = preprocess_audio(args.audio)
    try:
        transcriber = StepTranscriber()
        speaker_resolver = SpeakerResolver()
        confidence_flags = []
        speaker_map = load_speaker_map(args.speaker_map)
        voiceprint_names = sorted(speaker_resolver.voiceprint.load_all_voiceprints().keys())

        asr_cache_path = cache_file_path(args.audio, "asr", [args.language])
        asr_result = load_json_cache(asr_cache_path)
        if asr_result is None:
            asr_result = transcriber.transcribe(args.audio, args.language)
            save_json_cache(asr_cache_path, asr_result)
        full_text = str(asr_result.get("text", "")).strip()
        if not full_text:
            raise RuntimeError("Transcriber returned no text")

        speaker_count_estimate = estimate_speaker_count(full_text, voiceprint_names)
        effective_num_speakers = args.num_speakers or int(speaker_count_estimate.get("estimated_speakers", 4) or 4)

        try:
            diarization_cache_path = cache_file_path(args.audio, "diarization", [str(effective_num_speakers)])
            diarization_cache = load_json_cache(diarization_cache_path)
            if diarization_cache is None:
                normalized_wav, normalized_sr = load_wav(normalized_audio)
                segment_bounds, diarization_meta = selective_chunked_diarization(
                    args.audio,
                    effective_num_speakers,
                    normalized_wav,
                    normalized_sr,
                    max_new_chunks=args.max_new_chunks,
                )
                save_json_cache(diarization_cache_path, {"segments": segment_bounds, "meta": diarization_meta})
            else:
                segment_bounds = diarization_cache.get("segments", [])
                diarization_meta = diarization_cache.get("meta", {})
            segmenter_name = "pyannote-community-1-chunked"
        except Exception as exc:
            segmenter = EnergySegmenter()
            segment_bounds = segmenter.segment(normalized_audio)
            segmenter_name = segmenter.name
            diarization_meta = {}
            confidence_flags.append(f"Pyannote unavailable, fell back to energy-vad: {exc}")

        working_segments = [dict(seg) for seg in segment_bounds]
        working_segments = align_text_to_segments(full_text, working_segments)
        working_segments, speakers, resolver_flags, open_questions, speaker_review = speaker_resolver.resolve(
            normalized_audio,
            working_segments,
            speaker_map=speaker_map,
        )
        confidence_flags.extend(resolver_flags)
        transcript_segments = consolidate_segments(working_segments)
        transcript = build_transcript(transcript_segments)
        reference_text = load_reference_text(args.reference)
        summary_payload = summarize_with_llm(
            transcript=transcript,
            transcript_segments=transcript_segments,
            speakers=speakers,
            reference_text=reference_text,
            confidence_flags=confidence_flags,
        )
        summary = summary_payload["summary"]
        summary_markdown = summary_payload["summary_markdown"]

        output = {
            "audio_file": os.path.basename(args.audio),
            "processing_backend": make_processing_backend(segmenter_name, asr_result, speaker_resolver.name),
            "preprocess": preprocess_meta,
            "speakers": speakers,
            "segments": transcript_segments,
            "transcript": transcript,
            "summary": summary,
            "summary_markdown": summary_markdown,
            "summary_source": summary_payload.get("summary_source", "heuristic"),
            "open_questions": open_questions,
            "confidence_flags": dedupe_strings(confidence_flags),
            "speaker_review": speaker_review,
            "speaker_map_applied": speaker_map,
            "speaker_count_estimate": speaker_count_estimate,
            "effective_num_speakers": effective_num_speakers,
            "diarization_meta": diarization_meta,
            "reference_used": bool(reference_text),
            "usage": asr_result.get("usage", {}),
            "full_text": full_text,
        }

        if args.transcript_only:
            print(transcript)
            return

        formatted = json.dumps(output, ensure_ascii=False, indent=2)
        if args.out:
            out_dir = os.path.dirname(os.path.abspath(args.out))
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(formatted)
            print(f"Saved to: {args.out}", file=sys.stderr)
        if args.minutes_out:
            minutes_dir = os.path.dirname(os.path.abspath(args.minutes_out))
            if minutes_dir:
                os.makedirs(minutes_dir, exist_ok=True)
            with open(args.minutes_out, "w", encoding="utf-8") as handle:
                handle.write(summary_markdown + "\n")
            print(f"Saved minutes to: {args.minutes_out}", file=sys.stderr)
        print(formatted)
    except Exception as exc:
        error_payload = {
            "audio_file": os.path.basename(args.audio),
            "processing_backend": {},
            "speakers": [],
            "segments": [],
            "transcript": "",
            "summary": {"participants": [], "overview": [], "key_points": [], "decisions": [], "action_items": [], "risks_or_open_items": [], "style_notes": []},
            "open_questions": [{"speaker": "system", "question": str(exc)}],
            "confidence_flags": [f"Pipeline failed: {exc}"],
        }
        print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        sys.exit(1)
    finally:
        safe_unlink(normalized_audio or "")


if __name__ == "__main__":
    main()
