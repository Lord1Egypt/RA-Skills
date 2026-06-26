#!/usr/bin/env python3
"""
Example: Using MMOutput with PosterGen
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mm_output import MMOutputGenerator


def example_standalone():
    html_files = [
        "output/poster_llm.html",
        "output/poster_preview.html"
    ]
    
    output_dir = "output/mm_outputs"
    
    with MMOutputGenerator() as gen:
        for html_path in html_files:
            if Path(html_path).exists():
                print(f"\nProcessing: {html_path}")
                results = gen.convert_all(
                    html_path,
                    output_dir,
                    base_name=Path(html_path).stem
                )
                print("Generated:")
                for fmt, path in results.items():
                    print(f"  - {fmt}: {path}")


if __name__ == "__main__":
    example_standalone()
