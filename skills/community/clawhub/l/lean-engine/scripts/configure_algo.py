#!/usr/bin/env python3
"""
configure_algo.py — Create a backtest-ready config from a LEAN config template.

Reads a source config.json, updates algorithm fields, and writes to a
separate output file. The original config is NEVER modified.

Usage:
  python3 configure_algo.py <source_config> <output_config> <class_name> <file_name>

Example:
  python3 configure_algo.py config.json config.backtest.json MyAlgo MyAlgo.py
"""

import re
import sys


def main():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <source_config> <output_config> <class_name> <algo_file>")
        sys.exit(1)

    source, output, algo_class, algo_file = sys.argv[1:5]

    with open(source, "r") as f:
        content = f.read()

    # Replace algorithm-type-name
    content = re.sub(
        r'"algorithm-type-name"\s*:\s*"[^"]*"',
        f'"algorithm-type-name": "{algo_class}"',
        content,
    )

    # Replace algorithm-language
    content = re.sub(
        r'"algorithm-language"\s*:\s*"[^"]*"',
        '"algorithm-language": "Python"',
        content,
    )

    # Replace algorithm-location
    content = re.sub(
        r'"algorithm-location"\s*:\s*"[^"]*"',
        f'"algorithm-location": "../../../Algorithm.Python/{algo_file}"',
        content,
    )

    # Ensure backtesting environment
    content = re.sub(
        r'"environment"\s*:\s*"[^"]*"',
        '"environment": "backtesting"',
        content,
    )

    with open(output, "w") as f:
        f.write(content)

    print(f"✅ Config written to {output}")
    print(f"   Class: {algo_class}")
    print(f"   File:  {algo_file}")
    print(f"   Mode:  backtesting")
    print(f"   Source config unchanged: {source}")


if __name__ == "__main__":
    main()
