from __future__ import annotations

import json
import shutil
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .analysis import COORDINATE_COLUMNS, parse_board_ascii


BOARD_SIZE = 19


def normalize_board_ascii(rows: Any, *, board_size: int = BOARD_SIZE) -> list[str]:
    if not isinstance(rows, (list, tuple)):
        raise ValueError(f"board_ascii must contain exactly {board_size} rows")
    if len(rows) != board_size:
        raise ValueError(f"board_ascii must contain exactly {board_size} rows")
    if not all(isinstance(row, str) for row in rows):
        raise ValueError("Every board_ascii row must be a string")
    try:
        parsed = parse_board_ascii("\n".join(rows))
    except SystemExit as exc:
        raise ValueError(str(exc)) from exc
    if len(parsed) != board_size or any(len(row) != board_size for row in parsed):
        raise ValueError(f"board_ascii must be a {board_size}x{board_size} board")
    translation = str.maketrans({"x": "X", "b": "X", "B": "X", "o": "O", "w": "O", "W": "O"})
    return [row.translate(translation) for row in parsed]


def changed_board_points(
    before: Sequence[str],
    after: Sequence[str],
    *,
    coordinate_style: str,
) -> list[str]:
    before_rows = normalize_board_ascii(before, board_size=len(before))
    after_rows = normalize_board_ascii(after, board_size=len(before_rows))
    columns = COORDINATE_COLUMNS[coordinate_style]
    board_size = len(before_rows)
    return [
        f"{columns[col]}{board_size - row}"
        for row in range(board_size)
        for col in range(board_size)
        if before_rows[row][col] != after_rows[row][col]
    ]


@dataclass(frozen=True)
class RecognitionLabelStore:
    root: Path

    def create(
        self,
        *,
        image_path: Path,
        detector_output_path: Path | None,
        corrected_output_path: Path | None,
        metadata: dict[str, Any],
    ) -> tuple[str, Path]:
        label_id = "label_" + uuid.uuid4().hex
        self.root.mkdir(parents=True, exist_ok=True)
        staging = self.root / f".{label_id}.tmp"
        destination = self.root / label_id
        staging.mkdir()
        try:
            input_name = self._image_name("input", image_path)
            detector_name = self._image_name("detector-output", detector_output_path)
            corrected_name = self._image_name("corrected-output", corrected_output_path)
            shutil.copyfile(image_path, staging / input_name)
            if detector_output_path and detector_output_path.is_file():
                shutil.copyfile(detector_output_path, staging / detector_name)
            if corrected_output_path and corrected_output_path.is_file():
                shutil.copyfile(corrected_output_path, staging / corrected_name)
            payload = {
                "label_id": label_id,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
                "input_image": input_name,
                "detector_output_image": detector_name if (staging / detector_name).is_file() else None,
                "corrected_output_image": corrected_name if (staging / corrected_name).is_file() else None,
                **metadata,
            }
            (staging / "metadata.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            staging.replace(destination)
        except BaseException:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        return label_id, destination

    @staticmethod
    def _image_name(stem: str, path: Path | None) -> str:
        suffix = path.suffix.lower() if path else ""
        if suffix not in {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}:
            suffix = ".jpg"
        return stem + suffix
