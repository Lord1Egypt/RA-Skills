"""
毛泽东思想实践工具包
Mao Zedong Thought Practice Toolkit

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Mao Thought AI"
__description__ = "毛泽东思想实践工具包"

from .analyzer import analyze_contradiction
from .situator import situation_analysis
from .decider import mass_line_decide
from .summary import show_summary

__all__ = [
    "analyze_contradiction",
    "situation_analysis", 
    "mass_line_decide",
    "show_summary"
]