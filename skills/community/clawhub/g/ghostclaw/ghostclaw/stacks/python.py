"""Python (Django/FastAPI) stack analyzer with AST coupling."""

from typing import Dict, List
from ghostclaw.core.coupling import PythonImportAnalyzer
from .base import StackAnalyzer


class PythonAnalyzer(StackAnalyzer):
    """Analyzes Python projects for architectural issues using AST."""

    def get_extensions(self) -> List[str]:
        return ['.py']

    def get_large_file_threshold(self) -> int:
        return 300

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Run Python-specific architectural checks including AST import analysis."""
        issues = []
        ghosts = []
        flags = []

        # AST-based coupling analysis (the only thing this analyzer contributes)
        try:
            analyzer = PythonImportAnalyzer(root)
            coupling_report = analyzer.analyze()

            # Merge coupling issues (these come from AST, not rules)
            issues.extend(coupling_report.get('issues', []))
            ghosts.extend(coupling_report.get('architectural_ghosts', []))
            flags.extend(coupling_report.get('red_flags', []))
            coupling_metrics = coupling_report.get('coupling_metrics', {})
        except Exception as e:
            coupling_metrics = {}
            issues.append(f"AST analysis failed: {str(e)}")

        # Note: File size metrics are handled by validator rules, not here

        return {
            "stack": "python",
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "coupling_metrics": coupling_metrics
        }
