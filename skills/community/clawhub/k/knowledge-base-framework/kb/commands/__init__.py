#!/usr/bin/env python3
"""
KB Command Framework - Command Registry

Commands werden automatisch via @register_command registriert.

Verbesserungen gegenüber Original:
- Better Import Error Handling
- Command Metadata
- Lazy Loading Support
"""

from typing import Type, Dict, Optional, List
import importlib
import sys

from kb.base.command import BaseCommand


# Registry for command discovery
_COMMAND_REGISTRY: Dict[str, Type['BaseCommand']] = {}
_METADATA_REGISTRY: Dict[str, Dict] = {}


def register_command(
    cls: Type['BaseCommand'],
    description: Optional[str] = None,
    category: str = "general"
) -> Type['BaseCommand']:
    """
    Decorator: Registriert Command automatisch.
    
    Args:
        cls: Command class to register
        description: Optional override for help text
        category: Command category for grouping
    
    Returns:
        The same class (for decorator chaining)
    """
    # Register in main registry
    _COMMAND_REGISTRY[cls.name] = cls
    
    # Store metadata
    _METADATA_REGISTRY[cls.name] = {
        'name': cls.name,
        'help': description or cls.help,
        'category': category,
        'class': cls,
    }
    
    return cls


def get_commands(
    category: Optional[str] = None,
    include_hidden: bool = False
) -> Dict[str, Type['BaseCommand']]:
    """
    Gibt alle registrierten Commands zurück.
    
    Args:
        category: Filter by category
        include_hidden: Include commands marked as hidden
    
    Returns:
        Dictionary of command_name -> Command class
    """
    if category:
        return {
            name: cls for name, cls in _COMMAND_REGISTRY.items()
            if _METADATA_REGISTRY.get(name, {}).get('category') == category
        }
    
    return _COMMAND_REGISTRY.copy()


def get_command(name: str) -> Optional[Type['BaseCommand']]:
    """Get specific command by name."""
    return _COMMAND_REGISTRY.get(name)


def get_metadata(name: str) -> Optional[Dict]:
    """Get command metadata."""
    return _METADATA_REGISTRY.get(name)


def list_categories() -> List[str]:
    """List all command categories."""
    return list({m['category'] for m in _METADATA_REGISTRY.values()})


def reload_commands() -> None:
    """Reload all command modules."""
    # Clear registries
    _COMMAND_REGISTRY.clear()
    _METADATA_REGISTRY.clear()
    
    # Re-import command modules
    command_modules = [
        'kb.commands.sync',
        'kb.commands.audit',
        'kb.commands.ghost',
        'kb.commands.search',
        'kb.commands.warmup',
        'kb.commands.llm',
        'kb.commands.engine',
        'kb.commands.backup',
    ]
    
    for module_name in command_modules:
        try:
            if module_name in sys.modules:
                # Reload existing module
                importlib.reload(sys.modules[module_name])
            else:
                # Fresh import
                importlib.import_module(module_name)
        except ImportError as e:
            # Commands may not be implemented yet - that's ok
            pass


# Import all commands to trigger registration
# Use lazy imports to avoid circular dependency issues
def _ensure_commands_loaded():
    """Lazy load commands on first access."""
    if not _COMMAND_REGISTRY:
        try:
            from kb.commands.sync import SyncCommand
            from kb.commands.audit import AuditCommand
            from kb.commands.ghost import GhostCommand
            from kb.commands.warmup import WarmupCommand
            from kb.commands.search import SearchCommand
            from kb.commands.llm import LLMCommand
            from kb.commands.engine import EngineListCommand, EngineInfoCommand
            from kb.commands.backup import BackupCommand
        except ImportError:
            pass  # Commands not yet implemented


__all__ = [
    'BaseCommand',
    'SyncCommand',
    'AuditCommand',
    'GhostCommand',
    'WarmupCommand',
    'SearchCommand',
    'LLMCommand',
    'EngineListCommand',
    'EngineInfoCommand',
    'BackupCommand',
    'register_command',
    'get_commands',
    'get_command',
    'get_metadata',
    'list_categories',
    'reload_commands',
    '_COMMAND_REGISTRY',
    '_METADATA_REGISTRY',
]
