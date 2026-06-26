from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_PACKAGES = {
    "cv2": "opencv-python-headless",
}


def check_dependencies() -> list[str]:
    """Return list of missing required package names."""
    missing = []
    for module_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(pip_name)
    return missing


_missing = check_dependencies()
if _missing:
    print(
        f"ERROR: Missing required dependencies: {', '.join(_missing)}\n"
        f"Install them with:  pip install {' '.join(_missing)}",
        file=sys.stderr,
    )
    raise SystemExit(1)

SUPPORTED_INPUT_SUFFIXES = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".flv",
    ".wmv",
    ".webm",
    ".m4v",
}
DEFAULT_SIMILARITY_THRESHOLD = 0.70


@dataclass(slots=True)
class CaptureStats:
    attempted: int = 0
    saved: int = 0
    skipped_similar: int = 0


@dataclass(slots=True)
class SavedFrame:
    index: int
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture frames from a video at fixed time intervals."
    )
    parser.add_argument("--input", required=True, help="Path to the local video file.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where captured frames will be stored.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=float,
        required=True,
        help="Capture interval in seconds. Must be greater than 0.",
    )
    parser.add_argument(
        "--skip-similar-frames",
        action="store_true",
        help="Skip the current frame when similarity with the previous saved frame is above the threshold.",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=DEFAULT_SIMILARITY_THRESHOLD,
        help="Similarity threshold in the range 0-1. Defaults to 0.70.",
    )
    parser.add_argument(
        "--image-extension",
        choices=("jpg", "png"),
        default="jpg",
        help="Image format for saved frames. Defaults to jpg.",
    )
    return parser.parse_args()


def fail(message: str, exit_code: int = 1) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return exit_code


def log(message: str) -> None:
    print(f"[video_frame_capture] {message}")


def validate_args(args: argparse.Namespace) -> tuple[Path, Path]:
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    if input_path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        raise ValueError(
            f"Unsupported input file type '{input_path.suffix}'. Supported types: {supported}"
        )
    if args.interval_seconds <= 0:
        raise ValueError("--interval-seconds must be greater than 0.")
    if not 0 <= args.similarity_threshold <= 1:
        raise ValueError("--similarity-threshold must be in the range 0 to 1.")

    output_dir.mkdir(parents=True, exist_ok=True)
    return input_path, output_dir


def load_cv2():
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'opencv-python-headless'. Install dependencies first, for example: "
            "pip install -r requirements.txt"
        ) from exc
    return cv2


def format_clock(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}h{minutes:02d}m{secs:02d}s"


def build_output_name(video_stem: str, timestamp_seconds: float, capture_index: int, extension: str) -> str:
    return f"{video_stem}_{format_clock(timestamp_seconds)}_{capture_index:04d}.{extension}"


def write_image(output_path: Path, frame, image_extension: str, cv2_module) -> None:
    suffix = ".jpg" if image_extension == "jpg" else ".png"
    ok, encoded = cv2_module.imencode(suffix, frame)
    if not ok:
        raise RuntimeError(f"Failed to encode frame image: {output_path}")
    output_path.write_bytes(encoded.tobytes())


def calculate_similarity(frame_a, frame_b, cv2_module) -> float:
    resize_size = (320, 180)
    frame_a_resized = cv2_module.resize(frame_a, resize_size)
    frame_b_resized = cv2_module.resize(frame_b, resize_size)
    gray_a = cv2_module.cvtColor(frame_a_resized, cv2_module.COLOR_BGR2GRAY)
    gray_b = cv2_module.cvtColor(frame_b_resized, cv2_module.COLOR_BGR2GRAY)
    diff = cv2_module.absdiff(gray_a, gray_b)
    mean_diff = float(diff.mean())
    similarity = 1.0 - (mean_diff / 255.0)
    return max(0.0, min(1.0, similarity))


def write_result_json(output_dir: Path, saved_frames: list[SavedFrame]) -> Path:
    result_path = output_dir / "result.json"
    payload = [
        {
            "file_index": frame.index,
            "file_path": str(frame.path),
        }
        for frame in saved_frames
    ]
    result_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return result_path


def capture_frames(
    input_path: Path,
    output_dir: Path,
    interval_seconds: float,
    skip_similar_frames: bool,
    similarity_threshold: float,
    image_extension: str,
) -> tuple[CaptureStats, list[SavedFrame]]:
    cv2 = load_cv2()
    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Failed to open video file: {input_path}")

    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    total_frames = float(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0)
    duration_seconds = (total_frames / fps) if fps > 0 and total_frames > 0 else 0.0
    if duration_seconds <= 0:
        capture.release()
        raise RuntimeError("Failed to read video duration from the file.")

    log(f"Input video: {input_path}")
    log(f"Output directory: {output_dir}")
    log(f"Interval seconds: {interval_seconds}")
    log(f"Skip similar frames: {skip_similar_frames}")
    if skip_similar_frames:
        log(f"Similarity threshold: {similarity_threshold:.0%}")
    log(f"Video duration: {format_clock(duration_seconds)}")

    stats = CaptureStats()
    saved_frames: list[SavedFrame] = []
    timestamp_seconds = 0.0
    previous_saved_frame = None
    video_stem = input_path.stem

    try:
        while timestamp_seconds <= duration_seconds:
            stats.attempted += 1
            progress = min(100, int((timestamp_seconds / duration_seconds) * 100))
            log(
                f"Progress {progress:3d}% | seeking {format_clock(timestamp_seconds)} "
                f"| capture #{stats.attempted}"
            )

            capture.set(cv2.CAP_PROP_POS_MSEC, timestamp_seconds * 1000)
            ok, frame = capture.read()
            if not ok or frame is None:
                log(f"Reached unreadable position at {format_clock(timestamp_seconds)}, stopping.")
                break

            if skip_similar_frames and previous_saved_frame is not None:
                similarity = calculate_similarity(previous_saved_frame, frame, cv2)
                if similarity > similarity_threshold:
                    stats.skipped_similar += 1
                    log(
                        f"Skipped {format_clock(timestamp_seconds)} because similarity "
                        f"{similarity:.2%} > {similarity_threshold:.0%}"
                    )
                    timestamp_seconds += interval_seconds
                    continue

            output_name = build_output_name(video_stem, timestamp_seconds, stats.attempted, image_extension)
            output_path = output_dir / output_name
            write_image(output_path, frame, image_extension, cv2)

            previous_saved_frame = frame
            stats.saved += 1
            saved_frames.append(SavedFrame(index=stats.saved, path=output_path))
            log(f"Saved frame: {output_path.name}")
            timestamp_seconds += interval_seconds
    finally:
        capture.release()

    log(
        f"Completed. attempted={stats.attempted}, saved={stats.saved}, "
        f"skipped_similar={stats.skipped_similar}"
    )
    return stats, saved_frames


def main() -> int:
    args = parse_args()

    try:
        input_path, output_dir = validate_args(args)
        _, saved_frames = capture_frames(
            input_path=input_path,
            output_dir=output_dir,
            interval_seconds=args.interval_seconds,
            skip_similar_frames=args.skip_similar_frames,
            similarity_threshold=args.similarity_threshold,
            image_extension=args.image_extension,
        )
        result_path = write_result_json(output_dir, saved_frames)
        log(f"Saved result manifest: {result_path}")
    except Exception as exc:
        return fail(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
