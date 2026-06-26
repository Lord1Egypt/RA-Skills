"""
LLM Tools Library

Universal tool definition system for LLM function calling
"""

from .registry import ToolRegistry, Tool, tool

__version__ = "1.0.0"
__all__ = ['ToolRegistry', 'Tool', 'tool']
