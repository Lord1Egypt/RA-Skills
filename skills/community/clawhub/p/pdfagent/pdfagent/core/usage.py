from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter, process_time
from typing import Iterable

from .pdf import count_pages_safe


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Usage:
    tool: str
    started_at: str
    ended_at: str
    duration_ms: int
    cpu_ms: int
    bytes_in: int
    bytes_out: int
    pages_in: int | None
    pages_out: int | None
    inputs: list[str]
    outputs: list[str]
    success: bool
    error: str | None = None
    metrics: dict[str, int | float | str] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class UsageMeter:
    def __init__(self, tool: str, inputs: Iterable[Path]) -> None:
        self.tool = tool
        self.inputs = [Path(p) for p in inputs]
        self._start_wall = perf_counter()
        self._start_cpu = process_time()
        self._started_at = _utc_now()

    def finish(
        self,
        outputs: Iterable[Path],
        *,
        success: bool,
        error: str | None = None,
        metrics: dict[str, int | float | str] | None = None,
    ) -> Usage:
        ended_at = _utc_now()
        duration_ms = int((perf_counter() - self._start_wall) * 1000)
        cpu_ms = int((process_time() - self._start_cpu) * 1000)

        inputs = [Path(p) for p in self.inputs]
        outputs_list = [Path(p) for p in outputs]

        bytes_in = sum(p.stat().st_size for p in inputs if p.exists())
        bytes_out = sum(p.stat().st_size for p in outputs_list if p.exists())

        pages_in = _sum_pages(inputs)
        pages_out = _sum_pages(outputs_list)

        return Usage(
            tool=self.tool,
            started_at=self._started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            duration_ms=duration_ms,
            cpu_ms=cpu_ms,
            bytes_in=bytes_in,
            bytes_out=bytes_out,
            pages_in=pages_in,
            pages_out=pages_out,
            inputs=[str(p) for p in inputs],
            outputs=[str(p) for p in outputs_list],
            success=success,
            error=error,
            metrics=metrics,
        )


def _sum_pages(paths: Iterable[Path]) -> int | None:
    total: int | None = 0
    for path in paths:
        pages = count_pages_safe(path)
        if pages is None:
            total = None
            break
        total += pages
    return total
