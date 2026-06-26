# Papyrus Tool — Hermes Agent Integration
#
# Copy this file to your Hermes tools directory.
# Hermes auto-discovers Python tool modules.
#
# Usage:
#   from papyrus_tool import PapyrusTool
#   tool = PapyrusTool(papyrus_home="/path/to/papyrus")

import os
import subprocess
from typing import Optional


class PapyrusTool:
    """Academic paper deep-read tool for Hermes agent.

    Fetches arXiv papers, converts figures to PNG, renders LaTeX formulas,
    and builds annotated bilingual PDFs with Kami-styled typesetting.
    """

    def __init__(self, papyrus_home: str = None):
        self.home = papyrus_home or os.path.expanduser(
            "~/.openclaw/skills/papyrus"
        )
        self.cli = os.path.join(self.home, "SCRIPTS", "papyrus")

    def _run(self, *args, timeout: int = 300) -> str:
        """Execute a papyrus CLI command."""
        cmd = ["bash", self.cli, *args]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            return f"ERROR: {result.stderr}"
        return result.stdout

    def fetch(self, arxiv_url: str, output_dir: str = "/tmp/papyrus_work") -> str:
        """Download and extract arXiv paper source.
        
        Args:
            arxiv_url: Full arXiv URL (e.g. https://arxiv.org/abs/2502.11089)
            output_dir: Directory to extract source files
        """
        return self._run("fetch", arxiv_url, output_dir)

    def figures(self, figure_dir: str, output_dir: str = "/tmp/papyrus_figures") -> str:
        """Convert PDF figures to PNG for Web embedding.
        
        Args:
            figure_dir: Directory containing PDF figure files
            output_dir: Output directory for PNG figures
        """
        return self._run("figures", figure_dir, output_dir)

    def formulas(self, formulas_file: str, output_dir: str = "/tmp/papyrus_formulas") -> str:
        """Render LaTeX formulas to PNG images.
        
        Args:
            formulas_file: Text file with LaTeX formulas (one per line)
            output_dir: Output directory for PNG formula images
        """
        return self._run("formulas", formulas_file, output_dir)

    def pdf(self, html_file: str, output_pdf: str) -> str:
        """Convert annotated HTML to final PDF.
        
        Args:
            html_file: Path to annotated HTML file
            output_pdf: Output PDF file path
        """
        return self._run("pdf", html_file, output_pdf)


# Hermes auto-discovery: expose tool instance
papyrus = PapyrusTool()

if __name__ == "__main__":
    # Quick test
    import sys
    if len(sys.argv) < 2:
        print("Usage: python papyrus_tool.py <fetch|figures|formulas|pdf> [args...]")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    result = getattr(papyrus, cmd)(*args)
    print(result)
