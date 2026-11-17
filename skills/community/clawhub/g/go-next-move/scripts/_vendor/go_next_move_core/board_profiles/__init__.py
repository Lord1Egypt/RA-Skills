from __future__ import annotations

import numpy as np

from . import white_plastic_or_paper, wood


WOOD_BOARD_PROFILE = wood.PROFILE_NAME
WHITE_BOARD_PROFILE = white_plastic_or_paper.PROFILE_NAME


def estimate_board_profile(warped: np.ndarray) -> str:
    if white_plastic_or_paper.is_profile(warped):
        return WHITE_BOARD_PROFILE
    return WOOD_BOARD_PROFILE


def classify_intersections(warped: np.ndarray, xfit, yfit, board_size: int, board_profile: str) -> list[list[str]]:
    if board_profile == WHITE_BOARD_PROFILE:
        return white_plastic_or_paper.classify_intersections(warped, xfit, yfit, board_size)
    return wood.classify_intersections(warped, xfit, yfit, board_size)


def assess_recognition(board_profile: str, black_stones: int, white_stones: int) -> tuple[list[str], bool]:
    if board_profile == WHITE_BOARD_PROFILE:
        return white_plastic_or_paper.assess_recognition(black_stones, white_stones)
    return wood.assess_recognition(black_stones, white_stones)
