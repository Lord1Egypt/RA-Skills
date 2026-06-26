"""Base class for stack-specific analyzers."""

from abc import ABC, abstractmethod
from typing import Dict, List


class StackAnalyzer(ABC):
    """Abstract base for stack analyzers."""

    @abstractmethod
    def get_extensions(self) -> List[str]:
        """Return file extensions this stack handles."""
        pass

    @abstractmethod
    def get_large_file_threshold(self) -> int:
        """Return line count threshold for 'large files'."""
        pass

    @abstractmethod
    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """
        Perform stack-specific analysis.

        Args:
            root: Repository root path
            files: List of file paths (filtered by extensions)
            metrics: Pre-computed file size metrics

        Returns:
            Dict with stack-specific issues, ghosts, flags
        """
        pass
