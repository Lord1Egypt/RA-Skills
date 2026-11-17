"""Abstract browser driver interface."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

logger = logging.getLogger(__name__)


class BrowserDriver(ABC):
    """Abstract interface for browser automation drivers.

    Implement this to add a new browser backend (Playwright, Selenium, etc.)
    """

    @abstractmethod
    def navigate(self, url: str, new_tab: bool = True, group_title: str = "") -> dict:
        """Navigate to a URL."""
        ...

    def list_tabs(self) -> dict:
        """Return the current session's tabs when the backend supports it.

        Search uses this optional hook to distinguish the first navigation in
        a session from later navigations. Backends that cannot enumerate tabs
        may keep the default and the caller will conservatively open a tab.
        """
        raise NotImplementedError

    @abstractmethod
    def snapshot(self) -> dict:
        """Get accessibility tree snapshot."""
        ...

    @abstractmethod
    def click(self, selector: str) -> dict:
        """Click an element by selector (@e ref or CSS)."""
        ...

    @abstractmethod
    def fill(self, selector: str, value: str) -> dict:
        """Fill an input/textarea/contenteditable element."""
        ...

    @abstractmethod
    def evaluate(self, code: str) -> Any:
        """Execute JavaScript and return the result."""
        ...

    @abstractmethod
    def screenshot(self, path: Optional[str] = None) -> dict:
        """Take a screenshot."""
        ...

    @abstractmethod
    def close(self) -> dict:
        """Close the current session/tabs."""
        ...

    def cdp(self, method: str, params: Optional[dict] = None) -> dict:
        """Send a raw CDP command (optional, for advanced use)."""
        raise NotImplementedError
