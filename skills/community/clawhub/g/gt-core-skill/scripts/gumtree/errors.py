from __future__ import annotations


class GumtreeError(Exception):
    """Base error for gumtree-skills."""


class BridgeError(GumtreeError):
    """Local bridge or extension communication failed."""


class BrowserAutomationError(GumtreeError):
    """Browser-driven Gumtree automation failed."""
