"""
KB Framework - Base Module

Core components for KB commands:
- KBConfig: Singleton configuration management
- KBLogger: Singleton logging setup
- KBConnection: Context manager for SQLite
- BaseCommand: Abstract base for all commands
"""

from kb.base.config import KBConfig
from kb.base.logger import KBLogger
from kb.base.db import KBConnection
from kb.base.command import BaseCommand

__all__ = [
    'KBConfig',
    'KBLogger',
    'KBConnection',
    'BaseCommand',
]
