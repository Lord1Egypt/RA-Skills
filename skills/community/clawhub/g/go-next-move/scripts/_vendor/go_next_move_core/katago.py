from __future__ import annotations

import contextlib
import json
import logging
import subprocess
import threading
from collections import deque
from pathlib import Path
from typing import Any

from .katago_protocol import AnalysisResponseAccumulator, analysis_command, build_analysis_query


class ResidentKataGoAnalysisEngine:
    def __init__(
        self,
        *,
        katago: str,
        model: str,
        config: str,
        skill_config: Path,
        logger: logging.Logger | None = None,
    ) -> None:
        self.katago = katago
        self.model = model
        self.config = config
        self.skill_config = skill_config
        self.log = logger or logging.getLogger("resident-katago")
        self._lock = threading.Lock()
        self._proc: subprocess.Popen[str] | None = None
        self._stderr_tail: deque[str] = deque(maxlen=80)
        self._stderr_thread: threading.Thread | None = None

    def analyze(
        self,
        rows: list[str],
        side_to_move: str,
        *,
        komi: float,
        visits: int,
    ) -> dict[str, Any]:
        query = build_analysis_query(
            rows,
            side_to_move=side_to_move,
            komi=komi,
            visits=visits,
        )
        with self._lock:
            proc = self._ensure_process()
            assert proc.stdin is not None
            assert proc.stdout is not None
            proc.stdin.write(json.dumps(query, ensure_ascii=False) + "\n")
            proc.stdin.flush()

            accumulator = AnalysisResponseAccumulator(query["id"])
            while True:
                line = proc.stdout.readline()
                if line == "":
                    self._proc = None
                    raise RuntimeError(f"KataGo exited before returning analysis. stderr:\n{self._stderr_text()}")
                response = accumulator.consume(line)
                if response is not None:
                    return response

    def _ensure_process(self) -> subprocess.Popen[str]:
        if self._proc is not None and self._proc.poll() is None:
            return self._proc
        if self._proc is not None:
            self.log.warning("restarting exited KataGo analysis process returncode=%s", self._proc.returncode)

        working_directory = Path.cwd()
        command = analysis_command(
            self.katago,
            self.model,
            self.config,
            self.skill_config,
            working_directory=working_directory,
        )
        self.log.info("starting resident KataGo analysis process")
        self._proc = subprocess.Popen(
            command,
            cwd=working_directory,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._stderr_tail.clear()
        self._stderr_thread = threading.Thread(target=self._drain_stderr, args=(self._proc,), daemon=True)
        self._stderr_thread.start()
        return self._proc

    def start(self) -> None:
        with self._lock:
            self._ensure_process()

    def _drain_stderr(self, proc: subprocess.Popen[str]) -> None:
        if proc.stderr is None:
            return
        for line in proc.stderr:
            self._stderr_tail.append(line.rstrip())

    def _stderr_text(self) -> str:
        return "\n".join(self._stderr_tail)

    def close(self) -> None:
        proc = self._proc
        self._proc = None
        if proc is None or proc.poll() is not None:
            return
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=5)
        if proc.poll() is None:
            proc.kill()
