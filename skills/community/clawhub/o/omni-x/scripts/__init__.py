"""
Omni-X Twitter Skills Package
A skill project for agents to extract Twitter data.
"""

from .twitter_skills import TwitterSkills
from .skill_interface import TwitterSkillInterface

__version__ = "0.1.0"
__all__ = ["TwitterSkills", "TwitterSkillInterface"]
