"""Node.js / React / TypeScript stack analyzer with coupling."""

from typing import Dict, List
from ghostclaw.core.node_coupling import NodeImportAnalyzer
from .base import StackAnalyzer


class NodeAnalyzer(StackAnalyzer):
    """Analyzes Node.js projects for architectural issues."""

    def get_extensions(self) -> List[str]:
        return ['.ts', '.tsx', '.js', '.jsx']

    def get_large_file_threshold(self) -> int:
        return 400

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Run Node-specific architectural checks including import coupling."""
        issues = []
        ghosts = []
        flags = []

        # AST-based coupling analysis (the only thing this analyzer contributes)
        try:
            analyzer = NodeImportAnalyzer(root)
            coupling_report = analyzer.analyze()

            issues.extend(coupling_report.get('issues', []))
            ghosts.extend(coupling_report.get('architectural_ghosts', []))
            flags.extend(coupling_report.get('red_flags', []))
            coupling_metrics = coupling_report.get('coupling_metrics', {})
        except Exception as e:
            coupling_metrics = {}
            issues.append(f"Import analysis failed: {str(e)}")

        # File size metrics handled by validator rules

        return {
            "stack": "node",
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "coupling_metrics": coupling_metrics
        }
