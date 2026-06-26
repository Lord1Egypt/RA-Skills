#!/usr/bin/env python3
"""Music analysis v2 core — structure, groove, harmonic tension, timbre, explainable emotion."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import librosa

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def to_native(obj: Any) -> Any:
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_native(v) for v in obj]
    return obj


def format_ts(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    minutes = int(seconds // 60)
    rem = int(seconds % 60)
    return f"{minutes}:{rem:02d}"


def safe_div(a: float, b: float) -> float:
    return float(a) / float(b) if b else 0.0


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def load_audio(path: Path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    if y.size == 0:
        raise ValueError("empty audio")
    return y, sr


def estimate_key(chroma_mean: np.ndarray) -> dict[str, Any]:
    chroma = chroma_mean / (np.sum(chroma_mean) + 1e-9)
    major_scores = []
    minor_scores = []
    for i in range(12):
        major_scores.append(cosine_similarity(chroma, np.roll(MAJOR_PROFILE, i)))
        minor_scores.append(cosine_similarity(chroma, np.roll(MINOR_PROFILE, i)))
    major_scores = np.array(major_scores)
    minor_scores = np.array(minor_scores)
    best_major = int(np.argmax(major_scores))
    best_minor = int(np.argmax(minor_scores))
    best_major_score = float(major_scores[best_major])
    best_minor_score = float(minor_scores[best_minor])
    if best_major_score >= best_minor_score:
        tonic = NOTES[best_major]
        mode = "major"
        best = best_major_score
        runner_up = sorted(major_scores.tolist(), reverse=True)[1]
    else:
        tonic = NOTES[best_minor]
        mode = "minor"
        best = best_minor_score
        runner_up = sorted(minor_scores.tolist(), reverse=True)[1]
    clarity = max(0.0, min(1.0, best - runner_up + 0.35))
    entropy = float(-np.sum(chroma * np.log2(chroma + 1e-12)) / math.log2(12))
    return {
        "key_estimate": f"{tonic} {mode}",
        "tonic": tonic,
        "mode": mode,
        "key_clarity": round(float(clarity), 3),
        "chroma_entropy": round(entropy, 3),
    }


def describe_timbre(brightness: float, flatness: float, low_ratio: float, contrast: float, bandwidth: float) -> list[str]:
    tags = []
    if brightness < 1400:
        tags.append("warm/dark")
    elif brightness > 2800:
        tags.append("bright/brittle")
    else:
        tags.append("balanced")
    if flatness < 0.06:
        tags.append("harmonically rich")
    elif flatness > 0.18:
        tags.append("grainy/noisy")
    if low_ratio > 0.22:
        tags.append("full low-end")
    elif low_ratio < 0.10:
        tags.append("light low-end")
    if contrast > 20:
        tags.append("high contrast")
    if bandwidth > 2600:
        tags.append("wide-spectrum")
    return tags


def analyze_timbre(y: np.ndarray, sr: int) -> dict[str, Any]:
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    flatness = librosa.feature.spectral_flatness(y=y)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)[0]
    stft = np.abs(librosa.stft(y))
    power = stft ** 2
    freqs = librosa.fft_frequencies(sr=sr)
    low_mask = freqs < 200
    high_mask = freqs > 5000
    total_power = float(np.sum(power) + 1e-9)
    low_ratio = float(np.sum(power[low_mask, :]) / total_power) if np.any(low_mask) else 0.0
    air_ratio = float(np.sum(power[high_mask, :]) / total_power) if np.any(high_mask) else 0.0
    dynamic_range = float(np.percentile(rms, 95) - np.percentile(rms, 10))
    return {
        "centroid_mean": round(float(np.mean(centroid)), 2),
        "rolloff_mean": round(float(np.mean(rolloff)), 2),
        "flatness_mean": round(float(np.mean(flatness)), 4),
        "bandwidth_mean": round(float(np.mean(bandwidth)), 2),
        "contrast_mean": [round(float(x), 3) for x in contrast.mean(axis=1)],
        "low_end_ratio": round(low_ratio, 3),
        "air_ratio": round(air_ratio, 3),
        "dynamic_range": round(dynamic_range, 4),
        "descriptor_tags": describe_timbre(
            float(np.mean(centroid)),
            float(np.mean(flatness)),
            low_ratio,
            float(np.mean(contrast)),
            float(np.mean(bandwidth)),
        ),
    }


def analyze_groove(y: np.ndarray, sr: int, duration: float) -> dict[str, Any]:
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    iois = np.diff(beat_times) if len(beat_times) > 1 else np.array([])
    pulse_stability = max(0.0, 1.0 - safe_div(float(np.std(iois)) if iois.size else 0.0, float(np.mean(iois)) if iois.size else 1.0))
    onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="time")
    density = len(onset_times) / max(duration, 1e-9)
    swing_proxy = 0.0
    if len(beat_times) > 3:
        subdivisions = []
        for i in range(len(beat_times) - 1):
            start = beat_times[i]
            end = beat_times[i + 1]
            local = onset_times[(onset_times > start) & (onset_times < end)]
            if local.size:
                pos = float((local[0] - start) / max(end - start, 1e-9))
                subdivisions.append(pos)
        if subdivisions:
            median_pos = float(np.median(subdivisions))
            swing_proxy = abs(median_pos - 0.5) * 2.0
    pulse_confidence = max(0.0, min(1.0, 0.55 * pulse_stability + 0.45 * min(1.0, len(beat_times) / max(duration / 0.6, 1.0))))
    if pulse_stability > 0.82 and swing_proxy < 0.10:
        pocket = "grid-locked"
    elif pulse_stability > 0.70 and swing_proxy < 0.18:
        pocket = "steady"
    elif swing_proxy >= 0.18:
        pocket = "push-pull / swung"
    else:
        pocket = "loose / breathing"
    return {
        "tempo_bpm": round(tempo, 2),
        "beat_count": int(len(beat_times)),
        "pulse_stability": round(pulse_stability, 3),
        "pulse_confidence": round(pulse_confidence, 3),
        "onset_density_per_sec": round(density, 3),
        "swing_proxy": round(float(swing_proxy), 3),
        "pocket": pocket,
    }


def section_label(index: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if index < len(alphabet):
        return alphabet[index]
    return f"S{index+1}"


def analyze_structure(y: np.ndarray, sr: int, duration: float) -> dict[str, Any]:
    hop_length = 512
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

    chroma_delta = np.linalg.norm(np.diff(chroma, axis=1), axis=0) if chroma.shape[1] > 1 else np.array([])
    mfcc_delta = np.linalg.norm(np.diff(mfcc, axis=1), axis=0) if mfcc.shape[1] > 1 else np.array([])

    def norm(x: np.ndarray) -> np.ndarray:
        if x.size == 0:
            return x
        x = np.asarray(x, dtype=float)
        return (x - np.mean(x)) / (np.std(x) + 1e-9)

    min_len = min(len(onset_env), len(chroma_delta) or len(onset_env), len(mfcc_delta) or len(onset_env))
    novelty = 0.45 * norm(onset_env[:min_len])
    if chroma_delta.size:
        novelty += 0.35 * norm(chroma_delta[:min_len])
    if mfcc_delta.size:
        novelty += 0.20 * norm(mfcc_delta[:min_len])

    peak_frames = librosa.util.peak_pick(
        novelty,
        pre_max=24,
        post_max=24,
        pre_avg=24,
        post_avg=24,
        delta=0.75,
        wait=32,
    ) if novelty.size else np.array([])
    boundary_times = [float(t) for t in librosa.frames_to_time(peak_frames, sr=sr, hop_length=hop_length)]
    boundary_times = [t for t in boundary_times if 8.0 <= t <= duration - 8.0]
    raw_bounds = sorted(set([0.0] + boundary_times + [float(duration)]))

    filtered_bounds = [raw_bounds[0]]
    for bound in raw_bounds[1:]:
        if bound - filtered_bounds[-1] < 8.0 and bound != duration:
            continue
        filtered_bounds.append(bound)
    if filtered_bounds[-1] != duration:
        filtered_bounds.append(float(duration))

    sections = []
    prototypes: list[np.ndarray] = []
    for start, end in zip(filtered_bounds[:-1], filtered_bounds[1:]):
        if end - start < 6.0:
            continue
        start_f = int(librosa.time_to_frames(start, sr=sr, hop_length=hop_length))
        end_f = int(librosa.time_to_frames(end, sr=sr, hop_length=hop_length))
        feat = np.concatenate([
            np.mean(chroma[:, start_f:end_f], axis=1),
            np.mean(mfcc[:, start_f:end_f], axis=1),
        ])
        sims = [cosine_similarity(feat, proto) for proto in prototypes]
        if sims and max(sims) > 0.965:
            idx = int(np.argmax(sims))
        else:
            prototypes.append(feat)
            idx = len(prototypes) - 1
        sections.append({
            "label": section_label(idx),
            "start": round(start, 2),
            "end": round(end, 2),
            "start_fmt": format_ts(start),
            "end_fmt": format_ts(end),
            "duration": round(end - start, 2),
        })
    merged_sections = []
    for s in sections:
        if merged_sections and merged_sections[-1]["label"] == s["label"]:
            merged_sections[-1]["end"] = s["end"]
            merged_sections[-1]["end_fmt"] = s["end_fmt"]
            merged_sections[-1]["duration"] = round(merged_sections[-1]["end"] - merged_sections[-1]["start"], 2)
        else:
            merged_sections.append(dict(s))

    repeat_groups: dict[str, int] = {}
    for s in merged_sections:
        repeat_groups[s["label"]] = repeat_groups.get(s["label"], 0) + 1
    repeated = [label for label, count in repeat_groups.items() if count > 1]
    return {
        "section_count": len(merged_sections),
        "sections": merged_sections,
        "repeated_sections": repeated,
        "structure_summary": " → ".join(s["label"] for s in merged_sections) if merged_sections else "single span",
        "analysis_notes": [
            "Section labels are similarity-based (A/B/C), not semantic verse/chorus labels.",
            "Repeated labels indicate returning material or close variants.",
        ],
    }


def analyze_harmony(y: np.ndarray, sr: int) -> dict[str, Any]:
    hop_length = 512
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
    chroma_mean = np.mean(chroma, axis=1)
    key = estimate_key(chroma_mean)
    chroma_diff = np.linalg.norm(np.diff(chroma, axis=1), axis=0)
    harmonic_change = float(np.mean(chroma_diff))
    harmonic_spikes = float(np.percentile(chroma_diff, 90)) if chroma_diff.size else 0.0
    tonnetz = librosa.feature.tonnetz(chroma=chroma, sr=sr)
    tonal_motion = float(np.mean(np.linalg.norm(np.diff(tonnetz, axis=1), axis=0))) if tonnetz.shape[1] > 1 else 0.0
    tension_score = min(1.0, 0.9 * harmonic_change + 0.6 * tonal_motion + (1.0 - key["key_clarity"]) * 0.5)
    if tension_score < 0.22:
        tension_desc = "stable / resolved"
    elif tension_score < 0.38:
        tension_desc = "gently searching"
    elif tension_score < 0.58:
        tension_desc = "restless / mobile"
    else:
        tension_desc = "high-tension / unresolved"
    return {
        **key,
        "harmonic_change_rate": round(harmonic_change, 4),
        "harmonic_spike_p90": round(harmonic_spikes, 4),
        "tonal_motion": round(tonal_motion, 4),
        "tension_score": round(tension_score, 3),
        "tension_description": tension_desc,
    }


def explain_emotion(groove: dict[str, Any], timbre: dict[str, Any], harmony: dict[str, Any], energy: dict[str, Any]) -> dict[str, Any]:
    arousal = min(1.0, energy["rms_p95"] / (energy["rms_mean"] + 1e-9) / 3.0 + groove["onset_density_per_sec"] / 8.0)
    brightness = timbre["centroid_mean"]
    tension = harmony["tension_score"]
    low_end = timbre["low_end_ratio"]
    if brightness < 1200 and tension < 0.35:
        valence = 0.35
    elif brightness > 2600 and tension < 0.35:
        valence = 0.72
    elif tension > 0.55:
        valence = 0.42
    else:
        valence = 0.56
    if arousal < 0.33:
        energy_word = "calm / inward"
    elif arousal < 0.66:
        energy_word = "present / moving"
    else:
        energy_word = "urgent / surging"
    if valence < 0.42:
        color_word = "shadowed / heavy"
    elif valence > 0.65:
        color_word = "open / lifted"
    else:
        color_word = "mixed / bittersweet"
    reasons = []
    reasons.append(f"pulse feels {groove['pocket']} with stability {groove['pulse_stability']}")
    reasons.append(f"timbre reads {', '.join(timbre['descriptor_tags'][:3])}")
    reasons.append(f"harmonic field is {harmony['tension_description']}")
    if low_end > 0.22:
        reasons.append("low-end weight adds body and gravity")
    overview = f"{energy_word}, {color_word}; emotional read is explained by groove, timbre, and harmonic tension rather than a black-box mood guess."
    return {
        "arousal": round(arousal, 3),
        "valence": round(valence, 3),
        "tension": round(tension, 3),
        "energy_word": energy_word,
        "color_word": color_word,
        "overview": overview,
        "reasons": reasons,
    }


def analyze_track(path: Path) -> dict[str, Any]:
    y, sr = load_audio(path)
    duration = len(y) / sr
    rms = librosa.feature.rms(y=y)[0]
    energy = {
        "rms_mean": round(float(np.mean(rms)), 6),
        "rms_std": round(float(np.std(rms)), 6),
        "rms_p95": round(float(np.percentile(rms, 95)), 6),
    }
    timbre = analyze_timbre(y, sr)
    groove = analyze_groove(y, sr, duration)
    harmony = analyze_harmony(y, sr)
    structure = analyze_structure(y, sr, duration)
    emotion = explain_emotion(groove, timbre, harmony, energy)
    return {
        "duration_sec": round(duration, 3),
        "sample_rate": sr,
        "energy": energy,
        "groove": groove,
        "timbre": timbre,
        "harmony": harmony,
        "structure": structure,
        "emotion": emotion,
        "analysis_notes": [
            "Structure labels are pattern labels, not verse/chorus claims.",
            "Swing is an onset-based proxy, useful for feel but not drummer-grade microtiming truth.",
            "Emotion is explainable: derived from measured pulse, timbre, and harmonic tension.",
        ],
    }
