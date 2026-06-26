#!/usr/bin/env python3
"""Merge multiple PDF files into one."""

import sys
from pypdf import PdfMerger


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_merge.py <output.pdf> <input1.pdf> [input2.pdf ...]", file=sys.stderr)
        sys.exit(1)

    output = sys.argv[1]
    inputs = sys.argv[2:]

    merger = PdfMerger()
    for path in inputs:
        merger.append(path)
    merger.write(output)
    merger.close()
    print(f"Merged {len(inputs)} files → {output}")


if __name__ == "__main__":
    main()
