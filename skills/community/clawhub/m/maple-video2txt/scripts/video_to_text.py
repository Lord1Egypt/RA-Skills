from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

# OpenClaw 技能版本
SUPPORTED_INPUT_SUFFIXES = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".flv",
    ".wmv",
    ".webm",
    ".m4v",
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
}
SUPPORTED_OUTPUT_SUFFIXES = {".srt", ".txt"}

DEFAULT_MODEL_SIZE = "base"
DEFAULT_DEVICE = "cpu"
DEFAULT_LANGUAGE = "zh"
DEFAULT_BEAM_SIZE = 2


@dataclass(slots=True)
class TranscriptSegment:
    index: int
    start: float
    end: float
    text: str


class ProgressReporter:
    def __init__(self, total_duration: float | None) -> None:
        self.total_duration = total_duration if total_duration and total_duration > 0 else None
        self.last_percent = -1
        self.last_segment_count = 0

    def update(self, current_end: float, segment_count: int) -> None:
        if self.total_duration is not None:
            percent = min(100, int((current_end / self.total_duration) * 100))
            if percent <= self.last_percent and segment_count == self.last_segment_count:
                return
            if percent == self.last_percent and percent not in (0, 100):
                return

            self.last_percent = percent
            self.last_segment_count = segment_count
            bar_width = 24
            filled = int((percent / 100) * bar_width)
            bar = "#" * filled + "-" * (bar_width - filled)
            sys.stdout.write(
                "\r"
                f"[transcribe] [{bar}] {percent:3d}% "
                f"({format_clock(current_end)} / {format_clock(self.total_duration)}) "
                f"segments={segment_count}"
            )
            sys.stdout.flush()

            # 每 10% 打印一行独立日志，方便后台追踪
            if percent % 10 == 0 and percent != self.last_percent:
                print(f"\n[progress] {percent}% done, {segment_count} segments so far")
            return

        if segment_count >= self.last_segment_count + 10:
            self.last_segment_count = segment_count
            print(
                f"[progress] processed {segment_count} segments, current position "
                f"{format_clock(current_end)}"
            )

    def finish(self) -> None:
        if self.total_duration is not None:
            sys.stdout.write("\n")
            sys.stdout.flush()


def log(message: str) -> None:
    print(f"[video_to_text] {message}")


