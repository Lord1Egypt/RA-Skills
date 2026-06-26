#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import cv2
    import numpy as np
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Install with: "
        "python3 -m pip install -r scripts/requirements.txt"
    ) from exc

from go_board_recognition import GridFit, grid_to_source_point, read_image, recognize_board, render_overlay, render_source_overlay, write_image


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "/opt/homebrew/share/katago/g170e-b20c256x2-s5303129600-d1228401921.bin.gz"
DEFAULT_ANALYSIS_CONFIG = "/opt/homebrew/share/katago/configs/analysis_example.cfg"
DEFAULT_SKILL_CONFIG = Path("katago") / "analysis_skill.cfg"
GTP_COLUMNS = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
SEQUENTIAL_COLUMNS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COORDINATE_COLUMNS = {
    "gtp": GTP_COLUMNS,
    "sequential": SEQUENTIAL_COLUMNS,
}
LEVEL_ALIASES = {
    "beginner": "beginner",
    "初级": "beginner",
    "low": "beginner",
    "intermediate": "intermediate",
    "中级": "intermediate",
    "medium": "intermediate",
    "advanced": "advanced",
    "高级": "advanced",
    "high": "advanced",
    "all": "all",
    "全部": "all",
}
OVERLAY_SOURCE_ALIASES = {
    "ai": "ai",
    "assistant": "ai",
    "推荐": "ai",
    "ai推荐": "ai",
    "user": "user",
    "human": "user",
    "manual": "user",
    "人工": "user",
    "手动": "user",
}


@dataclass(frozen=True)
class MoveOverlay:
    source: str
    color: str
    move: str
    label: int


def normalize_player(raw: str) -> str:
    value = raw.strip().lower()
    if value in {"b", "black", "黑", "黑棋"}:
        return "B"
    if value in {"w", "white", "白", "白棋"}:
        return "W"
    raise SystemExit("--side-to-move must be black/B/黑 or white/W/白")


def normalize_overlay_source(raw: str) -> str:
    value = raw.strip().lower()
    if value in OVERLAY_SOURCE_ALIASES:
        return OVERLAY_SOURCE_ALIASES[value]
    raise SystemExit("Move overlay source must be ai/recommendation/推荐 or user/human/manual/人工")


def format_coord(row: int, col: int, board_size: int, coordinate_style: str) -> str:
    columns = COORDINATE_COLUMNS[coordinate_style]
    if col >= len(columns):
        raise SystemExit(
            f"Board size {board_size} is too large for the {coordinate_style} coordinate column table"
        )
    return f"{columns[col]}{board_size - row}"


def parse_coord(move: str, board_size: int, coordinate_style: str) -> tuple[int, int] | None:
    value = move.strip().upper()
    if value in {"PASS", "RESIGN"}:
        return None
    if len(value) < 2:
        raise SystemExit(f"Bad {coordinate_style} move: {move}")
    columns = COORDINATE_COLUMNS[coordinate_style]
    col = columns.find(value[0])
    if col < 0 or col >= board_size:
        raise SystemExit(f"Bad {coordinate_style} move column: {move}")
    try:
        number = int(value[1:])
    except ValueError as exc:
        raise SystemExit(f"Bad {coordinate_style} move row: {move}") from exc
    row = board_size - number
    if not 0 <= row < board_size:
        raise SystemExit(f"Bad {coordinate_style} move row: {move}")
    return row, col


def convert_coord(move: str, board_size: int, from_style: str, to_style: str) -> str:
    value = move.strip().upper()
    if value in {"PASS", "RESIGN"}:
        return value
    parsed = parse_coord(value, board_size, from_style)
    if parsed is None:
        return value
    return format_coord(*parsed, board_size, to_style)


def convert_move_info(move: dict[str, Any], board_size: int, coordinate_style: str) -> dict[str, Any]:
    converted = dict(move)
    if "move" in converted:
        converted["move"] = convert_coord(str(converted["move"]), board_size, "gtp", coordinate_style)
    if "pv" in converted:
        converted["pv"] = [
            convert_coord(str(item), board_size, "gtp", coordinate_style)
            for item in converted["pv"]
        ]
    return converted


