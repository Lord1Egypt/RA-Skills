"""Runtime wrapper for the OpenClaw capture skill."""

from .config import Settings
from .dispatcher import CaptureDispatcher

__all__ = ["CaptureDispatcher", "Settings"]

