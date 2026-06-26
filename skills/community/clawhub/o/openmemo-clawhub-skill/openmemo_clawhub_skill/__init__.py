"""
OpenMemo Bootstrap Skill for ClawHub

Provides persistent memory, task deduplication, and scene-aware recall
for OpenClaw agents via a Bootstrap + Memory dual-mode architecture.
"""

from openmemo_clawhub_skill.skill import OpenMemoSkill
from openmemo_clawhub_skill.detector import AdapterDetector
from openmemo_clawhub_skill.tools import recall_memory, write_memory, check_task_memory

__version__ = "1.0.0"
__all__ = [
    "OpenMemoSkill",
    "AdapterDetector",
    "recall_memory",
    "write_memory",
    "check_task_memory",
]
