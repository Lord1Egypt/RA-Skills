"""
Configuration for OpenMemo ClawHub Skill.
"""

import os

DEFAULT_ENDPOINT = "http://localhost:8765"
HEALTH_PATH = "/health"
MEMORY_WRITE_PATH = "/memory/write"
MEMORY_RECALL_PATH = "/memory/recall"
MEMORY_SEARCH_PATH = "/memory/search"
TASK_CHECK_PATH = "/memory/search"
HEALTH_TIMEOUT = 5
REQUEST_TIMEOUT = 10

MODE_BOOTSTRAP = "bootstrap"
MODE_MEMORY = "memory"


LOCALHOST_PREFIXES = (
    "http://localhost",
    "http://127.0.0.1",
    "http://[::1]",
)


class SkillConfig:
    def __init__(self,
                 endpoint: str = "",
                 health_timeout: int = HEALTH_TIMEOUT,
                 request_timeout: int = REQUEST_TIMEOUT,
                 auto_detect: bool = True,
                 allow_remote: bool = False):
        self.endpoint = endpoint or os.environ.get("OPENMEMO_ENDPOINT", DEFAULT_ENDPOINT)
        self.health_timeout = health_timeout
        self.request_timeout = request_timeout
        self.auto_detect = auto_detect
        self.allow_remote = allow_remote

        if not self.allow_remote and not self._is_localhost(self.endpoint):
            raise ValueError(
                f"Endpoint '{self.endpoint}' is not localhost. "
                "Set allow_remote=True to use remote endpoints."
            )

    @staticmethod
    def _is_localhost(endpoint: str) -> bool:
        return any(endpoint.startswith(p) for p in LOCALHOST_PREFIXES)
