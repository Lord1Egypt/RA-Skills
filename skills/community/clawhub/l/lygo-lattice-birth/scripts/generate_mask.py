#!/usr/bin/env python3
"""Generate masked lattice identity via in-process lygo_lattice_birth import."""

from __future__ import annotations

import argparse
import json
import sys

from _stack_paths import resolve_stack_root
from _stack_tools import load_tool


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate masked LYGO identity (local vault)")
    ap.add_argument("--slug", default="builder", help="Local-only slug — never published")
    ap.add_argument("--show-consent", action="store_true", help="Include consent in output (vault only)")
    args = ap.parse_args()

    stack = resolve_stack_root()
    birth = load_tool(stack, "lygo_lattice_birth.py")
    ns = argparse.Namespace(
        consent=None,
        slug=args.slug,
        show_consent=args.show_consent,
    )
    return int(birth.cmd_generate_mask(ns))


if __name__ == "__main__":
    raise SystemExit(main())