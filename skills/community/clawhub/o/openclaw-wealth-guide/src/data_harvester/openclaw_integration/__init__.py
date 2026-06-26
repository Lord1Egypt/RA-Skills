"""
OpenClaw集成模块
提供与OpenClaw平台的集成功能
"""

from .skill_wrapper import OpenClawSkillWrapper
from .skill_manifest import SkillManifest
from .api_client import OpenClawAPIClient

__all__ = [
    "OpenClawSkillWrapper",
    "SkillManifest",
    "OpenClawAPIClient",
]