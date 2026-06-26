"""
OpenMemo Bootstrap Skill — main entry point.

Dual-mode architecture:
  - Bootstrap Mode: adapter not detected → guide installation
  - Memory Mode: adapter detected → provide memory tools

Usage:
    skill = OpenMemoSkill()
    result = skill.run()

    if result["mode"] == "memory":
        # Tools available: recall_memory, write_memory, check_task_memory
        pass
    else:
        # Bootstrap mode: show installation guide
        print(result["message"])
"""

import logging
from typing import Optional

from openmemo_clawhub_skill.config import SkillConfig, MODE_BOOTSTRAP, MODE_MEMORY
from openmemo_clawhub_skill.detector import AdapterDetector
from openmemo_clawhub_skill.bootstrap import get_install_guide, setup_wizard
from openmemo_clawhub_skill.tools import (
    recall_memory, write_memory, check_task_memory, TOOL_DEFINITIONS,
)
from openmemo_clawhub_skill.rules import get_memory_rules

logger = logging.getLogger("openmemo_clawhub_skill")


class OpenMemoSkill:
    def __init__(self, config: SkillConfig = None):
        self._config = config or SkillConfig()
        self._detector = AdapterDetector(self._config)
        self._mode = None
        self._detection_result = None

    @property
    def mode(self) -> str:
        if self._mode is None:
            self.detect()
        return self._mode

    @property
    def is_memory_mode(self) -> bool:
        return self.mode == MODE_MEMORY

    @property
    def is_bootstrap_mode(self) -> bool:
        return self.mode == MODE_BOOTSTRAP

    def detect(self):
        self._detection_result = self._detector.detect()
        if self._detection_result.available:
            self._mode = MODE_MEMORY
            logger.info("OpenMemo adapter detected — entering Memory Mode")
        else:
            self._mode = MODE_BOOTSTRAP
            logger.info("OpenMemo adapter not detected — entering Bootstrap Mode")
        return self._detection_result

    def run(self) -> dict:
        detection = self.detect()

        if self._mode == MODE_MEMORY:
            return {
                "mode": MODE_MEMORY,
                "status": "ready",
                "tools": TOOL_DEFINITIONS,
                "rules": get_memory_rules(),
                "endpoint": self._config.endpoint,
                "message": "OpenMemo Memory Mode active. Agent memory system is ready.",
            }
        else:
            guide = get_install_guide(
                adapter_installed=detection.adapter_installed,
                server_running=detection.server_running,
            )
            return {
                "mode": MODE_BOOTSTRAP,
                "status": "setup_required",
                "tools": [],
                "rules": "",
                "message": guide,
                "diagnostics": detection.summary(),
            }

    def get_setup_wizard(self) -> str:
        return setup_wizard()

    def recall(self, query: str, scene: str = "") -> dict:
        if not self.is_memory_mode:
            return {"error": "Memory mode not active. Run setup first."}
        return recall_memory(query, scene=scene, config=self._config)

    def write(self, content: str, scene: str = "",
              memory_type: str = "fact") -> dict:
        if not self.is_memory_mode:
            return {"error": "Memory mode not active. Run setup first."}
        return write_memory(content, scene=scene, memory_type=memory_type,
                           config=self._config)

    def check_task(self, task_description: str) -> dict:
        if not self.is_memory_mode:
            return {"error": "Memory mode not active. Run setup first."}
        return check_task_memory(task_description, config=self._config)

    def get_manifest(self) -> dict:
        return SKILL_MANIFEST


SKILL_MANIFEST = {
    "name": "openmemo-memory",
    "version": "1.0.0",
    "description": "Persistent memory system for OpenClaw agents. Stop agents from repeating tasks. Give your AI long-term memory.",
    "author": "OpenMemo",
    "homepage": "https://github.com/openmemoai/openmemo-clawhub-skill",
    "tools": [
        "recall_memory",
        "write_memory",
        "check_task_memory",
    ],
    "modes": ["bootstrap", "memory"],
    "features": [
        "Persistent agent memory across sessions",
        "Task deduplication — stop repeating work",
        "Scene-aware recall (coding, debug, research)",
        "Memory inspector dashboard",
        "Local-first architecture — your data stays local",
    ],
    "setup": {
        "install": "pip install openmemo openmemo-openclaw",
        "serve": "openmemo serve",
        "restart": "Restart your agent after setup",
    },
    "security": {
        "network": "localhost only",
        "data": "local-first, no cloud by default",
    },
}