def get_media_duration(file_path: Path) -> float | None:
    """使用 ffprobe 获取媒体文件时长（秒）"""
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        ffprobe = get_ffmpeg_exe().replace("ffmpeg", "ffprobe")
    except Exception:
        ffprobe = "ffprobe"

    cmd = [
        ffprobe,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except Exception:
        pass
    return None


def resolve_beam_size(beam_size_arg: str | int) -> int:
    """解析 beam-size 参数，默认使用 2"""
    # 如果用户指定了具体数字，直接使用
    if isinstance(beam_size_arg, int):
        return beam_size_arg

    # 尝试解析为数字
    try:
        return int(beam_size_arg)
    except (ValueError, TypeError):
        pass

    # 默认使用 2
    log(f"Using default beam-size={DEFAULT_BEAM_SIZE}")
    return DEFAULT_BEAM_SIZE


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_model_dir = script_dir / "models"

    parser = argparse.ArgumentParser(
        description="Transcribe a local video/audio file into SRT and TXT using faster-whisper."
    )
    parser.add_argument("--input", required=True, help="Path to the local video/audio file.")
    parser.add_argument(
        "--output-dir",
        help="Directory for output files. Defaults to the input file directory.",
    )
    parser.add_argument(
        "--output-path",
        help=(
            "Base output path for the generated files. Example: "
            "D:\\out\\result or D:\\out\\result.srt. The script will generate "
            "D:\\out\\result.srt and D:\\out\\result.txt."
        ),
    )
    parser.add_argument(
        "--model-dir",
        default=str(default_model_dir),
        help=f"Directory for whisper model downloads. Defaults to {default_model_dir}.",
    )
    parser.add_argument(
        "--model-size",
        default=DEFAULT_MODEL_SIZE,
        help="Whisper model size or local model path. Defaults to 'base'.",
    )
    parser.add_argument(
        "--language",
        choices=("auto", "zh", "en"),
        default=DEFAULT_LANGUAGE,
        help="Recognition language. Defaults to zh.",
    )
    parser.add_argument(
        "--device",
        choices=("cpu", "cuda"),
        default=DEFAULT_DEVICE,
        help="Inference device. Defaults to cpu.",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="faster-whisper compute_type. Defaults to int8 for CPU-friendly inference.",
    )
    parser.add_argument(
        "--beam-size",
        default=str(DEFAULT_BEAM_SIZE),
        help="Beam size for decoding. Defaults to 2.",
    )
    parser.add_argument(
        "--no-vad-filter",
        action="store_true",
        help="Disable VAD filtering. VAD is enabled by default to reduce non-speech noise.",
    )
    return parser.parse_args()


def fail(message: str, exit_code: int = 1) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return exit_code


def validate_input_path(input_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    if input_path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        raise ValueError(
            f"Unsupported input file type '{input_path.suffix}'. Supported types: {supported}"
        )


def build_output_paths(
    input_path: Path,
    output_dir: Path | None,
    output_path: Path | None,
) -> tuple[Path, Path]:
    if output_path is not None:
        target_parent = output_path.parent
        target_parent.mkdir(parents=True, exist_ok=True)
        base_name = (
            output_path.stem if output_path.suffix.lower() in SUPPORTED_OUTPUT_SUFFIXES else output_path.name
        )
        return target_parent / f"{base_name}.srt", target_parent / f"{base_name}.txt"

    target_dir = output_dir if output_dir is not None else input_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    return target_dir / f"{stem}.srt", target_dir / f"{stem}.txt"


def format_srt_timestamp(seconds: float) -> str:
    total_milliseconds = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def format_clock(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


@lru_cache(maxsize=1)
def get_opencc():
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'opencc'. Install dependencies first, for example: "
            "pip install -r requirements.txt"
        ) from exc

    return OpenCC("t2s")


def convert_chinese_text(text: str, language: str) -> str:
    if language != "zh":
        return text
    return get_opencc().convert(text)


def to_transcript_segment(raw_segment: object, language: str, index: int) -> TranscriptSegment | None:
    text = normalize_text(getattr(raw_segment, "text", ""))
    if not text:
        return None
    text = convert_chinese_text(text, language)

    start = float(getattr(raw_segment, "start", 0.0))
    end = float(getattr(raw_segment, "end", start))
    if end < start:
        end = start

    return TranscriptSegment(index=index, start=start, end=end, text=text)


def render_srt(segments: list[TranscriptSegment]) -> str:
    blocks: list[str] = []
    for segment in segments:
        blocks.append(
            "\n".join(
                [
                    str(segment.index),
                    f"{format_srt_timestamp(segment.start)} --> {format_srt_timestamp(segment.end)}",
                    segment.text,
                ]
            )
        )

    return "\n\n".join(blocks) + ("\n" if blocks else "")


def render_txt(segments: list[TranscriptSegment]) -> str:
    if not segments:
        return ""
    return "\n".join(segment.text for segment in segments) + "\n"


def load_whisper_model(model_size: str, model_dir: Path, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'faster-whisper'. Install dependencies first, for example: "
            "pip install -r requirements.txt"
        ) from exc

    model_dir.mkdir(parents=True, exist_ok=True)

    return WhisperModel(
        model_size,
        device=device,
        compute_type=compute_type,
        download_root=str(model_dir),
    )


def transcribe_file(
    input_path: Path,
    model_size: str,
    model_dir: Path,
    language: str,
    device: str,
    compute_type: str,
    beam_size: int,
    vad_filter: bool,
) -> tuple[list[TranscriptSegment], object]:
    log(f"Loading model '{model_size}' from {model_dir}")
    model = load_whisper_model(
        model_size=model_size,
        model_dir=model_dir,
        device=device,
        compute_type=compute_type,
    )

    log(f"Starting transcription on {input_path.name}")
    language_arg = None if language == "auto" else language
    raw_segments, info = model.transcribe(
        str(input_path),
        task="transcribe",
        language=language_arg,
        beam_size=beam_size,
        vad_filter=vad_filter,
    )

    output_language = language if language != "auto" else getattr(info, "language", "auto")
    total_duration = getattr(info, "duration", None)
    if isinstance(total_duration, (int, float)):
        log(f"Detected media duration: {format_clock(float(total_duration))}")

    segments: list[TranscriptSegment] = []
    progress = ProgressReporter(float(total_duration) if isinstance(total_duration, (int, float)) else None)

    for raw_segment in raw_segments:
        segment = to_transcript_segment(raw_segment, output_language, len(segments) + 1)
        if segment is None:
            continue
        segments.append(segment)
        progress.update(segment.end, len(segments))

    progress.finish()
    log(f"Transcription completed with {len(segments)} valid segments")
    return segments, info


def main() -> int:
    args = parse_args()

    if args.output_dir and args.output_path:
        return fail("Use either --output-dir or --output-path, not both.")

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    output_path = Path(args.output_path).expanduser().resolve() if args.output_path else None
    model_dir = Path(args.model_dir).expanduser().resolve()

    try:
        log(f"Validating input file: {input_path}")
        validate_input_path(input_path)
        srt_path, txt_path = build_output_paths(input_path, output_dir, output_path)
        log(f"Planned SRT output: {srt_path}")
        log(f"Planned TXT output: {txt_path}")

        # 获取视频时长（仅用于日志）
        duration = get_media_duration(input_path)
        if duration:
            log(f"Media duration: {format_clock(duration)}")
        beam_size = resolve_beam_size(args.beam_size)

        segments, info = transcribe_file(
            input_path=input_path,
            model_size=args.model_size,
            model_dir=model_dir,
            language=args.language,
            device=args.device,
            compute_type=args.compute_type,
            beam_size=beam_size,
            vad_filter=not args.no_vad_filter,
        )
    except Exception as exc:
        return fail(str(exc))

    log("Writing output files")
    srt_path.write_text(render_srt(segments), encoding="utf-8-sig")
    txt_path.write_text(render_txt(segments), encoding="utf-8-sig")

    detected_language = getattr(info, "language", "unknown")
    language_probability = getattr(info, "language_probability", None)
    probability_text = (
        f"{language_probability:.4f}" if isinstance(language_probability, (float, int)) else "n/a"
    )

    print(f"Input: {input_path}")
    print(f"SRT output: {srt_path}")
    print(f"TXT output: {txt_path}")
    print(f"Segments: {len(segments)}")
    print(f"Detected language: {detected_language}")
    print(f"Language confidence: {probability_text}")

    if not segments:
        print("No valid speech segments were recognized. Empty output files were generated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
