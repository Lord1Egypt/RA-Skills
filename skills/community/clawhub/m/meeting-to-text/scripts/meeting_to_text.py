from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torchaudio
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.sparse.linalg import eigsh
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]

# Allow overriding paths via environment variables for portability
FFMPEG_EXE = Path(os.getenv("MEETING_TO_TEXT_FFMPEG", PROJECT_ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"))
SENSEVOICE_MODEL = Path(os.getenv("MEETING_TO_TEXT_SENSEVOICE", PROJECT_ROOT / "models" / "SenseVoiceSmall"))
VAD_MODEL = Path(os.getenv("MEETING_TO_TEXT_VAD", PROJECT_ROOT / "models" / "fsmn-vad"))
THREE_D_SPEAKER_REPO = Path(os.getenv("MEETING_TO_TEXT_3D_SPEAKER", PROJECT_ROOT / "repos" / "3D-Speaker"))
THREE_D_SPEAKER_CACHE = Path(os.getenv("MEETING_TO_TEXT_3D_SPEAKER_CACHE", PROJECT_ROOT / "models" / "3d-speaker" / "hub"))

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm"}
SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}
SUPPORTED_EXTENSIONS = SUPPORTED_VIDEO_EXTENSIONS | SUPPORTED_AUDIO_EXTENSIONS

MIN_SEGMENT_SECONDS = 0.40
MERGE_GAP_SECONDS = 0.80
CHUNK_DURATION_SECONDS = 1.50
CHUNK_STEP_SECONDS = 0.75
SAMPLE_RATE = 16000

SPEAKER_MODEL_ID = "iic/speech_campplus_sv_zh_en_16k-common_advanced"
SPEAKER_MODEL_REVISION = "v1.0.0"
SPEAKER_MODEL_CKPT = "campplus_cn_en_common.pt"


class PipelineError(Exception):
    exit_code = 1

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(PipelineError):
    exit_code = 1


class MediaError(PipelineError):
    exit_code = 2


class DiarizationError(PipelineError):
    exit_code = 3


class TranscriptionError(PipelineError):
    exit_code = 4


class OutputWriteError(PipelineError):
    exit_code = 5


@dataclass
class DiarizationSegment:
    start: float
    end: float
    speaker_id: int


@dataclass
class TranscriptSegment:
    start: float
    end: float
    speaker_label: str
    text: str


def call_silently(func: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return func(*args, **kwargs)


def ensure_file(path: Path, description: str) -> None:
    if not path.exists():
        raise ValidationError(f"Missing {description}: {path}")


def ensure_supported_input(source_path: Path) -> None:
    if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValidationError(f"Unsupported input extension: {source_path.suffix or '<none>'}. Supported: {supported}")


def resolve_output_path(source_path: Path, output_target: Path) -> Path:
    if output_target.suffix.lower() == ".txt":
        final_path = output_target
    else:
        final_path = output_target / f"{source_path.stem}_transcript.txt"

    final_path.parent.mkdir(parents=True, exist_ok=True)
    return final_path


def create_work_dir(base_dir: Path | None) -> Path:
    if base_dir is not None:
        base_dir.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix="meeting_to_text_", dir=str(base_dir)))
    return Path(tempfile.mkdtemp(prefix="meeting_to_text_"))


