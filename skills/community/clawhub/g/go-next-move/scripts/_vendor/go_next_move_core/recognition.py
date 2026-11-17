from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Install with: "
        "python3 -m pip install -r requirements.txt"
    ) from exc

from . import board_profiles


@dataclass
class GridFit:
    offset: float
    spacing: float
    score: float
    coverage: int
    candidates: int


WOOD_BOARD_PROFILE = board_profiles.WOOD_BOARD_PROFILE
WHITE_BOARD_PROFILE = board_profiles.WHITE_BOARD_PROFILE
DENSE_BOARD_MIN_STONES = 100
DENSE_BOARD_MIN_CIRCLES = 40


def read_image(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"Could not read image: {path}")
    return image


def write_image(path: Path, image: np.ndarray) -> None:
    ext = path.suffix or ".jpg"
    ok, encoded = cv2.imencode(ext, image)
    if not ok:
        raise SystemExit(f"Could not encode image as {ext}")
    encoded.tofile(str(path))


def parse_corners(raw: str) -> np.ndarray:
    parts = raw.replace(";", " ").split()
    if len(parts) != 4:
        raise SystemExit("--corners expects four points, e.g. '74,76 1100,53 1118,1031 72,1034'")
    points = []
    for part in parts:
        xy = part.split(",")
        if len(xy) != 2:
            raise SystemExit(f"Bad corner point: {part}")
        points.append([float(xy[0]), float(xy[1])])
    return np.array(points, dtype=np.float32)


def order_points(points: np.ndarray) -> np.ndarray:
    pts = np.array(points, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).reshape(-1)
    ordered = np.zeros((4, 2), dtype=np.float32)
    ordered[0] = pts[np.argmin(s)]
    ordered[2] = pts[np.argmax(s)]
    ordered[1] = pts[np.argmin(d)]
    ordered[3] = pts[np.argmax(d)]
    return ordered


def side_lengths(points: np.ndarray) -> tuple[float, float, float, float]:
    pts = order_points(points)
    return tuple(float(np.linalg.norm(pts[(i + 1) % 4] - pts[i])) for i in range(4))


def candidate_score(points: np.ndarray, area: float, image_area: float) -> float:
    lengths = side_lengths(points)
    width = (lengths[0] + lengths[2]) / 2.0
    height = (lengths[1] + lengths[3]) / 2.0
    if width <= 1 or height <= 1:
        return -1.0
    square_score = math.exp(-abs(math.log(width / height)) * 2.2)
    area_score = min(area / image_area, 1.0)
    return area_score * square_score


def detect_board_candidates(image: np.ndarray) -> list[np.ndarray]:
    height, width = image.shape[:2]
    image_area = float(height * width)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ranges = [
        ((8, 35, 55), (38, 240, 250)),
        ((10, 45, 65), (35, 230, 245)),
        ((5, 25, 45), (45, 255, 255)),
        ((0, 20, 45), (55, 255, 255)),
    ]
    ksize = max(9, int(max(height, width) / 45))
    if ksize % 2 == 0:
        ksize += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    candidates: list[tuple[float, np.ndarray]] = []

    for low, high in ranges:
        mask = cv2.inRange(hsv, np.array(low, dtype=np.uint8), np.array(high, dtype=np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:8]:
            area = float(cv2.contourArea(contour))
            if area < image_area * 0.12:
                continue
            perimeter = cv2.arcLength(contour, True)
            point_sets = []
            for eps in (0.02, 0.04, 0.06):
                approx = cv2.approxPolyDP(contour, eps * perimeter, True)
                if len(approx) == 4:
                    point_sets.append(approx.reshape(4, 2).astype(np.float32))
            point_sets.append(cv2.boxPoints(cv2.minAreaRect(contour)).astype(np.float32))

            for points in point_sets:
                score = candidate_score(points, area, image_area)
                if score > 0:
                    candidates.append((score, order_points(points)))

    candidates.extend(detect_dark_grid_board_candidates(image))
    candidates.sort(key=lambda item: item[0], reverse=True)
    unique: list[np.ndarray] = []
    for _, points in candidates:
        if all(np.max(np.abs(points - existing)) > 12 for existing in unique):
            unique.append(points)
        if len(unique) >= 8:
            break
    return unique


def detect_dark_grid_board_candidates(image: np.ndarray) -> list[tuple[float, np.ndarray]]:
    height, width = image.shape[:2]
    image_area = float(height * width)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    candidates: list[tuple[float, np.ndarray]] = []
    attempts = (
        (51, 7, 15),
        (71, 9, 15),
        (101, 9, 25),
        (151, 11, 15),
    )

    for block_size, adaptive_c, kernel_len in attempts:
        if block_size % 2 == 0:
            block_size += 1
        dark = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            block_size,
            adaptive_c,
        )
        horizontal = cv2.morphologyEx(
            dark,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 2)),
        )
        vertical = cv2.morphologyEx(
            dark,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_RECT, (2, kernel_len)),
        )
        lines = cv2.bitwise_or(horizontal, vertical)
        close_len = max(9, kernel_len // 2)
        connected = cv2.morphologyEx(
            lines,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_RECT, (close_len, close_len)),
        )
        contours, _ = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:
            area = float(cv2.contourArea(contour))
            if area < image_area * 0.10:
                continue
            perimeter = cv2.arcLength(contour, True)
            point_sets = []
            for eps in (0.015, 0.025, 0.04):
                approx = cv2.approxPolyDP(contour, eps * perimeter, True)
                if len(approx) == 4:
                    point_sets.append(approx.reshape(4, 2).astype(np.float32))
            point_sets.append(cv2.boxPoints(cv2.minAreaRect(contour)).astype(np.float32))

            for points in point_sets:
                score = candidate_score(points, area, image_area)
                if score > 0.06:
                    candidates.append((score, order_points(points)))
    return candidates