def parse_move_overlay(raw: str, board_size: int, coordinate_style: str) -> MoveOverlay:
    parts = [part.strip() for part in raw.replace(",", ":").split(":")]
    if len(parts) != 4 or any(not part for part in parts):
        raise SystemExit(
            "--move-overlay must use source:color:move:label, "
            "for example ai:W:Q4:1 or user:B:D16:2"
        )
    source = normalize_overlay_source(parts[0])
    color = normalize_player(parts[1])
    move = parts[2].upper()
    if parse_coord(move, board_size, coordinate_style) is None:
        raise SystemExit("--move-overlay does not support PASS/RESIGN because it must draw and compose a board point")
    try:
        label = int(parts[3])
    except ValueError as exc:
        raise SystemExit("--move-overlay label must be an integer") from exc
    if label < 1:
        raise SystemExit("--move-overlay label must be at least 1")
    return MoveOverlay(source=source, color=color, move=move, label=label)


def overlay_to_json(overlay: MoveOverlay) -> dict[str, Any]:
    return {
        "source": overlay.source,
        "color": overlay.color,
        "move": overlay.move,
        "label": overlay.label,
    }


def recommendation_overlay(
    recommendation: dict[str, Any] | None,
    side_to_move: str,
    label: int,
    board_size: int,
    coordinate_style: str,
) -> MoveOverlay | None:
    move = recommendation.get("move") if recommendation else None
    if not move:
        return None
    if parse_coord(str(move), board_size, coordinate_style) is None:
        return None
    return MoveOverlay(source="ai", color=side_to_move, move=str(move).upper(), label=label)


def next_overlay_label(overlays: list[MoveOverlay]) -> int:
    if not overlays:
        return 1
    return max(overlay.label for overlay in overlays) + 1


def apply_move_overlays(
    rows: list[str],
    overlays: list[MoveOverlay],
    coordinate_style: str,
) -> list[str]:
    board = [list(row) for row in rows]
    board_size = len(rows)
    seen_labels: set[int] = set()
    for overlay in overlays:
        if overlay.label in seen_labels:
            raise SystemExit(f"Duplicate move overlay label: {overlay.label}")
        seen_labels.add(overlay.label)
        parsed = parse_coord(overlay.move, board_size, coordinate_style)
        if parsed is None:
            raise SystemExit(f"Move overlay cannot be PASS/RESIGN: {overlay.move}")
        row, col = parsed
        current = board[row][col]
        if current != ".":
            raise SystemExit(
                f"Move overlay {overlay.label} ({overlay.source}:{overlay.color}:{overlay.move}) "
                f"targets an occupied point. Re-shoot/reset the board if captures or recognition drift occurred."
            )
        board[row][col] = "X" if overlay.color == "B" else "O"
    return ["".join(row) for row in board]


def parse_board_ascii(text: str) -> list[str]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        compact = "".join(ch for ch in line if not ch.isspace())
        if compact:
            rows.append(compact)
    if not rows:
        raise SystemExit("No board_ascii rows found")
    size = len(rows)
    bad_rows = [idx + 1 for idx, row in enumerate(rows) if len(row) != size]
    if bad_rows:
        raise SystemExit(f"board_ascii must be square; bad row(s): {bad_rows}")
    allowed = set("XxBbOoWw.")
    for idx, row in enumerate(rows, start=1):
        bad = sorted(set(row) - allowed)
        if bad:
            raise SystemExit(f"Unsupported board_ascii character(s) on row {idx}: {''.join(bad)}")
    return rows


def board_ascii_to_initial_stones(rows: list[str]) -> list[list[str]]:
    size = len(rows)
    stones: list[list[str]] = []
    for row_idx, row in enumerate(rows):
        for col_idx, value in enumerate(row):
            if value in {"X", "x", "B", "b"}:
                stones.append(["B", format_coord(row_idx, col_idx, size, "gtp")])
            elif value in {"O", "o", "W", "w"}:
                stones.append(["W", format_coord(row_idx, col_idx, size, "gtp")])
    return stones


def blend_circle(image: np.ndarray, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: float) -> None:
    layer = image.copy()
    cv2.circle(layer, center, radius, color, -1, lineType=cv2.LINE_AA)
    cv2.addWeighted(layer, alpha, image, 1.0 - alpha, 0, image)


