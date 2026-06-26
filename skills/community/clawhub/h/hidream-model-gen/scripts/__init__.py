"""
Vivago AI Skill - Python Package

Usage:
    from scripts import VivagoClient
    from scripts.enums import TaskStatus
    from scripts.exceptions import TaskFailedError
"""

from .vivago_client import VivagoClient, create_client
from .template_manager import TemplateManager
from .config_loader import load_ports_config
from .enums import TaskStatus, AspectRatio, PortCategory, PortName, ModuleName
from .exceptions import (
    VivagoError, VivagoAPIError, InvalidPortError,
    TaskFailedError, TaskRejectedError, TaskTimeoutError,
    ImageUploadError, MissingCredentialError
)

__version__ = "0.3.0"
__all__ = [
    "VivagoClient",
    "create_client",
    "TemplateManager",
    "load_ports_config",
    "TaskStatus",
    "AspectRatio",
    "PortCategory",
    "PortName",
    "ModuleName",
    "VivagoError",
    "VivagoAPIError",
    "InvalidPortError",
    "TaskFailedError",
    "TaskRejectedError",
    "TaskTimeoutError",
    "ImageUploadError",
    "MissingCredentialError",
]
