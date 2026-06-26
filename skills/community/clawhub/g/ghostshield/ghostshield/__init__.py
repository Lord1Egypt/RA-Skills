"""
GhostShield - 反同事蒸馏防护盾
保护个人数字痕迹，防止被 AI 精准蒸馏
"""

__version__ = "1.0.0"
__author__ = "老杨 + AI Assistant"

from .core import GhostShield
from .pii_detector import PIIDetector
from .style_analyzer import StyleAnalyzer
from .obfuscator import Obfuscator
from .validator import Validator

__all__ = [
    "GhostShield",
    "PIIDetector",
    "StyleAnalyzer",
    "Obfuscator",
    "Validator",
]
