"""
Adapter Detection — checks if OpenMemo adapter is running locally.

Performs three checks:
  1. Health endpoint (GET /health)
  2. Memory recall endpoint (POST /memory/recall)
  3. Task check endpoint (POST /memory/search)
"""

import logging
from dataclasses import dataclass, field
from typing import List, Tuple

import requests

from openmemo_clawhub_skill.config import (
    SkillConfig,
    HEALTH_PATH,
    MEMORY_RECALL_PATH,
    TASK_CHECK_PATH,
)

logger = logging.getLogger("openmemo_clawhub_skill")


@dataclass
class DetectionResult:
    available: bool = False
    server_running: bool = False
    adapter_installed: bool = False
    checks: List[Tuple[str, bool, str]] = field(default_factory=list)

    def summary(self) -> str:
        lines = []
        for name, ok, msg in self.checks:
            status = "OK" if ok else "FAIL"
            lines.append(f"  {name}: {status} — {msg}")
        return "\n".join(lines)


class AdapterDetector:
    def __init__(self, config: SkillConfig = None):
        self._config = config or SkillConfig()

    def detect(self) -> DetectionResult:
        result = DetectionResult()
        endpoint = self._config.endpoint
        timeout = self._config.health_timeout

        result.adapter_installed = self._check_package_installed()

        health_ok = self._check_health(endpoint, timeout, result)
        if not health_ok:
            return result

        result.server_running = True

        self._check_recall(endpoint, timeout, result)
        self._check_task(endpoint, timeout, result)

        all_ok = all(ok for _, ok, _ in result.checks)
        result.available = all_ok
        result.adapter_installed = True
        return result

    @staticmethod
    def _check_package_installed() -> bool:
        try:
            import openmemo  # noqa: F401
            return True
        except ImportError:
            return False

    def _check_health(self, endpoint: str, timeout: int,
                      result: DetectionResult) -> bool:
        try:
            resp = requests.get(f"{endpoint}{HEALTH_PATH}", timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "ok":
                    result.checks.append(("health", True, f"{endpoint} reachable, status=ok"))
                    return True
                else:
                    result.checks.append(("health", False, f"unexpected status: {data}"))
                    return False
            else:
                result.checks.append(("health", False, f"HTTP {resp.status_code}"))
                return False
        except requests.ConnectionError:
            result.checks.append(("health", False, f"cannot connect to {endpoint}"))
            return False
        except Exception as e:
            result.checks.append(("health", False, str(e)))
            return False

    def _check_recall(self, endpoint: str, timeout: int,
                      result: DetectionResult) -> bool:
        try:
            resp = requests.post(
                f"{endpoint}{MEMORY_RECALL_PATH}",
                json={"query": "_health_check", "limit": 1},
                timeout=timeout,
            )
            if 200 <= resp.status_code < 300:
                result.checks.append(("recall", True, "/memory/recall OK"))
                return True
            else:
                result.checks.append(("recall", False, f"HTTP {resp.status_code}"))
                return False
        except Exception as e:
            result.checks.append(("recall", False, str(e)))
            return False

    def _check_task(self, endpoint: str, timeout: int,
                    result: DetectionResult) -> bool:
        try:
            resp = requests.post(
                f"{endpoint}{TASK_CHECK_PATH}",
                json={"query": "_task_health_check", "limit": 1},
                timeout=timeout,
            )
            if 200 <= resp.status_code < 300:
                result.checks.append(("task_check", True, "/memory/search OK"))
                return True
            else:
                result.checks.append(("task_check", False, f"HTTP {resp.status_code}"))
                return False
        except Exception as e:
            result.checks.append(("task_check", False, str(e)))
            return False
