"""
Abstract Base Extractor
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseExtractor(ABC):
    def __init__(self, ws, ws_url: str):
        self.ws = ws
        self.ws_url = ws_url

    @classmethod
    @abstractmethod
    def can_handle(cls, url: str) -> bool:
        """Returns True if this extractor can process the given URL."""
        pass

    @abstractmethod
    async def prepare(self) -> int:
        """Prepares the page, resolves contexts/frames, and returns total page count."""
        pass

    @abstractmethod
    async def extract_page(self, page_index: int, temp_dir: str) -> str:
        """Renders and extracts a single page (0-based index) to an image file, returning the file path."""
        pass
