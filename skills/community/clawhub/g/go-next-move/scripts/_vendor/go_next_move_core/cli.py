from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .analysis import (
    COORDINATE_COLUMNS,
    DEFAULT_ANALYSIS_CONFIG,
    DEFAULT_VISITS,
    DEFAULT_MODEL,
    DEFAULT_SKILL_CONFIG,
    AnalysisRequest,
    analyze,
)
from .recognition_labels import (
    RecognitionLabelStore,
    changed_board_points,
    normalize_board_ascii,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Recognize or read a Go position and ask KataGo for the next move.")
    result.add_argument("source", nargs="?", help="Image path, board_ascii text file, or omitted to read board_ascii from stdin")
    result.add_argument("--input", choices=["auto", "image", "ascii"], default="auto", help="Input kind, default: auto")
    result.add_argument("--side-to-move", required=True, help="Side to move: black/B/黑 or white/W/白")
    result.add_argument("--level", default="advanced", help="Move strength: beginner/初级, intermediate/中级, advanced/高级, or all/全部")
    result.add_argument(
        "--coordinate-style",
        choices=sorted(COORDINATE_COLUMNS),
        default="gtp",
        help="Coordinate letters: gtp skips I (default); sequential includes I",
    )
    result.add_argument(
        "--move-overlay",
        action="append",
        default=[],
        help=(
            "Confirmed post-photo move as source:color:move:label, repeatable. "
            "Coordinates use --coordinate-style. "
            "Example: --move-overlay ai:W:Q4:1 --move-overlay user:B:D16:2. "
            "Captures are intentionally unsupported; re-shoot/reset when captures occur."
        ),
    )
    result.add_argument("--board-size", type=int, default=19, help="Board size, default: 19")
    result.add_argument("--komi", type=float, default=7.5, help="Komi, default: 7.5")
    result.add_argument(
        "--visits",
        type=int,
        default=DEFAULT_VISITS,
        help=f"KataGo visit budget, default: {DEFAULT_VISITS}",
    )
    result.add_argument("--top-candidates", type=int, default=20, help="Number of candidate moves to return and consider for level selection")
    result.add_argument("--warp-size", type=int, default=1200, help="Image recognition warp size")
    result.add_argument("--corners", help="Manual image board corners as 'x,y x,y x,y x,y'")
    result.add_argument("--grid-corners", action="store_true", help="Treat --corners as outer grid intersections")
    result.add_argument("--overlay", type=Path, help="Write a recognition overlay when input is an image")
    result.add_argument("--source-overlay", type=Path, help="Write a recognition overlay on the original source image")
    result.add_argument("--reject-low-confidence-recognition", action="store_true", help="Return a reviewable result instead of calling KataGo when image recognition confidence is low")
    result.add_argument("--result-image", type=Path, help="Write a clean board image with the recommended move marked")
    result.add_argument("--source-result-image", type=Path, help="Write the recommended move overlay on the original source image")
    result.add_argument("--result-size", type=int, default=1200, help="Pixel size for --result-image, default: 1200")
    result.add_argument(
        "--board-override-file",
        type=Path,
        help=(
            "Use a caller-supplied board_ascii file instead of the image detector result while "
            "retaining the source photo for rendering"
        ),
    )
    result.add_argument(
        "--recognition-label-dir",
        type=Path,
        help=(
            "Store an image/detector/override candidate-label bundle here; only valid with "
            "--board-override-file"
        ),
    )
    result.add_argument("--katago", default="katago", help="Path to katago executable")
    result.add_argument("--model", default=DEFAULT_MODEL, help="KataGo model path")
    result.add_argument("--analysis-config", default=DEFAULT_ANALYSIS_CONFIG, help="KataGo analysis config path")
    result.add_argument("--skill-config", type=Path, default=DEFAULT_SKILL_CONFIG, help="KataGo analysis override config")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    board_override: list[str] | None = None
    if args.board_override_file is not None:
        if args.input == "ascii" or not args.source:
            raise SystemExit("--board-override-file requires image input")
        try:
            board_override = normalize_board_ascii(
                args.board_override_file.read_text(encoding="utf-8").splitlines(),
                board_size=args.board_size,
            )
        except OSError as exc:
            raise SystemExit(f"Unable to read board override: {exc}") from exc
        except ValueError as exc:
            raise SystemExit(f"Invalid board override: {exc}") from exc
    elif args.recognition_label_dir is not None:
        raise SystemExit("--recognition-label-dir requires --board-override-file")
    request = AnalysisRequest(
        source=args.source,
        input_kind=args.input,
        side_to_move=args.side_to_move,
        level=args.level,
        coordinate_style=args.coordinate_style,
        move_overlays=tuple(args.move_overlay),
        board_size=args.board_size,
        komi=args.komi,
        visits=args.visits,
        top_candidates=args.top_candidates,
        warp_size=args.warp_size,
        corners=args.corners,
        grid_corners=args.grid_corners,
        recognition_overlay=args.overlay,
        source_overlay=args.source_overlay,
        reject_low_confidence_recognition=(
            args.reject_low_confidence_recognition and board_override is None
        ),
        result_image=args.result_image,
        source_result_image=args.source_result_image,
        result_size=args.result_size,
        board_override=tuple(board_override) if board_override is not None else None,
        katago=args.katago,
        model=args.model,
        analysis_config=args.analysis_config,
        engine_config=args.skill_config,
    )
    try:
        result = analyze(request)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if board_override is not None:
        recognition = result.get("recognition") or {}
        try:
            detector_rows = normalize_board_ascii(
                recognition.get("detector_board_ascii"),
                board_size=args.board_size,
            )
        except ValueError as exc:
            raise SystemExit(f"Unable to label recognition retry: {exc}") from exc
        label_dir = args.recognition_label_dir or Path(
            os.getenv(
                "GO_NEXT_MOVE_RECOGNITION_LABEL_DIR",
                str(Path.home() / ".go-next-move" / "recognition-labels"),
            )
        )
        corrected_output_value = result.get("source_result_image") or result.get("result_image")
        corrected_output = Path(corrected_output_value) if corrected_output_value else None
        detector_output = args.source_overlay if args.source_overlay and args.source_overlay.is_file() else None
        retry_metadata = {
            "entry_point": "skill",
            "source": "agent_llm",
            "status": "llm_proposed",
            "detector_board_ascii": detector_rows,
            "board_ascii": board_override,
            "changed_points": changed_board_points(
                detector_rows,
                board_override,
                coordinate_style=args.coordinate_style,
            ),
            "model": "host-agent-llm",
        }
        try:
            label_id, label_path = RecognitionLabelStore(label_dir).create(
                image_path=Path(args.source),
                detector_output_path=detector_output,
                corrected_output_path=corrected_output,
                metadata=retry_metadata,
            )
        except OSError as exc:
            raise SystemExit(f"Unable to store recognition label: {exc}") from exc
        retry_metadata["label_id"] = label_id
        retry_metadata["label_path"] = str(label_path)
        result["recognition_retry"] = retry_metadata
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
