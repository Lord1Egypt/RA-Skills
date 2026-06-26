"""
LIR-v2 核心模块
"""

from .reflector import (
    LogicInversionReflector,
    reflect,
    reflect_json
)

__all__ = [
    'LogicInversionReflector',
    'reflect',
    'reflect_json'
]

__version__ = '2.0.0'