def warp_board(image: np.ndarray, corners: np.ndarray, size: int) -> np.ndarray:
    dst = np.array([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]], dtype=np.float32)
    transform = cv2.getPerspectiveTransform(order_points(corners), dst)
    return cv2.warpPerspective(image, transform, (size, size))


def cluster_positions(items: list[tuple[float, float]], tolerance: float) -> list[tuple[float, float]]:
    if not items:
        return []
    clusters: list[list[tuple[float, float]]] = []
    for value, weight in sorted(items):
        if not clusters or value - clusters[-1][-1][0] > tolerance:
            clusters.append([(value, weight)])
        else:
            clusters[-1].append((value, weight))

    merged = []
    for cluster in clusters:
        total_weight = sum(weight for _, weight in cluster)
        if total_weight > 0:
            merged.append((sum(value * weight for value, weight in cluster) / total_weight, total_weight))
    return merged


def projection_peaks(mask: np.ndarray, axis: int, percentile: float = 93.0) -> list[tuple[float, float]]:
    projection = mask.mean(axis=axis)
    if projection.size < 16:
        return []
    smooth = np.convolve(projection, np.ones(7) / 7.0, mode="same")
    threshold = float(np.percentile(smooth, percentile))
    if threshold <= 0:
        return []
    peaks = []
    for idx in range(4, len(smooth) - 4):
        window = smooth[idx - 4 : idx + 5]
        if smooth[idx] >= threshold and smooth[idx] >= window.max():
            peaks.append((float(idx), float(max(smooth[idx], 1.0)) / 255.0))
    return cluster_positions(peaks, 12.0)


def collect_line_candidates(warped: np.ndarray, axis: str) -> list[tuple[float, float]]:
    size = warped.shape[0]
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    candidates: list[tuple[float, float]] = []

    edges = cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 50, 120, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=max(55, int(size * 0.055)),
        minLineLength=max(140, int(size * 0.18)),
        maxLineGap=max(16, int(size * 0.035)),
    )
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0, :]:
            dx = float(x2 - x1)
            dy = float(y2 - y1)
            length = math.hypot(dx, dy)
            if length < size * 0.18:
                continue
            angle = abs(math.degrees(math.atan2(dy, dx)))
            if axis == "x" and 84 <= angle <= 96:
                candidates.append(((x1 + x2) / 2.0, 1.0 + length / size))
            elif axis == "y" and (angle <= 6 or angle >= 174):
                candidates.append(((y1 + y2) / 2.0, 1.0 + length / size))

    block_size = max(31, int(size / 20))
    if block_size % 2 == 0:
        block_size += 1
    dark = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size, 7)
    kernel_len = max(35, int(size / 18))
    if axis == "x":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, kernel_len))
        candidates.extend(projection_peaks(cv2.morphologyEx(dark, cv2.MORPH_OPEN, kernel), axis=0))
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 2))
        candidates.extend(projection_peaks(cv2.morphologyEx(dark, cv2.MORPH_OPEN, kernel), axis=1))
    return cluster_positions(candidates, tolerance=max(8.0, size / 120.0))


