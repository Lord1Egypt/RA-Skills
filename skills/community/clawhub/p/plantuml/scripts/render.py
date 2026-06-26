#!/usr/bin/env python3
"""PlantUML diagram renderer wrapper.

Usage:
  python3 render.py <file.puml> [options]

Options:
  --format FORMAT   Output format: png (default), svg, pdf, eps, txt, utxt
  --output DIR      Output directory (default: same as source)
  --limit SIZE      Max image dimension (default: 16384)
  --verbose         Enable verbose output
"""

import subprocess
import sys
import os
from pathlib import Path

PLANTUML_JAR = os.path.expanduser("~/tools/plantuml.jar")

def render(puml_file, fmt="png", output_dir=None, limit=16384, verbose=False):
    puml_path = Path(puml_file).resolve()
    if not puml_path.exists():
        print(f"Error: {puml_file} not found", file=sys.stderr)
        sys.exit(1)

    cmd = ["java"]
    if limit:
        cmd.append(f"-DPLANTUML_LIMIT_SIZE={limit}")
    cmd.extend(["-jar", PLANTUML_JAR])
    cmd.extend([f"-t{fmt}", "-charset", "UTF-8"])
    if output_dir:
        cmd.extend(["-o", str(Path(output_dir).resolve())])
    if verbose:
        cmd.append("-v")
    cmd.append(str(puml_path))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"PlantUML error:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    # Find output file
    if verbose:
        for line in result.stderr.splitlines():
            if "Creating file:" in line or "Creating image" in line:
                print(line)

    # Guess output filename from @startuml label
    with open(puml_path) as f:
        for line in f:
            if line.strip().startswith("@startuml"):
                diagram_name = line.strip().split(None, 1)[1] if len(line.strip().split()) > 1 else puml_path.stem
                out_dir = output_dir or str(puml_path.parent)
                out_file = Path(out_dir) / f"{diagram_name}.{fmt}"
                if out_file.exists() and out_file.stat().st_size > 0:
                    print(f"Output: {out_file}")
                    return str(out_file)

    # Fallback: check for same-name file
    out_dir = output_dir or str(puml_path.parent)
    out_file = Path(out_dir) / f"{puml_path.stem}.{fmt}"
    if out_file.exists() and out_file.stat().st_size > 0:
        print(f"Output: {out_file}")
        return str(out_file)

    print(f"Warning: Could not locate output file", file=sys.stderr)
    return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Render PlantUML diagrams")
    parser.add_argument("puml_file", help="PlantUML source file")
    parser.add_argument("--format", default="png", help="Output format (png, svg, pdf, eps, txt)")
    parser.add_argument("--output", default=None, help="Output directory")
    parser.add_argument("--limit", type=int, default=16384, help="Max image dimension")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    render(args.puml_file, args.format, args.output, args.limit, args.verbose)
