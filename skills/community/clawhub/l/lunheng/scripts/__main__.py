#!/usr/bin/env python3
"""lunheng CLI — Unified entry point for all tools.

Usage:
  python -m scripts <command> [args...]

Commands:
  pipeline        Run the full draft→review pipeline
  law-check       Check law citations for validity
  quality-check   Review a judgment for quality issues
  consistency     Check logical consistency of a judgment
  parse           Parse a judgment document into structured data
  fee-calc        Calculate court fees
  shape-spirit    Search the 形与神 reference corpus
  npc-law         Query NPC (全国人大) law database
  moj-law         Query MOJ (司法部) law database
  serve           Start the REST API server
"""

import sys
import os

# Ensure scripts/ is on the path for intra-package imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    # Shift args so sys.argv[0] becomes the subcommand
    sys.argv = [sys.argv[0] + " " + command] + sys.argv[2:]

    commands = {
        "pipeline": ("pipeline", "main"),
        "law-check": ("law_checker", "main"),
        "quality-check": ("quality_checker", "main"),
        "consistency": ("consistency_checker", "main"),
        "parse": ("enhanced_parser", "main"),
        "fee-calc": ("fee_calculator", "main"),
        "shape-spirit": ("shape_spirit_index", None),
        "npc-law": ("npc_law_api", "main"),
        "moj-law": ("moj_law_api", None),
        "serve": ("server", "main"),
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)

    module_name, func_name = commands[command]
    try:
        mod = __import__(module_name)
        if func_name:
            getattr(mod, func_name)()
        # If no main() function, the module's __name__ block runs on import
        # when invoked as `python -m scripts <command>` — but since we
        # already imported it, we need to call its inline logic directly.
        # For moj_law_api and shape_spirit_index, the __name__ block
        # handles CLI args via sys.argv which we already set above.
        if func_name is None:
            # Re-execute the module's script logic
            import runpy
            runpy.run_module(f"scripts.{module_name}", run_name="__main__")
    except Exception as e:
        print(f"Error in {command}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