def fit_regular_grid(candidates: list[tuple[float, float]], board_size: int, image_size: int) -> GridFit:
    nominal = image_size / float(board_size - 1)
    if not candidates:
        margin = image_size * 0.045
        return GridFit(margin, (image_size - 2 * margin) / float(board_size - 1), 0.0, 0, 0)

    values = np.array([value for value, _ in candidates], dtype=np.float64)
    weights = np.clip(np.array([weight for _, weight in candidates], dtype=np.float64), 0.25, 6.0)
    best: tuple[float, float, float, int] | None = None

    def evaluate(spacing_values: np.ndarray, offset_values_for_spacing: int | np.ndarray) -> None:
        nonlocal best
        for spacing in spacing_values:
            max_offset = image_size - 1 - (board_size - 1) * spacing
            if max_offset < 0:
                continue
            if isinstance(offset_values_for_spacing, np.ndarray):
                offsets = offset_values_for_spacing
            else:
                offsets = np.linspace(0, min(max_offset, image_size * 0.16), offset_values_for_spacing)
            tolerance = max(4.5, spacing * 0.095)
            grid_base = np.arange(board_size) * spacing
            for offset in offsets:
                if offset < 0 or offset > max_offset:
                    continue
                grid = offset + grid_base
                distances = np.min(np.abs(values[:, None] - grid[None, :]), axis=1)
                nearest = np.argmin(np.abs(values[:, None] - grid[None, :]), axis=1)
                weighted = float(np.sum(weights * np.exp(-((distances / tolerance) ** 2))))
                coverage = len(set(int(v) for v in nearest[distances < tolerance * 1.2]))
                score = weighted + coverage * 1.8
                if best is None or score > best[0]:
                    best = (score, float(offset), float(spacing), coverage)

    evaluate(np.linspace(nominal * 0.78, nominal * 1.02, 72), 72)
    if best is not None:
        _, best_offset, best_spacing, _ = best
        spacing_step = nominal * 0.24 / 71.0
        offset_limit = image_size * 0.16
        spacing_values = np.linspace(best_spacing - spacing_step * 2.0, best_spacing + spacing_step * 2.0, 36)
        offset_values = np.linspace(
            max(0.0, best_offset - spacing_step * 2.0),
            min(offset_limit, best_offset + spacing_step * 2.0),
            36,
        )
        evaluate(spacing_values, offset_values)

    if best is None:
        margin = image_size * 0.045
        return GridFit(margin, (image_size - 2 * margin) / float(board_size - 1), 0.0, 0, len(candidates))
    score, offset, spacing, coverage = best
    return GridFit(offset, spacing, score, coverage, len(candidates))

def detect_grid(warped: np.ndarray, board_size: int) -> tuple[GridFit, GridFit]:
    size = warped.shape[0]
    return (
        fit_regular_grid(collect_line_candidates(warped, "x"), board_size, size),
        fit_regular_grid(collect_line_candidates(warped, "y"), board_size, size),
    )


def detect_stone_circles(warped: np.ndarray, board_size: int) -> np.ndarray:
    """Return circle candidates used to stabilize dense-board grid fitting."""
    size = warped.shape[0]
    nominal_spacing = size / float(board_size - 1)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    blur_size = max(5, int(round(size / 240.0)))
    if blur_size % 2 == 0:
        blur_size += 1
    gray = cv2.GaussianBlur(gray, (blur_size, blur_size), 1.2)
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.25,
        minDist=max(12.0, nominal_spacing * 0.51),
        param1=100,
        param2=max(18.0, nominal_spacing * 0.39),
        minRadius=max(5, int(round(nominal_spacing * 0.285))),
        maxRadius=max(8, int(round(nominal_spacing * 0.555))),
    )
    if circles is None:
        return np.empty((0, 3), dtype=np.float32)
    return circles[0].astype(np.float32)


