"""
Progress display for image-works.
Simple progress bar for batch processing.
"""
import sys
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ProgressBar:
    """Simple progress bar for batch processing."""
    
    def __init__(self, total: int, width: int = 40, prefix: str = "Processing"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
        self._last_output = ""
    
    def update(self, current: int, current_file: Optional[str] = None):
        """Update progress bar."""
        self.current = min(current, self.total)
        fraction = self.current / self.total if self.total > 0 else 0
        filled = int(self.width * fraction)
        bar = "█" * filled + "░" * (self.width - filled)
        
        pct = fraction * 100
        filename = f" ({os.path.basename(current_file)})" if current_file else ""
        
        line = f"\r{self.prefix}: |{bar}| {self.current}/{self.total} ({pct:.0f}%){filename}"
        sys.stdout.write(line)
        sys.stdout.flush()
        self._last_output = line
    
    def finish(self):
        """Complete the progress display."""
        self.update(self.total)
        sys.stdout.write("\n")
        sys.stdout.flush()


import os


def display_processing(files: list, results: list) -> str:
    """
    Display processing progress as a text-based progress bar.
    Returns the final progress line.
    """
    total = len(files)
    processed = len([r for r in results if r.get("status") == "success"])
    failed = len([r for r in results if r.get("status") == "failed"])
    
    bar_width = 30
    fraction = processed / total if total > 0 else 0
    filled = int(bar_width * fraction)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    return f"Processing: |{bar}| {processed}/{total} ({fraction * 100:.0f}%) | ✅ {processed} ❌ {failed}"
