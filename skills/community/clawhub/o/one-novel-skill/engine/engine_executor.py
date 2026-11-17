#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engine_executor.py — 统一的引擎执行器

替换所有裸 try/except pass，所有引擎失败可观测、可度量。
"""

import logging, time
from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

_log = logging.getLogger("engine_executor")


class EngineStatus(Enum):
    OK = "ok"
    DEGRADED = "degraded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class EngineResult:
    engine_name: str
    status: EngineStatus
    issues: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    retry_count: int = 0
    elapsed_ms: float = 0.0

    @property
    def is_ok(self) -> bool:
        return self.status in (EngineStatus.OK, EngineStatus.SKIPPED)

    @property
    def is_degraded(self) -> bool:
        return self.status == EngineStatus.DEGRADED


@dataclass
class EngineTask:
    name: str
    fn: Callable
    critical: bool = False       # 致命引擎：失败则终止管线
    max_retries: int = 1
    timeout: float = 30.0
    kwargs: Dict[str, Any] = field(default_factory=dict)


class EngineExecutor:
    """统一的引擎执行器"""

    def __init__(self, max_consecutive_failures: int = 5):
        self._tasks: List[EngineTask] = []
        self._results: List[EngineResult] = []
        self._max_consecutive_failures = max_consecutive_failures

    def register(
        self,
        name: str,
        fn: Callable,
        critical: bool = False,
        max_retries: int = 1,
        **kwargs,
    ):
        self._tasks.append(EngineTask(
            name=name, fn=fn, critical=critical,
            max_retries=max_retries, kwargs=kwargs,
        ))

    def execute_all(self) -> List[EngineResult]:
        self._results = []
        consecutive_failures = 0

        for task in self._tasks:
            result = self._execute_one(task)
            self._results.append(result)

            if not result.is_ok:
                consecutive_failures += 1
                if task.critical:
                    _log.error(
                        f"EngineExecutor: critical engine '{task.name}' failed, aborting"
                    )
                    break
                if consecutive_failures >= self._max_consecutive_failures:
                    _log.error(
                        f"EngineExecutor: {consecutive_failures} consecutive failures, aborting"
                    )
                    break
            else:
                consecutive_failures = 0

        return self._results

    def _execute_one(self, task: EngineTask) -> EngineResult:
        start = time.time()
        last_error = None

        for attempt in range(task.max_retries + 1):
            try:
                result_data = task.fn(**task.kwargs)
                elapsed = (time.time() - start) * 1000

                if isinstance(result_data, dict):
                    return EngineResult(
                        engine_name=task.name,
                        status=EngineStatus.OK,
                        issues=result_data.get("issues", []),
                        metrics=result_data.get("metrics", {}),
                        retry_count=attempt,
                        elapsed_ms=elapsed,
                    )
                elif isinstance(result_data, list):
                    return EngineResult(
                        engine_name=task.name,
                        status=EngineStatus.OK,
                        issues=result_data,
                        retry_count=attempt,
                        elapsed_ms=elapsed,
                    )
                elif isinstance(result_data, str):
                    return EngineResult(
                        engine_name=task.name,
                        status=EngineStatus.OK,
                        issues=[result_data] if result_data else [],
                        retry_count=attempt,
                        elapsed_ms=elapsed,
                    )
                else:
                    return EngineResult(
                        engine_name=task.name,
                        status=EngineStatus.OK,
                        retry_count=attempt,
                        elapsed_ms=elapsed,
                    )

            except Exception as e:
                last_error = str(e)
                if attempt < task.max_retries:
                    delay = 2 ** attempt
                    _log.debug(
                        f"EngineExecutor: '{task.name}' attempt {attempt+1} failed, retry in {delay}s: {e}"
                    )
                    time.sleep(delay)
                    continue

        elapsed = (time.time() - start) * 1000
        return EngineResult(
            engine_name=task.name,
            status=EngineStatus.FAILED if task.critical else EngineStatus.DEGRADED,
            error=last_error,
            retry_count=task.max_retries,
            elapsed_ms=elapsed,
        )

    def get_results(self) -> List[EngineResult]:
        return list(self._results)

    def get_summary(self) -> Dict[str, Any]:
        total = len(self._results)
        ok = sum(1 for r in self._results if r.status == EngineStatus.OK)
        degraded = sum(1 for r in self._results if r.status == EngineStatus.DEGRADED)
        failed = sum(1 for r in self._results if r.status == EngineStatus.FAILED)
        skipped = sum(1 for r in self._results if r.status == EngineStatus.SKIPPED)

        return {
            "total": total,
            "ok": ok,
            "degraded": degraded,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": ok / max(total, 1),
            "failed_engines": [r.engine_name for r in self._results if r.status == EngineStatus.FAILED],
            "degraded_engines": [r.engine_name for r in self._results if r.status == EngineStatus.DEGRADED],
        }