def fit_stone_center_grid(
    warped: np.ndarray,
    board_size: int,
) -> tuple[GridFit, GridFit, int]:
    circles = detect_stone_circles(warped, board_size)
    size = warped.shape[0]
    xfit = fit_regular_grid([(float(x), 2.5) for x, _, _ in circles], board_size, size)
    yfit = fit_regular_grid([(float(y), 2.5) for _, y, _ in circles], board_size, size)
    return xfit, yfit, len(circles)


def align_grid_phase(
    fit: GridFit,
    reference: GridFit,
    board_size: int,
    image_size: int,
) -> GridFit:
    """Resolve whole-cell phase ambiguity using the line-based grid as a reference."""
    valid_offsets = []
    for phase in range(-board_size, board_size + 1):
        offset = fit.offset + phase * fit.spacing
        if offset < 0:
            continue
        if offset + (board_size - 1) * fit.spacing > image_size - 1:
            continue
        valid_offsets.append(offset)
    if not valid_offsets:
        return fit
    offset = min(valid_offsets, key=lambda value: abs(value - reference.offset))
    return GridFit(offset, fit.spacing, fit.score, fit.coverage, fit.candidates)


def board_candidate_grid_score(
    xfit: GridFit,
    yfit: GridFit,
    board_size: int,
    image_size: int,
    *,
    balance_margins: bool = True,
) -> float:
    evidence_score = (
        xfit.score
        + yfit.score
        + (xfit.coverage + yfit.coverage) * 2.0
    )
    # A board contour should map the playable grid to almost the full square.
    # Image-edge or partial-board contours can still contain many regularly
    # spaced lines, but one axis then covers much less of the warped candidate.
    # The playable grid should also leave comparable physical-board margins on
    # opposite sides.  A contour pulled into the background by a hand, rope, or
    # shadow can make the grid reach one warped edge while retaining convincing
    # line evidence; penalizing that asymmetry keeps the actual board frame.
    score = evidence_score * board_grid_extent(xfit, yfit, board_size, image_size)
    if balance_margins:
        score *= board_grid_margin_balance(xfit, yfit, board_size, image_size)
    return score


def board_grid_extent(
    xfit: GridFit,
    yfit: GridFit,
    board_size: int,
    image_size: int,
) -> float:
    image_span = max(float(image_size - 1), 1.0)
    x_extent = min((board_size - 1) * xfit.spacing / image_span, 1.0)
    y_extent = min((board_size - 1) * yfit.spacing / image_span, 1.0)
    return min(x_extent, y_extent)


def board_grid_margin_balance(
    xfit: GridFit,
    yfit: GridFit,
    board_size: int,
    image_size: int,
) -> float:
    image_span = max(float(image_size - 1), 1.0)

    def axis_balance(fit: GridFit) -> float:
        leading = max(fit.offset, 0.0)
        trailing = max(
            image_span - (fit.offset + (board_size - 1) * fit.spacing),
            0.0,
        )
        larger = max(leading, trailing, 1.0)
        return min(leading, trailing) / larger

    combined = math.sqrt(axis_balance(xfit) * axis_balance(yfit))
    return 0.5 + 0.5 * combined


