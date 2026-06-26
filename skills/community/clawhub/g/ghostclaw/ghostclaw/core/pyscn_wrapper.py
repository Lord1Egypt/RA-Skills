"""
Wrapper for pyscn to leverage faster dead code and clone detection.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


class PySCNAnalyzer:
    """Wrapper for the pyscn command-line tool."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def is_available(self) -> bool:
        """Check if pyscn is installed and accessible."""
        try:
            subprocess.run(["pyscn", "--version"], capture_output=True, check=False)
            return True
        except FileNotFoundError:
            return False

    def analyze(self) -> Dict:
        """Run pyscn analysis and return structured results."""
        if not self.is_available():
            return {"error": "pyscn not installed"}

        try:
            # Running pyscn with json output if supported,
            # or parsing its output. Assuming it has a basic CLI for now.
            # In a real scenario, we'd use its specific flags.
            result = subprocess.run(
                ["pyscn", "analyze", str(self.repo_path), "--json"],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"raw_output": result.stdout}
            else:
                return {"error": f"pyscn failed with return code {result.returncode}", "stderr": result.stderr}

        except Exception as e:
            return {"error": str(e)}

    def get_dead_code(self) -> List[str]:
        """Extract dead code reports from pyscn output."""
        # Implementation depends on pyscn's output format
        # Placeholder for now
        return []

    def get_clones(self) -> List[Dict]:
        """Extract code clone reports from pyscn output."""
        # Placeholder for now
        return []