def draw_stone(image: np.ndarray, center: tuple[int, int], radius: int, color: str) -> None:
    x, y = center
    blend_circle(image, (x + max(1, radius // 10), y + max(1, radius // 10)), radius, (70, 92, 118), 0.18)
    if color in {"X", "x", "B", "b"}:
        cv2.circle(image, center, radius, (22, 22, 24), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (x - radius // 4, y - radius // 4), max(2, radius // 4), (58, 58, 62), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, radius, (5, 5, 7), 2, lineType=cv2.LINE_AA)
    else:
        cv2.circle(image, center, radius, (236, 232, 218), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (x - radius // 4, y - radius // 4), max(3, radius // 3), (255, 252, 244), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, radius, (168, 162, 148), 1, lineType=cv2.LINE_AA)


def draw_recommendation_marker(
    image: np.ndarray,
    center: tuple[int, int],
    stone_radius: int,
    side_to_move: str,
    occupied: bool,
) -> None:
    if not occupied:
        draw_stone(image, center, stone_radius, "X" if side_to_move == "B" else "O")
    marker_radius = max(7, int(stone_radius * 0.34))
    ring_radius = max(marker_radius + 6, int(stone_radius * 0.62))
    cv2.circle(image, center, ring_radius, (0, 0, 235), 4, lineType=cv2.LINE_AA)
    cv2.circle(image, center, marker_radius, (0, 0, 255), -1, lineType=cv2.LINE_AA)
    cv2.circle(image, center, max(2, marker_radius // 3), (245, 245, 245), -1, lineType=cv2.LINE_AA)


def draw_numbered_source_stone(image: np.ndarray, center: tuple[int, int], side_to_move: str, label: str = "1") -> None:
    height, width = image.shape[:2]
    stone_radius = max(18, int(round(min(height, width) / 43)))
    shadow_offset = max(2, stone_radius // 9)
    blend_circle(image, (center[0] + shadow_offset, center[1] + shadow_offset), stone_radius, (50, 60, 78), 0.20)
    try:
        label_number = int(label)
    except ValueError:
        label_number = 1
    ring_color = (255, 126, 52) if label_number % 2 == 1 else (70, 165, 92)
    cv2.circle(image, center, stone_radius + max(3, stone_radius // 7), ring_color, max(3, stone_radius // 8), lineType=cv2.LINE_AA)
    if side_to_move == "W":
        cv2.circle(image, center, stone_radius, (238, 235, 222), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (center[0] - stone_radius // 4, center[1] - stone_radius // 4), max(3, stone_radius // 3), (255, 252, 244), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, stone_radius, (140, 135, 125), 1, lineType=cv2.LINE_AA)
        text_color = (0, 0, 0)
    else:
        cv2.circle(image, center, stone_radius, (22, 22, 24), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (center[0] - stone_radius // 4, center[1] - stone_radius // 4), max(2, stone_radius // 4), (58, 58, 62), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, stone_radius, (5, 5, 7), 2, lineType=cv2.LINE_AA)
        text_color = (255, 255, 255)
    font_scale = max(1.0, min(height, width) / 1150.0)
    thickness = max(3, int(round(min(height, width) / 360.0)))
    (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    origin = (center[0] - text_w // 2, center[1] + (text_h - baseline) // 2)
    cv2.putText(image, label, origin, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness, lineType=cv2.LINE_AA)


def render_source_recommendation_image(
    image: np.ndarray,
    rows: list[str],
    move_overlays: list[MoveOverlay],
    corners: list[list[float]],
    xfit: GridFit,
    yfit: GridFit,
    warp_size: int,
    coordinate_style: str,
) -> np.ndarray:
    board = [["B" if value in {"X", "x", "B", "b"} else "W" if value in {"O", "o", "W", "w"} else "." for value in row] for row in rows]
    overlay = render_source_overlay(image, corners, board, xfit, yfit, warp_size)
    for move_overlay in sorted(move_overlays, key=lambda item: item.label):
        parsed = parse_coord(move_overlay.move, len(rows), coordinate_style)
        if parsed is None:
            continue
        row, col = parsed
        point = grid_to_source_point(row, col, corners, xfit, yfit, warp_size)
        center = (int(round(float(point[0]))), int(round(float(point[1]))))
        draw_numbered_source_stone(overlay, center, move_overlay.color, str(move_overlay.label))
    return overlay


def default_source_result_path() -> Path:
    return Path(tempfile.gettempdir()) / f"go-next-move-source-result-{uuid.uuid4().hex}.jpg"


def render_recommendation_board(
    rows: list[str],
    move_overlays: list[MoveOverlay],
    output_size: int,
    coordinate_style: str,
) -> np.ndarray:
    board_size = len(rows)
    image = np.full((output_size, output_size, 3), (94, 166, 214), dtype=np.uint8)
    y = np.arange(output_size, dtype=np.float32)[:, None]
    x = np.arange(output_size, dtype=np.float32)[None, :]
    grain = 5.0 * np.sin(x / 6.0) + 3.0 * np.sin(x / 19.0) + 1.5 * np.sin((x + y) / 31.0)
    image = np.clip(image.astype(np.float32) + grain[..., None], 0, 255).astype(np.uint8)

    pad = int(round(output_size * 0.06))
    cell = (output_size - 2 * pad) / float(board_size - 1)
    line_color = (38, 43, 52)
    border_color = (53, 72, 102)
    cv2.rectangle(image, (8, 8), (output_size - 9, output_size - 9), border_color, max(4, output_size // 210), lineType=cv2.LINE_AA)
    for idx in range(board_size):
        pos = int(round(pad + idx * cell))
        thickness = 2 if idx in {0, board_size - 1} else 1
        cv2.line(image, (pad, pos), (output_size - pad, pos), line_color, thickness, lineType=cv2.LINE_AA)
        cv2.line(image, (pos, pad), (pos, output_size - pad), line_color, thickness, lineType=cv2.LINE_AA)

    if board_size == 19:
        star_radius = max(3, int(round(cell * 0.06)))
        for row in (3, 9, 15):
            for col in (3, 9, 15):
                center = (int(round(pad + col * cell)), int(round(pad + row * cell)))
                cv2.circle(image, center, star_radius, (13, 18, 25), -1, lineType=cv2.LINE_AA)

    stone_radius = max(8, int(round(cell * 0.43)))
    for row_idx, row in enumerate(rows):
        for col_idx, value in enumerate(row):
            if value not in {"X", "x", "B", "b", "O", "o", "W", "w"}:
                continue
            center = (int(round(pad + col_idx * cell)), int(round(pad + row_idx * cell)))
            draw_stone(image, center, stone_radius, value)

    for move_overlay in sorted(move_overlays, key=lambda item: item.label):
        parsed = parse_coord(move_overlay.move, board_size, coordinate_style)
        if parsed is None:
            continue
        row_idx, col_idx = parsed
        center = (int(round(pad + col_idx * cell)), int(round(pad + row_idx * cell)))
        draw_numbered_source_stone(image, center, move_overlay.color, str(move_overlay.label))
    return image


def load_board_source(args: argparse.Namespace) -> tuple[list[str], dict[str, Any] | None, dict[str, Any] | None]:
    source = Path(args.source) if args.source else None
    input_kind = args.input
    if input_kind == "auto":
        if source and source.exists() and source.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}:
            input_kind = "image"
        else:
            input_kind = "ascii"

    if input_kind == "image":
        if source is None:
            raise SystemExit("Image input requires a source image path")
        recognition, warped, board, xfit, yfit = recognize_board(
            source,
            board_size=args.board_size,
            warp_size=args.warp_size,
            corners=args.corners,
            grid_corners=args.grid_corners,
        )
        if args.overlay:
            write_image(args.overlay, render_overlay(warped, board, xfit, yfit))
            recognition["overlay"] = str(args.overlay)
        if args.source_overlay:
            source_overlay = render_source_overlay(read_image(source), recognition["board_corners"], board, xfit, yfit, args.warp_size)
            write_image(args.source_overlay, source_overlay)
            recognition["source_overlay"] = str(args.source_overlay)
        image_context = {
            "source": source,
            "board": board,
            "xfit": xfit,
            "yfit": yfit,
        }
        return list(recognition["board_ascii"]), recognition, image_context

    if source:
        text = source.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    return parse_board_ascii(text), None, None


def run_katago_analysis(
    rows: list[str],
    side_to_move: str,
    komi: float,
    visits: int,
    katago: str,
    model: str,
    config: str,
    skill_config: Path,
) -> dict[str, Any]:
    skill_config_arg = str(skill_config)
    if skill_config.is_absolute():
        try:
            skill_config_arg = str(skill_config.relative_to(REPO_ROOT))
        except ValueError:
            raise SystemExit("KataGo analysis does not accept an absolute project override config path; pass a path relative to this project")

    query = {
        "id": f"go-next-move-{uuid.uuid4().hex}",
        "initialStones": board_ascii_to_initial_stones(rows),
        "initialPlayer": side_to_move,
        "moves": [],
        "rules": "chinese",
        "komi": komi,
        "boardXSize": len(rows),
        "boardYSize": len(rows),
        "analyzeTurns": [0],
        "maxVisits": visits,
        "includePVVisits": True,
        "analysisPVLen": 8,
    }
    command = [
        katago,
        "analysis",
        "-model",
        model,
        "-config",
        config,
        "-config",
        skill_config_arg,
    ]
    proc = subprocess.run(
        command,
        input=json.dumps(query, ensure_ascii=False) + "\n",
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
        timeout=max(30, int(visits / 20) + 25),
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(
            "KataGo analysis failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stderr:\n{proc.stderr.strip()}"
        )

    final_response = None
    warnings = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "error" in payload:
            raise SystemExit(f"KataGo returned an error: {payload['error']}")
        if "warning" in payload:
            warnings.append(payload["warning"])
            continue
        if payload.get("id") == query["id"] and payload.get("isDuringSearch") is False:
            final_response = payload

    if final_response is None:
        raise SystemExit(f"KataGo returned no final analysis response. stderr:\n{proc.stderr.strip()}")
    if warnings:
        final_response.setdefault("warnings", []).extend(warnings)
    return final_response


def slim_move_info(move: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "move",
        "order",
        "visits",
        "edgeVisits",
        "winrate",
        "scoreLead",
        "scoreMean",
        "scoreStdev",
        "prior",
        "lcb",
        "utility",
        "pv",
        "pvVisits",
        "pvEdgeVisits",
    ]
    return {key: move[key] for key in keys if key in move}


def normalize_level(raw: str) -> str:
    value = raw.strip().lower()
    if value in LEVEL_ALIASES:
        return LEVEL_ALIASES[value]
    raise SystemExit("--level must be beginner/初级, intermediate/中级, advanced/高级, or all/全部")


def score_loss(best: dict[str, Any], move: dict[str, Any]) -> float | None:
    if "scoreLead" not in best or "scoreLead" not in move:
        return None
    return max(0.0, float(best["scoreLead"]) - float(move["scoreLead"]))


def winrate_loss(best: dict[str, Any], move: dict[str, Any]) -> float | None:
    if "winrate" not in best or "winrate" not in move:
        return None
    return max(0.0, float(best["winrate"]) - float(move["winrate"]))


def percent(value: Any) -> str | None:
    if value is None:
        return None
    return f"{float(value) * 100:.1f}%"


def points(value: Any) -> str | None:
    if value is None:
        return None
    return f"{float(value):+.1f}"


def rounded_float(value: Any, digits: int = 4) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return None


def side_name(side_to_move: str) -> str:
    return "白棋" if side_to_move == "W" else "黑棋"


def candidate_snapshot(
    candidate: dict[str, Any],
    best: dict[str, Any] | None = None,
    recommendation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = {
        "move": candidate.get("move"),
        "order": candidate.get("order"),
        "visits": candidate.get("visits"),
        "winrate": rounded_float(candidate.get("winrate")),
        "winrate_percent": percent(candidate.get("winrate")),
        "scoreLead": rounded_float(candidate.get("scoreLead"), 3),
        "score_lead_points": points(candidate.get("scoreLead")),
        "scoreStdev": rounded_float(candidate.get("scoreStdev"), 3),
        "prior": rounded_float(candidate.get("prior")),
        "lcb": rounded_float(candidate.get("lcb")),
        "utility": rounded_float(candidate.get("utility")),
        "pv": candidate.get("pv", []),
    }
    if best is not None:
        loss = score_loss(best, candidate)
        wr_loss = winrate_loss(best, candidate)
        if loss is not None:
            item["score_loss_vs_best"] = round(loss, 3)
        if wr_loss is not None:
            item["winrate_loss_vs_best"] = round(wr_loss, 4)
            item["winrate_loss_vs_best_percent"] = percent(wr_loss)
    if recommendation is not None and candidate.get("move") != recommendation.get("move"):
        rec_score = score_loss(recommendation, candidate)
        rec_wr = winrate_loss(recommendation, candidate)
        if rec_score is not None:
            item["score_loss_vs_recommendation"] = round(rec_score, 3)
        if rec_wr is not None:
            item["winrate_loss_vs_recommendation"] = round(rec_wr, 4)
            item["winrate_loss_vs_recommendation_percent"] = percent(rec_wr)
    return {key: value for key, value in item.items() if value is not None}


def level_description(requested_level: str) -> str:
    if requested_level == "advanced":
        return "高级强度：直接采用 KataGo 当前搜索排序第一的候选手。"
    if requested_level == "intermediate":
        return "中级强度：优先选择接近最优、但不一定是第一推荐的稳健候选手。"
    if requested_level == "beginner":
        return "初级强度：选择仍可下、但相对最强手有一定损失的温和候选手。"
    return "全部级别：`recommendation` 使用高级强度，三档结果见 `recommendations_by_level`。"


def move_reason(
    recommendation: dict[str, Any] | None,
    candidates: list[dict[str, Any]],
    root_info: dict[str, Any],
    side_to_move: str,
    requested_level: str,
    recognition: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not recommendation:
        return None

    move = str(recommendation.get("move", "unknown"))
    visits = recommendation.get("visits")
    winrate = percent(recommendation.get("winrate"))
    score_lead = points(recommendation.get("scoreLead"))
    pv = recommendation.get("pv", [])
    selection_reason = recommendation.get("selection_reason")
    best = candidates[0] if candidates else recommendation
    best_move = best.get("move")
    score_loss_vs_best = score_loss(best, recommendation)
    winrate_loss_vs_best = winrate_loss(best, recommendation)

    summary_parts = [f"建议{side_name(side_to_move)}走 {move}。"]
    summary_parts.append(level_description(requested_level))
    if visits is not None:
        summary_parts.append(f"该手获得 {visits} 次访问。")
    if winrate is not None or score_lead is not None:
        eval_bits = []
        if winrate is not None:
            eval_bits.append(f"胜率 {winrate}")
        if score_lead is not None:
            eval_bits.append(f"目差 {score_lead}")
        summary_parts.append("KataGo 对该手的评估为：" + "，".join(eval_bits) + "。")
    if best_move and best_move != move:
        loss_bits = []
        if score_loss_vs_best is not None:
            loss_bits.append(f"相对搜索第一候选 {best_move} 的目差损失约 {score_loss_vs_best:.1f} 目")
        if winrate_loss_vs_best is not None:
            loss_bits.append(f"胜率差 {float(winrate_loss_vs_best) * 100:.1f} 个百分点")
        if loss_bits:
            summary_parts.append("强度取舍：" + "，".join(loss_bits) + "。")
    if pv:
        summary_parts.append("主变化参考：" + " -> ".join(str(item) for item in pv[:6]) + "。")

    explanation = [
        f"选择依据：{level_description(requested_level)}",
    ]
    if selection_reason:
        explanation.append(f"分级策略说明：{selection_reason}")
    if visits is not None:
        explanation.append(f"搜索置信度：KataGo 在该候选手上投入了 {visits} 次访问，访问数越高通常表示引擎越重视这条变化。")
    if winrate is not None or score_lead is not None:
        eval_text = []
        if winrate is not None:
            eval_text.append(f"胜率 {winrate}")
        if score_lead is not None:
            eval_text.append(f"预估目差 {score_lead}")
        explanation.append("局面评估：" + "，".join(eval_text) + "。")
    if pv:
        explanation.append("后续思路：主变化显示引擎预期双方可能按 " + " -> ".join(str(item) for item in pv[:6]) + " 展开。")
    if best_move == move:
        explanation.append("候选手对比：该手就是当前搜索排序第一的最强候选。")
    elif best_move:
        comparison_text = [f"搜索排序第一候选是 {best_move}"]
        if score_loss_vs_best is not None:
            comparison_text.append(f"本手相对它的目差损失约 {score_loss_vs_best:.1f} 目")
        if winrate_loss_vs_best is not None:
            comparison_text.append(f"胜率差 {float(winrate_loss_vs_best) * 100:.1f} 个百分点")
        explanation.append("候选手对比：" + "，".join(comparison_text) + "。")

    comparisons = []
    for candidate in candidates[:5]:
        if candidate.get("move") == recommendation.get("move"):
            continue
        comparisons.append(candidate_snapshot(candidate, best, recommendation))

    caveats = []
    if recognition is not None:
        warnings = recognition.get("warnings") or []
        if warnings:
            caveats.extend(str(warning) for warning in warnings)
        caveats.append("推荐基于识别出的 board_ascii；如果结果图和真实棋盘不一致，应先修正识别再采纳下一手。")

    return {
        "summary": "".join(summary_parts),
        "explanation": explanation,
        "selection_reason": selection_reason,
        "main_variation": pv,
        "technical_parameters": {
            "engine": "KataGo",
            "rules": "Chinese",
            "side_to_move": side_to_move,
            "root": {
                "visits": root_info.get("visits"),
                "winrate": rounded_float(root_info.get("winrate")),
                "winrate_percent": percent(root_info.get("winrate")),
                "scoreLead": rounded_float(root_info.get("scoreLead"), 3),
                "score_lead_points": points(root_info.get("scoreLead")),
            },
            "recommended_move": candidate_snapshot(recommendation, best),
            "top_search_move": candidate_snapshot(best, best) if best else None,
            "best_move": candidate_snapshot(best, best) if best else None,
        },
        "root_evaluation": {
            "visits": root_info.get("visits"),
            "winrate": root_info.get("winrate"),
            "scoreLead": root_info.get("scoreLead"),
        },
        "recommended_evaluation": {
            "visits": visits,
            "winrate": recommendation.get("winrate"),
            "scoreLead": recommendation.get("scoreLead"),
            "scoreStdev": recommendation.get("scoreStdev"),
        },
        "comparison_candidates": comparisons,
        "caveats": caveats,
    }


def annotate_strength(best: dict[str, Any], move: dict[str, Any], level: str, reason: str) -> dict[str, Any]:
    annotated = dict(move)
    loss = score_loss(best, move)
    wr_loss = winrate_loss(best, move)
    annotated["strength_level"] = level
    annotated["selection_reason"] = reason
    if loss is not None:
        annotated["score_loss_vs_best"] = round(loss, 3)
    if wr_loss is not None:
        annotated["winrate_loss_vs_best"] = round(wr_loss, 4)
    return annotated


def choose_by_window(
    best: dict[str, Any],
    moves: list[dict[str, Any]],
    *,
    min_order: int,
    min_score_loss: float,
    max_score_loss: float,
    max_winrate_loss: float,
) -> dict[str, Any] | None:
    for move in moves:
        if int(move.get("order", 999999)) < min_order:
            continue
        loss = score_loss(best, move)
        wr_loss = winrate_loss(best, move)
        if loss is None or wr_loss is None:
            continue
        if min_score_loss <= loss <= max_score_loss and wr_loss <= max_winrate_loss:
            return move
    return None


def choose_fallback(
    best: dict[str, Any],
    moves: list[dict[str, Any]],
    *,
    min_order: int,
    max_score_loss: float,
    max_winrate_loss: float,
) -> dict[str, Any]:
    for move in moves:
        if int(move.get("order", 999999)) < min_order:
            continue
        loss = score_loss(best, move)
        wr_loss = winrate_loss(best, move)
        if loss is None or wr_loss is None:
            return move
        if loss <= max_score_loss and wr_loss <= max_winrate_loss:
            return move
    return best


def recommendations_by_level(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any] | None]:
    if not candidates:
        return {"beginner": None, "intermediate": None, "advanced": None}

    best = candidates[0]
    intermediate = choose_by_window(
        best,
        candidates,
        min_order=1,
        min_score_loss=0.8,
        max_score_loss=4.0,
        max_winrate_loss=0.12,
    )
    if intermediate is None:
        intermediate = choose_fallback(best, candidates, min_order=1, max_score_loss=5.0, max_winrate_loss=0.15)

    beginner = choose_by_window(
        best,
        candidates,
        min_order=3,
        min_score_loss=3.0,
        max_score_loss=12.0,
        max_winrate_loss=0.25,
    )
    if beginner is None:
        beginner = choose_fallback(best, candidates, min_order=2, max_score_loss=15.0, max_winrate_loss=0.30)

    return {
        "beginner": annotate_strength(
            best,
            beginner,
            "beginner",
            "选择一个仍可下、但低于顶部变化的候选手，用来降低落子强度。",
        ),
        "intermediate": annotate_strength(
            best,
            intermediate,
            "intermediate",
            "选择接近顶部变化的稳健候选手，但不一定采用 KataGo 搜索排序第一手。",
        ),
        "advanced": annotate_strength(
            best,
            best,
            "advanced",
            "采用 KataGo 当前搜索排序第一的候选手。",
        ),
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    side_to_move = normalize_player(args.side_to_move)
    level = normalize_level(args.level)
    coordinate_style = getattr(args, "coordinate_style", "gtp")
    base_rows, recognition, image_context = load_board_source(args)
    if len(base_rows) != args.board_size:
        raise SystemExit(f"Expected {args.board_size} board rows, got {len(base_rows)}")

    confirmed_overlays = [
        parse_move_overlay(raw, len(base_rows), coordinate_style)
        for raw in args.move_overlay
    ]
    rows = apply_move_overlays(base_rows, confirmed_overlays, coordinate_style)

    analysis = run_katago_analysis(
        rows,
        side_to_move,
        komi=args.komi,
        visits=args.visits,
        katago=args.katago,
        model=args.model,
        config=args.analysis_config,
        skill_config=args.skill_config,
    )
    move_infos = sorted(analysis.get("moveInfos", []), key=lambda item: item.get("order", 999999))
    candidates = [
        slim_move_info(convert_move_info(move, len(rows), coordinate_style))
        for move in move_infos[: args.top_candidates]
    ]
    by_level = recommendations_by_level(candidates)
    selected = by_level["advanced"] if level == "all" else by_level[level]
    root_info = analysis.get("rootInfo", {})
    reason = move_reason(selected, candidates, root_info, side_to_move, level, recognition)
    next_recommendation_overlay = recommendation_overlay(
        selected,
        side_to_move,
        next_overlay_label(confirmed_overlays),
        len(rows),
        coordinate_style,
    )
    display_overlays = list(confirmed_overlays)
    if next_recommendation_overlay is not None:
        display_overlays.append(next_recommendation_overlay)
    result = {
        "board_size": len(rows),
        "coordinate_style": coordinate_style,
        "side_to_move": side_to_move,
        "requested_level": level,
        "rules": "chinese",
        "komi": args.komi,
        "visits_requested": args.visits,
        "base_board_ascii": base_rows,
        "move_overlays": [overlay_to_json(overlay) for overlay in confirmed_overlays],
        "display_move_overlays": [overlay_to_json(overlay) for overlay in display_overlays],
        "board_ascii": rows,
        "recommendation": selected,
        "reason": reason,
        "recommendations_by_level": by_level,
        "candidate_moves": candidates,
        "root_info": root_info,
        "katago_warnings": analysis.get("warnings", []),
        "level_policy": {
            "beginner": "Choose a plausible lower-ranked move with a moderate score/winrate loss when available.",
            "intermediate": "Choose a solid near-top candidate with a small score/winrate loss when available.",
            "advanced": "Choose KataGo's top searched candidate.",
        },
    }
    if recognition is not None:
        result["recognition"] = recognition
    if args.result_image:
        result_image = render_recommendation_board(
            base_rows,
            display_overlays,
            args.result_size,
            coordinate_style,
        )
        write_image(args.result_image, result_image)
        result["result_image"] = str(args.result_image)
    source_result_path = args.source_result_image
    if recognition is not None and image_context is not None and source_result_path is None:
        source_result_path = default_source_result_path()
    if source_result_path:
        if recognition is None or image_context is None:
            raise SystemExit("--source-result-image requires image input")
        source_result = render_source_recommendation_image(
            read_image(image_context["source"]),
            base_rows,
            display_overlays,
            recognition["board_corners"],
            image_context["xfit"],
            image_context["yfit"],
            args.warp_size,
            coordinate_style,
        )
        write_image(source_result_path, source_result)
        result["source_result_image"] = str(source_result_path)
        if args.result_image is None:
            result["result_image"] = str(source_result_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Recognize or read a Go position and ask KataGo for the next move.")
    parser.add_argument("source", nargs="?", help="Image path, board_ascii text file, or omitted to read board_ascii from stdin")
    parser.add_argument("--input", choices=["auto", "image", "ascii"], default="auto", help="Input kind, default: auto")
    parser.add_argument("--side-to-move", required=True, help="Side to move: black/B/黑 or white/W/白")
    parser.add_argument("--level", default="advanced", help="Move strength: beginner/初级, intermediate/中级, advanced/高级, or all/全部")
    parser.add_argument(
        "--coordinate-style",
        choices=sorted(COORDINATE_COLUMNS),
        default="gtp",
        help="Coordinate letters: gtp skips I (default); sequential includes I",
    )
    parser.add_argument(
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
    parser.add_argument("--board-size", type=int, default=19, help="Board size, default: 19")
    parser.add_argument("--komi", type=float, default=7.5, help="Komi, default: 7.5")
    parser.add_argument("--visits", type=int, default=400, help="KataGo visit budget, default: 400")
    parser.add_argument("--top-candidates", type=int, default=20, help="Number of candidate moves to return and consider for level selection")
    parser.add_argument("--warp-size", type=int, default=1200, help="Image recognition warp size")
    parser.add_argument("--corners", help="Manual image board corners as 'x,y x,y x,y x,y'")
    parser.add_argument("--grid-corners", action="store_true", help="Treat --corners as outer grid intersections")
    parser.add_argument("--overlay", type=Path, help="Write a recognition overlay when input is an image")
    parser.add_argument("--source-overlay", type=Path, help="Write a recognition overlay on the original source image")
    parser.add_argument("--result-image", type=Path, help="Write a clean board image with the recommended move marked")
    parser.add_argument("--source-result-image", type=Path, help="Write the recommended move overlay on the original source image")
    parser.add_argument("--result-size", type=int, default=1200, help="Pixel size for --result-image, default: 1200")
    parser.add_argument("--katago", default="katago", help="Path to katago executable")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="KataGo model path")
    parser.add_argument("--analysis-config", default=DEFAULT_ANALYSIS_CONFIG, help="KataGo analysis config path")
    parser.add_argument("--skill-config", type=Path, default=DEFAULT_SKILL_CONFIG, help="Project analysis override config")
    args = parser.parse_args()

    if args.visits < 1:
        raise SystemExit("--visits must be at least 1")
    if args.top_candidates < 1:
        raise SystemExit("--top-candidates must be at least 1")
    if args.result_size < 320:
        raise SystemExit("--result-size must be at least 320")
    print(json.dumps(build_result(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
