from __future__ import annotations


GTP_COLUMNS = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
SEQUENTIAL_COLUMNS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COORDINATE_COLUMNS = {
    "gtp": GTP_COLUMNS,
    "sequential": SEQUENTIAL_COLUMNS,
}


def format_coord(row: int, col: int, board_size: int, coordinate_style: str) -> str:
    columns = COORDINATE_COLUMNS[coordinate_style]
    if col >= len(columns):
        raise SystemExit(
            f"Board size {board_size} is too large for the {coordinate_style} coordinate column table"
        )
    return f"{columns[col]}{board_size - row}"
