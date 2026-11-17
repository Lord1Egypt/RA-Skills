from __future__ import annotations

import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any

from .coordinates import format_coord


DEFAULT_RUNTIME_LOG_DIRECTORY = Path(tempfile.gettempdir()) / "go-next-move-katago-analysis-logs"


class KataGoProtocolError(RuntimeError):
    """A structured error returned by KataGo's analysis protocol."""


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


def build_analysis_query(
    rows: list[str],
    *,
    side_to_move: str,
    komi: float,
    visits: int,
    query_id: str | None = None,
) -> dict[str, Any]:
    return {
        "id": query_id or f"go-next-move-{uuid.uuid4().hex}",
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


def analysis_command(
    katago: str,
    model: str,
    config: str,
    skill_config: Path,
    *,
    working_directory: Path | None = None,
    runtime_log_directory: Path | None = None,
) -> list[str]:
    process_cwd = working_directory or Path.cwd()
    log_directory = runtime_log_directory or DEFAULT_RUNTIME_LOG_DIRECTORY
    skill_config_arg = (
        os.path.relpath(skill_config, start=process_cwd)
        if skill_config.is_absolute()
        else str(skill_config)
    )
    return [
        katago,
        "analysis",
        "-model",
        model,
        "-config",
        config,
        "-config",
        skill_config_arg,
        "-override-config",
        (
            f"logDir={log_directory},logToStderr=true,"
            "logAllRequests=false,logAllResponses=false,logErrorsAndWarnings=false"
        ),
    ]


class AnalysisResponseAccumulator:
    """Parse the shared line-oriented KataGo response contract."""

    def __init__(self, query_id: str) -> None:
        self.query_id = query_id
        self.warnings: list[Any] = []

    def consume(self, line: str) -> dict[str, Any] | None:
        line = line.strip()
        if not line:
            return None
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict):
            return None
        if "error" in payload:
            raise KataGoProtocolError(f"KataGo returned an error: {payload['error']}")
        if "warning" in payload:
            self.warnings.append(payload["warning"])
            return None
        if payload.get("id") != self.query_id or payload.get("isDuringSearch") is not False:
            return None
        if self.warnings:
            payload.setdefault("warnings", []).extend(self.warnings)
        return payload