def run_ffmpeg_normalize(source_path: Path, output_wav_path: Path) -> None:
    ensure_file(FFMPEG_EXE, "ffmpeg executable")
    command = [
        str(FFMPEG_EXE),
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(SAMPLE_RATE),
        "-c:a",
        "pcm_s16le",
        str(output_wav_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode != 0 or not output_wav_path.exists():
        message = completed.stderr.strip() or completed.stdout.strip() or "ffmpeg failed to normalize media"
        raise MediaError(message)


def load_waveform(wav_path: Path) -> tuple[torch.Tensor, int]:
    waveform, sample_rate = torchaudio.load(str(wav_path))
    if waveform.ndim != 2:
        raise MediaError(f"Unexpected waveform shape: {tuple(waveform.shape)}")
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != SAMPLE_RATE:
        waveform = torchaudio.functional.resample(waveform, sample_rate, SAMPLE_RATE)
        sample_rate = SAMPLE_RATE
    return waveform, sample_rate


def ensure_speakerlab_path() -> None:
    repo_path = str(THREE_D_SPEAKER_REPO)
    if repo_path not in sys.path:
        sys.path.insert(0, repo_path)


def ensure_speaker_model_cached() -> Path:
    target_dir = THREE_D_SPEAKER_CACHE / SPEAKER_MODEL_ID
    if (target_dir / "configuration.json").exists():
        return target_dir

    THREE_D_SPEAKER_CACHE.mkdir(parents=True, exist_ok=True)
    from modelscope.hub.snapshot_download import snapshot_download

    downloaded = snapshot_download(
        SPEAKER_MODEL_ID,
        revision=SPEAKER_MODEL_REVISION,
        cache_dir=str(THREE_D_SPEAKER_CACHE),
    )
    return Path(downloaded)


def load_embedding_runtime() -> tuple[Any, Any, Any]:
    ensure_speakerlab_path()
    from speakerlab.utils.builder import build
    from speakerlab.utils.config import Config
    from speakerlab.utils.utils import circle_pad

    model_dir = ensure_speaker_model_cached()
    checkpoint_path = model_dir / SPEAKER_MODEL_CKPT
    if not checkpoint_path.exists():
        raise DiarizationError(f"Missing speaker model checkpoint: {checkpoint_path}")

    config = Config(
        {
            "feature_extractor": {
                "obj": "speakerlab.process.processor.FBank",
                "args": {
                    "n_mels": 80,
                    "sample_rate": SAMPLE_RATE,
                    "mean_nor": True,
                },
            },
            "embedding_model": {
                "obj": "speakerlab.models.campplus.DTDNN.CAMPPlus",
                "args": {
                    "feat_dim": 80,
                    "embedding_size": 192,
                },
            },
        }
    )

    feature_extractor = build("feature_extractor", config)
    embedding_model = build("embedding_model", config)
    state_dict = torch.load(str(checkpoint_path), map_location="cpu")
    embedding_model.load_state_dict(state_dict)
    embedding_model.eval()
    return feature_extractor, embedding_model, circle_pad


def load_vad_model() -> AutoModel:
    ensure_file(VAD_MODEL, "local VAD model directory")
    return call_silently(
        AutoModel,
        model=str(VAD_MODEL),
        device="cpu",
        disable_update=True,
    )


def load_asr_model() -> AutoModel:
    ensure_file(SENSEVOICE_MODEL, "local SenseVoice model directory")
    return call_silently(
        AutoModel,
        model=str(SENSEVOICE_MODEL),
        device="cpu",
        disable_update=True,
    )


def run_vad(vad_model: AutoModel, wav_path: Path) -> list[list[float]]:
    result = call_silently(vad_model.generate, input=str(wav_path))
    if not isinstance(result, list) or not result or "value" not in result[0]:
        raise DiarizationError("VAD did not return usable segments")
    return [[item[0] / 1000.0, item[1] / 1000.0] for item in result[0]["value"]]


def chunk_interval(start: float, end: float, duration: float = CHUNK_DURATION_SECONDS, step: float = CHUNK_STEP_SECONDS) -> list[list[float]]:
    chunks: list[list[float]] = []
    chunk_start = start
    while chunk_start + duration < end + step:
        chunk_end = min(chunk_start + duration, end)
        chunks.append([chunk_start, chunk_end])
        chunk_start += step
    return chunks


def extract_embeddings(
    waveform: torch.Tensor,
    chunks: list[list[float]],
    feature_extractor: Any,
    embedding_model: Any,
    circle_pad: Any,
) -> np.ndarray:
    if not chunks:
        return np.zeros((0, 192), dtype=np.float32)

    wavs = [waveform[0, int(start * SAMPLE_RATE) : int(end * SAMPLE_RATE)] for start, end in chunks]
    if any(segment.numel() == 0 for segment in wavs):
        raise DiarizationError("Encountered an empty diarization chunk while extracting embeddings")

    max_len = max(segment.shape[0] for segment in wavs)
    padded = [circle_pad(segment, max_len) for segment in wavs]
    batch_tensor = torch.stack(padded).unsqueeze(1)

    embeddings: list[torch.Tensor] = []
    batch_start = 0
    batch_size = 64
    with torch.no_grad():
        while batch_start < len(chunks):
            wavs_batch = batch_tensor[batch_start : batch_start + batch_size]
            feats_batch = torch.vmap(feature_extractor)(wavs_batch)
            embeddings_batch = embedding_model(feats_batch).cpu()
            embeddings.append(embeddings_batch)
            batch_start += batch_size

    return torch.cat(embeddings, dim=0).numpy()


def eigen_gaps(eigenvalues: np.ndarray) -> list[float]:
    return [float(eigenvalues[idx + 1]) - float(eigenvalues[idx]) for idx in range(len(eigenvalues) - 1)]


def spectral_cluster(
    embeddings: np.ndarray,
    min_num_spks: int = 1,
    max_num_spks: int = 15,
    pval: float = 0.012,
    min_pnum: int = 6,
    oracle_num: int | None = None,
) -> np.ndarray:
    similarity = cosine_similarity(embeddings, embeddings)
    pruned = similarity.copy()
    n_elems = int((1 - pval) * pruned.shape[0])
    n_elems = min(n_elems, pruned.shape[0] - min_pnum)
    for index in range(pruned.shape[0]):
        low_indexes = np.argsort(pruned[index, :])[:n_elems]
        pruned[index, low_indexes] = 0

    pruned = 0.5 * (pruned + pruned.T)
    np.fill_diagonal(pruned, 0)
    degree = np.sum(np.abs(pruned), axis=1)
    laplacian = -pruned
    laplacian[np.diag_indices_from(laplacian)] = degree

    eig_count = min(max_num_spks + 1, max(1, laplacian.shape[0] - 1))
    lambdas, eig_vecs = eigsh(laplacian, k=eig_count, which="SM")

    if oracle_num is not None:
        num_speakers = oracle_num
    else:
        gap_values = eigen_gaps(lambdas[min_num_spks - 1 : max_num_spks + 1])
        num_speakers = int(np.argmax(gap_values)) + min_num_spks if gap_values else 1

    num_speakers = max(1, num_speakers)
    features = eig_vecs[:, :num_speakers]
    return KMeans(n_clusters=num_speakers, n_init=10, random_state=0).fit_predict(features)


def ahc_cluster(embeddings: np.ndarray, threshold: float = 0.4) -> np.ndarray:
    if embeddings.shape[0] <= 1:
        return np.zeros(embeddings.shape[0], dtype=int)

    scores = cosine_similarity(embeddings)
    condensed = squareform(-scores, checks=False)
    linkage_matrix = linkage(condensed, method="average")
    adjust = abs(linkage_matrix[:, 2].min())
    linkage_matrix[:, 2] += adjust
    return fcluster(linkage_matrix, -threshold + adjust, criterion="distance") - 1


def filter_minor_clusters(labels: np.ndarray, embeddings: np.ndarray, min_cluster_size: int) -> np.ndarray:
    cluster_set = np.unique(labels)
    cluster_sizes = np.array([(labels == cluster_id).sum() for cluster_id in cluster_set])
    minor_indexes = np.where(cluster_sizes <= min_cluster_size)[0]
    if len(minor_indexes) == 0:
        return labels

    minor_clusters = cluster_set[minor_indexes]
    major_indexes = np.where(cluster_sizes > min_cluster_size)[0]
    if len(major_indexes) == 0:
        return np.zeros_like(labels)

    major_clusters = cluster_set[major_indexes]
    major_centers = np.stack([embeddings[labels == cluster_id].mean(0) for cluster_id in major_clusters])
    updated = labels.copy()
    for index, cluster_id in enumerate(updated):
        if cluster_id in minor_clusters:
            scores = cosine_similarity(embeddings[index][np.newaxis], major_centers)
            updated[index] = major_clusters[int(scores.argmax())]
    return updated


def merge_by_cosine(labels: np.ndarray, embeddings: np.ndarray, threshold: float) -> np.ndarray:
    updated = labels.copy()
    while True:
        cluster_set = np.unique(updated)
        if len(cluster_set) == 1:
            return updated

        centers = np.stack([embeddings[updated == cluster_id].mean(0) for cluster_id in cluster_set])
        affinity = cosine_similarity(centers, centers)
        affinity = np.triu(affinity, 1)
        best_index = np.unravel_index(np.argmax(affinity), affinity.shape)
        if affinity[best_index] < threshold:
            return updated

        first, second = cluster_set[np.array(best_index)]
        updated[updated == second] = first


def cluster_embeddings(embeddings: np.ndarray) -> np.ndarray:
    if embeddings.ndim != 2:
        raise DiarizationError(f"Unexpected embedding shape: {embeddings.shape}")
    if embeddings.shape[0] <= 1:
        return np.zeros(embeddings.shape[0], dtype=int)

    if embeddings.shape[0] < 40:
        labels = ahc_cluster(embeddings)
    else:
        labels = spectral_cluster(embeddings)

    labels = filter_minor_clusters(labels, embeddings, min_cluster_size=4)
    return merge_by_cosine(labels, embeddings, threshold=0.8)


def compress_segments(segments: list[list[float]]) -> list[list[float]]:
    compressed: list[list[float]] = []
    for index, segment in enumerate(segments):
        start, end, speaker_id = segment
        if index == 0:
            compressed.append([start, end, speaker_id])
            continue

        previous = compressed[-1]
        if speaker_id == previous[2]:
            if start > previous[1]:
                compressed.append([start, end, speaker_id])
            else:
                previous[1] = end
            continue

        if start < previous[1]:
            midpoint = (previous[1] + start) / 2
            previous[1] = midpoint
            start = midpoint
        compressed.append([start, end, speaker_id])
    return compressed


def run_diarization(
    normalized_wav_path: Path,
    waveform: torch.Tensor,
    vad_model: AutoModel,
    feature_extractor: Any,
    embedding_model: Any,
    circle_pad: Any,
) -> list[DiarizationSegment]:
    vad_intervals = run_vad(vad_model, normalized_wav_path)
    chunks = [chunk for start, end in vad_intervals for chunk in chunk_interval(start, end)]
    if not chunks:
        raise DiarizationError("Diarization produced no chunks after VAD")

    embeddings = extract_embeddings(waveform, chunks, feature_extractor, embedding_model, circle_pad)
    if embeddings.shape[0] == 0:
        raise DiarizationError("Failed to extract speaker embeddings")

    labels = cluster_embeddings(embeddings)
    raw_segments = compress_segments([[chunk[0], chunk[1], int(label)] for chunk, label in zip(chunks, labels)])
    return [DiarizationSegment(start=item[0], end=item[1], speaker_id=int(item[2])) for item in raw_segments]


def normalize_diarization_segments(
    raw_segments: list[DiarizationSegment],
) -> tuple[list[DiarizationSegment], list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    failed_segments: list[dict[str, Any]] = []
    normalized: list[DiarizationSegment] = []

    for segment in sorted(raw_segments, key=lambda item: (item.start, item.end)):
        start = float(segment.start)
        end = float(segment.end)
        if end <= start:
            failed_segments.append({"start": round(start, 3), "end": round(end, 3), "reason": "invalid_segment"})
            continue
        if end - start < MIN_SEGMENT_SECONDS:
            failed_segments.append({"start": round(start, 3), "end": round(end, 3), "reason": "too_short"})
            continue

        if normalized and start < normalized[-1].end:
            start = normalized[-1].end

        if end <= start or end - start < MIN_SEGMENT_SECONDS:
            failed_segments.append({"start": round(start, 3), "end": round(end, 3), "reason": "too_short_after_clamp"})
            continue

        normalized.append(DiarizationSegment(start=start, end=end, speaker_id=segment.speaker_id))

    if not normalized:
        return [], failed_segments, warnings

    speaker_map: dict[int, int] = {}
    next_speaker = 1
    remapped: list[DiarizationSegment] = []
    for segment in normalized:
        if segment.speaker_id not in speaker_map:
            speaker_map[segment.speaker_id] = next_speaker
            next_speaker += 1
        remapped.append(DiarizationSegment(start=segment.start, end=segment.end, speaker_id=speaker_map[segment.speaker_id]))

    if len(speaker_map) == 1:
        warnings.append("only one speaker detected")

    return remapped, failed_segments, warnings


def save_segment_audio(
    waveform: torch.Tensor,
    segment: DiarizationSegment,
    output_path: Path,
) -> None:
    start_frame = max(0, int(segment.start * SAMPLE_RATE))
    end_frame = min(waveform.shape[1], int(segment.end * SAMPLE_RATE))
    if end_frame <= start_frame:
        raise TranscriptionError("Invalid segment slice produced empty audio")

    clip = waveform[:, start_frame:end_frame]
    if clip.numel() == 0:
        raise TranscriptionError("Empty waveform slice")

    torchaudio.save(str(output_path), clip, SAMPLE_RATE, encoding="PCM_S", bits_per_sample=16)


def postprocess_text(raw_text: str) -> str:
    processed = rich_transcription_postprocess(raw_text or "")
    return processed.strip()


def transcribe_segments(
    normalized_segments: list[DiarizationSegment],
    waveform: torch.Tensor,
    asr_model: AutoModel,
    segment_dir: Path,
) -> tuple[list[TranscriptSegment], list[dict[str, Any]], int]:
    transcripts: list[TranscriptSegment] = []
    failed_segments: list[dict[str, Any]] = []
    skipped_count = 0

    segment_dir.mkdir(parents=True, exist_ok=True)

    for index, segment in enumerate(normalized_segments):
        segment_path = segment_dir / f"segment_{index:04d}_speaker_{segment.speaker_id}.wav"
        try:
            save_segment_audio(waveform, segment, segment_path)
            result = call_silently(
                asr_model.generate,
                input=str(segment_path),
                language="auto",
                use_itn=True,
                batch_size_s=60,
                merge_vad=False,
            )
            if not isinstance(result, list) or not result or "text" not in result[0]:
                raise RuntimeError("SenseVoice returned no text field")
            text = postprocess_text(result[0]["text"])
            if not text:
                failed_segments.append(
                    {"start": round(segment.start, 3), "end": round(segment.end, 3), "reason": "empty_transcript"}
                )
                skipped_count += 1
                continue
            transcripts.append(
                TranscriptSegment(
                    start=segment.start,
                    end=segment.end,
                    speaker_label=f"说话人{segment.speaker_id}",
                    text=text,
                )
            )
        except Exception as exc:  # noqa: BLE001
            failed_segments.append(
                {"start": round(segment.start, 3), "end": round(segment.end, 3), "reason": f"asr_failed: {exc}"}
            )
            skipped_count += 1

    return transcripts, failed_segments, skipped_count


def join_text(left: str, right: str) -> str:
    if not left:
        return right
    if not right:
        return left
    if left.endswith((" ", "\n", "，", "。", "！", "？", ",", ".", "!", "?", ":", "：", ";", "；")):
        return left + right
    if re.search(r"[\u4e00-\u9fff]$", left) or re.match(r"^[\u4e00-\u9fff]", right):
        return left + right
    return f"{left} {right}"


def merge_transcripts(segments: list[TranscriptSegment]) -> list[TranscriptSegment]:
    if not segments:
        return []

    merged: list[TranscriptSegment] = [segments[0]]
    for current in segments[1:]:
        previous = merged[-1]
        if current.speaker_label == previous.speaker_label and current.start - previous.end <= MERGE_GAP_SECONDS:
            merged[-1] = TranscriptSegment(
                start=previous.start,
                end=current.end,
                speaker_label=previous.speaker_label,
                text=join_text(previous.text, current.text),
            )
            continue
        merged.append(current)
    return merged


def format_timestamp(seconds: float, *, ceiling: bool = False) -> str:
    whole_seconds = int(math.ceil(seconds) if ceiling else math.floor(seconds))
    whole_seconds = max(0, whole_seconds)
    hours, remainder = divmod(whole_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def write_transcript(output_path: Path, segments: list[TranscriptSegment]) -> None:
    lines: list[str] = []
    for segment in segments:
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end, ceiling=True)
        lines.append(f"[{start} - {end}] {segment.speaker_label}：{segment.text}")

    try:
        output_path.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    except OSError as exc:
        raise OutputWriteError(f"Failed to write transcript: {exc}") from exc


def build_result(
    status: str,
    input_path: Path,
    output_path: Path,
    speaker_count: int,
    segment_count: int,
    transcribed_segment_count: int,
    skipped_segment_count: int,
    failed_segments: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "status": status,
        "input_path": str(input_path),
        "output_path": str(output_path),
        "speaker_count": speaker_count,
        "segment_count": segment_count,
        "transcribed_segment_count": transcribed_segment_count,
        "skipped_segment_count": skipped_segment_count,
        "failed_segments": failed_segments,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract audio when needed, diarize speakers, and write a .txt transcript.")
    parser.add_argument("--input", required=True, help="Path to the source audio or video file")
    parser.add_argument("--output", required=True, help="Directory path or final .txt path for the transcript")
    parser.add_argument("--work-dir", help="Optional base directory for temporary files")
    return parser.parse_args()


def main() -> int:
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))

    args = parse_args()
    source_path = Path(args.input).expanduser().resolve()
    output_target = Path(args.output).expanduser().resolve()
    work_base = Path(args.work_dir).expanduser().resolve() if args.work_dir else None

    output_path = output_target if output_target.suffix.lower() == ".txt" else output_target / f"{source_path.stem}_transcript.txt"
    failed_segments: list[dict[str, Any]] = []
    warnings: list[str] = []

    try:
        if not source_path.exists():
            raise ValidationError(f"Input file does not exist: {source_path}")
        ensure_supported_input(source_path)
        output_path = resolve_output_path(source_path, output_target)

        ensure_file(FFMPEG_EXE, "ffmpeg executable")
        ensure_file(SENSEVOICE_MODEL, "SenseVoice model directory")
        ensure_file(VAD_MODEL, "VAD model directory")
        ensure_file(THREE_D_SPEAKER_REPO, "3D-Speaker repository")

        work_dir = create_work_dir(work_base)
        try:
            normalized_wav_path = work_dir / "normalized.wav"
            run_ffmpeg_normalize(source_path, normalized_wav_path)
            waveform, _ = load_waveform(normalized_wav_path)

            vad_model = load_vad_model()
            asr_model = load_asr_model()
            feature_extractor, embedding_model, circle_pad = load_embedding_runtime()

            raw_segments = run_diarization(
                normalized_wav_path=normalized_wav_path,
                waveform=waveform,
                vad_model=vad_model,
                feature_extractor=feature_extractor,
                embedding_model=embedding_model,
                circle_pad=circle_pad,
            )
            normalized_segments, normalization_failures, normalization_warnings = normalize_diarization_segments(raw_segments)
            failed_segments.extend(normalization_failures)
            warnings.extend(normalization_warnings)
            if not normalized_segments:
                raise DiarizationError("No usable speaker segments after normalization")

            transcript_segments, transcription_failures, skipped_count = transcribe_segments(
                normalized_segments=normalized_segments,
                waveform=waveform,
                asr_model=asr_model,
                segment_dir=work_dir / "segments",
            )
            failed_segments.extend(transcription_failures)

            if not transcript_segments:
                raise TranscriptionError("No usable transcript segments were produced")

            merged_transcripts = merge_transcripts(transcript_segments)
            if not merged_transcripts:
                raise TranscriptionError("Transcript merging produced no output")

            write_transcript(output_path, merged_transcripts)
            speaker_count = len({segment.speaker_label for segment in merged_transcripts})
            result = build_result(
                status="warning" if warnings or failed_segments else "success",
                input_path=source_path,
                output_path=output_path,
                speaker_count=speaker_count,
                segment_count=len(normalized_segments),
                transcribed_segment_count=len(transcript_segments),
                skipped_segment_count=len(normalization_failures) + skipped_count,
                failed_segments=failed_segments,
                warnings=warnings,
            )
            print(json.dumps(result, ensure_ascii=False))
            return 0
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)
    except PipelineError as exc:
        result = build_result(
            status="error",
            input_path=source_path,
            output_path=output_path,
            speaker_count=0,
            segment_count=0,
            transcribed_segment_count=0,
            skipped_segment_count=len(failed_segments),
            failed_segments=failed_segments,
            warnings=warnings + [exc.message],
        )
        print(json.dumps(result, ensure_ascii=False))
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

