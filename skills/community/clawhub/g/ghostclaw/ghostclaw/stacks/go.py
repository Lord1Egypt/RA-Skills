"""Go stack analyzer (basic implementation)."""

from typing import Dict, List
from .base import StackAnalyzer


class GoAnalyzer(StackAnalyzer):
    """Analyzes Go projects for architectural issues (stub for now)."""

    def get_extensions(self) -> List[str]:
        return ['.go']

    def get_large_file_threshold(self) -> int:
        return 500

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Basic Go analysis (to be enhanced)."""
        return {
            "stack": "go",
            "issues": [],
            "architectural_ghosts": [],
            "red_flags": [],
            "notes": ["Go detection not yet implemented"]
        }