def choose_board(
    image: np.ndarray,
    corners: np.ndarray | None,
    board_size: int,
    warp_size: int,
) -> tuple[np.ndarray, np.ndarray, GridFit, GridFit]:
    if corners is not None:
        ordered = order_points(corners)
        warped = warp_board(image, ordered, warp_size)
        xfit, yfit = detect_grid(warped, board_size)
        return ordered, warped, xfit, yfit

    candidates = detect_board_candidates(image)
    if not candidates:
        h, w = image.shape[:2]
        side = min(h, w)
        x0 = (w - side) / 2.0
        y0 = (h - side) / 2.0
        candidates = [
            np.array(
                [
                    [x0, y0],
                    [x0 + side - 1, y0],
                    [x0 + side - 1, y0 + side - 1],
                    [x0, y0 + side - 1],
                ],
                dtype=np.float32,
            )
        ]

    evaluated = []
    for candidate in candidates:
        warped = warp_board(image, candidate, warp_size)
        xfit, yfit = detect_grid(warped, board_size)
        score = board_candidate_grid_score(xfit, yfit, board_size, warp_size)
        board_profile = estimate_board_profile(warped)
        board = classify_intersections(warped, xfit, yfit, board_size, board_profile)
        occupied = sum(row.count("B") + row.count("W") for row in board)
        evaluated.append((score, occupied, candidate, warped, xfit, yfit))

    raw_best = max(
        evaluated,
        key=lambda item: item[0]
        / board_grid_margin_balance(item[4], item[5], board_size, warp_size),
    )
    raw_margin_balance = board_grid_margin_balance(
        raw_best[4],
        raw_best[5],
        board_size,
        warp_size,
    )
    # Board/background segmentation can occasionally get one corner wrong
    # while the other three remain precise (a hand beside the board is a
    # common cause).  On wood boards, only when that raw winner has strongly
    # asymmetric grid margins, retry it with each corresponding corner from
    # the other detected quadrilaterals.  This keeps the search tightly scoped
    # and lets the grid evidence select a consensus repair.
    if (
        estimate_board_profile(raw_best[3]) == WOOD_BOARD_PROFILE
        and raw_margin_balance < 0.75
    ):
        raw_candidate = order_points(raw_best[2])
        repaired_evaluated = []
        for corner_index in range(4):
            for donor in candidates:
                repaired = raw_candidate.copy()
                repaired[corner_index] = np.round(
                    order_points(donor)[corner_index]
                )
                contour = np.round(repaired).astype(np.int32)
                if not cv2.isContourConvex(contour):
                    continue
                warped = warp_board(image, repaired, warp_size)
                xfit, yfit = detect_grid(warped, board_size)
                score = board_candidate_grid_score(
                    xfit,
                    yfit,
                    board_size,
                    warp_size,
                )
                board_profile = estimate_board_profile(warped)
                board = classify_intersections(
                    warped,
                    xfit,
                    yfit,
                    board_size,
                    board_profile,
                )
                occupied = sum(
                    row.count("B") + row.count("W")
                    for row in board
                )
                lengths = side_lengths(repaired)
                width = (lengths[0] + lengths[2]) / 2.0
                height = (lengths[1] + lengths[3]) / 2.0
                square_score = math.exp(
                    -abs(math.log(width / height)) * 2.2
                )
                repaired_evaluated.append(
                    (
                        score * square_score,
                        (score, occupied, repaired, warped, xfit, yfit),
                    )
                )
        if repaired_evaluated:
            _, repaired_best = max(
                repaired_evaluated,
                key=lambda item: item[0],
            )
            if repaired_best[0] > max(item[0] for item in evaluated):
                evaluated.append(repaired_best)

    best = max(evaluated, key=lambda item: item[0])
    # A sparse board can still have an unreliable line fit when stones or the
    # board frame obscure one of the outer grid lines.  In that case, use the
    # circle centers to select the board candidate as well; they distinguish
    # the playable 19-line grid from the physical wood frame.
    line_grid_incomplete = (
        estimate_board_profile(best[3]) == WOOD_BOARD_PROFILE
        and min(best[4].coverage, best[5].coverage) < board_size - 1
        and board_grid_extent(best[4], best[5], board_size, warp_size) < 0.88
    )
    if max(item[1] for item in evaluated) >= DENSE_BOARD_MIN_STONES or line_grid_incomplete:
        dense_evaluated = []
        for _, occupied, candidate, warped, line_xfit, line_yfit in evaluated:
            circle_xfit, circle_yfit, circle_count = fit_stone_center_grid(warped, board_size)
            if (
                circle_count < DENSE_BOARD_MIN_CIRCLES
                or circle_xfit.coverage < 6
                or circle_yfit.coverage < 6
            ):
                continue
            circle_score = board_candidate_grid_score(
                circle_xfit,
                circle_yfit,
                board_size,
                warp_size,
                balance_margins=False,
            )
            xfit = align_grid_phase(circle_xfit, line_xfit, board_size, warp_size)
            yfit = align_grid_phase(circle_yfit, line_yfit, board_size, warp_size)
            dense_evaluated.append(
                (circle_score, circle_count, occupied, candidate, warped, xfit, yfit)
            )
        if dense_evaluated:
            _, _, _, candidate, warped, xfit, yfit = max(
                dense_evaluated,
                key=lambda item: (item[0], item[1]),
            )
            return order_points(candidate), warped, xfit, yfit

    _, _, chosen, warped, xfit, yfit = best
    return order_points(chosen), warped, xfit, yfit


def fixed_grid_fit(warp_size: int, board_size: int) -> GridFit:
    spacing = (warp_size - 1) / float(board_size - 1)
    return GridFit(0.0, spacing, float(board_size), board_size, board_size)


def estimate_board_profile(warped: np.ndarray) -> str:
    return board_profiles.estimate_board_profile(warped)


def classify_intersections(
    warped: np.ndarray,
    xfit: GridFit,
    yfit: GridFit,
    board_size: int,
    board_profile: str | None = None,
) -> list[list[str]]:
    return board_profiles.classify_intersections(
        warped,
        xfit,
        yfit,
        board_size,
        board_profile or estimate_board_profile(warped),
    )


def board_to_strings(board: list[list[str]]) -> list[str]:
    return ["".join(row).replace("B", "X").replace("W", "O") for row in board]


def render_overlay(warped: np.ndarray, board: list[list[str]], xfit: GridFit, yfit: GridFit) -> np.ndarray:
    overlay = warped.copy()
    size = len(board)
    stone_radius = max(8, int(((xfit.spacing + yfit.spacing) / 2.0) * 0.24))
    for row in range(size):
        y = int(round(yfit.offset + row * yfit.spacing))
        for col in range(size):
            x = int(round(xfit.offset + col * xfit.spacing))
            value = board[row][col]
            if value == "B":
                cv2.circle(overlay, (x, y), stone_radius, (0, 0, 255), 2)
                cv2.putText(overlay, "B", (x - 8, y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            elif value == "W":
                cv2.circle(overlay, (x, y), stone_radius, (255, 0, 0), 2)
                cv2.putText(overlay, "W", (x - 11, y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0), 2)
    return overlay


def render_source_overlay(
    image: np.ndarray,
    corners: list[list[float]] | np.ndarray,
    board: list[list[str]],
    xfit: GridFit,
    yfit: GridFit,
    warp_size: int,
) -> np.ndarray:
    overlay = image.copy()
    source_corners = order_points(np.array(corners, dtype=np.float32))
    polygon = source_corners.astype(np.int32).reshape((-1, 1, 2))
    cv2.polylines(overlay, [polygon], True, (0, 0, 255), 3, lineType=cv2.LINE_AA)
    grid_polygon = grid_edge_source_points(len(board), source_corners, xfit, yfit, warp_size)
    cv2.polylines(
        overlay,
        [grid_polygon.astype(np.int32).reshape((-1, 1, 2))],
        True,
        (0, 210, 255),
        3,
        lineType=cv2.LINE_AA,
    )

    height, width = image.shape[:2]
    label_radius = max(7, int(round(min(height, width) / 95)))
    font_scale = max(0.55, min(height, width) / 2100.0)
    thickness = max(2, int(round(min(height, width) / 520.0)))

    for row in range(len(board)):
        for col in range(len(board)):
            value = board[row][col]
            if value not in {"B", "W"}:
                continue
            source_point = grid_to_source_point(row, col, source_corners, xfit, yfit, warp_size)
            x, y = int(round(float(source_point[0]))), int(round(float(source_point[1])))
            if not (0 <= x < width and 0 <= y < height):
                continue
            text_color = (255, 255, 255) if value == "B" else (0, 0, 0)
            (text_w, text_h), baseline = cv2.getTextSize(value, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            origin = (x - text_w // 2, y + (text_h - baseline) // 2)
            cv2.putText(
                overlay,
                value,
                origin,
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                text_color,
                thickness,
                lineType=cv2.LINE_AA,
            )
    return overlay


def grid_edge_source_points(
    board_size: int,
    corners: list[list[float]] | np.ndarray,
    xfit: GridFit,
    yfit: GridFit,
    warp_size: int,
) -> np.ndarray:
    last = board_size - 1
    return np.array(
        [
            grid_to_source_point(0, 0, corners, xfit, yfit, warp_size),
            grid_to_source_point(0, last, corners, xfit, yfit, warp_size),
            grid_to_source_point(last, last, corners, xfit, yfit, warp_size),
            grid_to_source_point(last, 0, corners, xfit, yfit, warp_size),
        ],
        dtype=np.float32,
    )


def grid_to_source_point(
    row: int,
    col: int,
    corners: list[list[float]] | np.ndarray,
    xfit: GridFit,
    yfit: GridFit,
    warp_size: int,
) -> np.ndarray:
    source_corners = order_points(np.array(corners, dtype=np.float32))
    warped_corners = np.array(
        [[0, 0], [warp_size - 1, 0], [warp_size - 1, warp_size - 1], [0, warp_size - 1]],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(warped_corners, source_corners)
    warped_point = np.array([[[xfit.offset + col * xfit.spacing, yfit.offset + row * yfit.spacing]]], dtype=np.float32)
    return cv2.perspectiveTransform(warped_point, transform)[0, 0]


def recognize_board(
    image_path: Path,
    board_size: int = 19,
    warp_size: int = 1200,
    corners: str | None = None,
    grid_corners: bool = False,
) -> tuple[dict[str, object], np.ndarray, list[list[str]], GridFit, GridFit]:
    image = read_image(image_path)
    manual_corners = parse_corners(corners) if corners else None
    if grid_corners and manual_corners is None:
        raise SystemExit("--grid-corners requires --corners")
    if grid_corners:
        chosen = order_points(manual_corners)
        warped = warp_board(image, chosen, warp_size)
        xfit = fixed_grid_fit(warp_size, board_size)
        yfit = fixed_grid_fit(warp_size, board_size)
    else:
        chosen, warped, xfit, yfit = choose_board(image, manual_corners, board_size, warp_size)

    board_profile = estimate_board_profile(warped)
    board = classify_intersections(warped, xfit, yfit, board_size, board_profile)
    black_stones = sum(row.count("B") for row in board)
    white_stones = sum(row.count("W") for row in board)
    warnings = []
    analysis_safe = True
    if xfit.coverage < 6 or yfit.coverage < 6:
        warnings.append("Low grid-line confidence; verify the overlay or pass --corners manually.")
        analysis_safe = False
    if manual_corners is None and float(np.max(chosen[:, 1])) < image.shape[0] * 0.58:
        warnings.append("Detected board candidate covers only the upper part of the photo; verify the overlay or pass --corners manually.")
        analysis_safe = False
    profile_warnings, profile_analysis_safe = board_profiles.assess_recognition(
        board_profile,
        black_stones,
        white_stones,
    )
    warnings.extend(profile_warnings)
    analysis_safe = analysis_safe and profile_analysis_safe
    result = {
        "image": str(image_path),
        "board_size": board_size,
        "black_stones": black_stones,
        "white_stones": white_stones,
        "board_profile": board_profile,
        "recognition_confidence": "medium" if analysis_safe else "low",
        "analysis_safe": analysis_safe,
        "board_corners": [[round(float(x), 2), round(float(y), 2)] for x, y in chosen],
        "grid": {
            "x_offset": round(xfit.offset, 3),
            "x_spacing": round(xfit.spacing, 3),
            "x_coverage": xfit.coverage,
            "y_offset": round(yfit.offset, 3),
            "y_spacing": round(yfit.spacing, 3),
            "y_coverage": yfit.coverage,
        },
        "board_ascii": board_to_strings(board),
        "board_ascii_legend": "X black stone, O white stone, . empty",
        "warnings": warnings,
    }
    return result, warped, board, xfit, yfit


def main() -> int:
    parser = argparse.ArgumentParser(description="Recognize a Go board image as a 2D board_ascii array.")
    parser.add_argument("image", type=Path, help="Path to a Go board photo or screenshot")
    parser.add_argument("--board-size", type=int, default=19, help="Number of grid lines, default: 19")
    parser.add_argument("--warp-size", type=int, default=1200, help="Internal square board size in pixels")
    parser.add_argument("--corners", help="Four board corners as 'x,y x,y x,y x,y', clockwise from top-left")
    parser.add_argument("--grid-corners", action="store_true", help="Treat --corners as outer grid intersections")
    parser.add_argument("--overlay", type=Path, help="Write a warped-board overlay image for verification")
    parser.add_argument("--source-overlay", type=Path, help="Write an overlay on the original source image for verification")
    args = parser.parse_args()

    result, warped, board, xfit, yfit = recognize_board(args.image, args.board_size, args.warp_size, args.corners, args.grid_corners)
    if args.overlay:
        write_image(args.overlay, render_overlay(warped, board, xfit, yfit))
        result["overlay"] = str(args.overlay)
    if args.source_overlay:
        source_overlay = render_source_overlay(read_image(args.image), result["board_corners"], board, xfit, yfit, args.warp_size)
        write_image(args.source_overlay, source_overlay)
        result["source_overlay"] = str(args.source_overlay)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
