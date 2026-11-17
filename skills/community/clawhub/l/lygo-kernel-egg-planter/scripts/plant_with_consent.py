#!/usr/bin/env python3
"""Plant kernel eggs — consent + trusted stack + mandatory post-plant verify. Core path only."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _stack_paths import require_consent, resolve_stack_root  # noqa: E402

# Only these stack tool basenames may be executed (allowlist)
ALLOWED_STACK_TOOLS = frozenset(
    {
        "build_kernel_eggs.py",
        "anchor_kernel_eggs.py",
        "verify_kernel_eggs.py",
        "retrieve_kernel_egg.py",
    }
)


def run_verify(stack: Path) -> int:
    return subprocess.call(
        [sys.executable, str(SCRIPT_DIR / "verify_eggs.py"), "--stack-root", str(stack)]
    )


def run_stack_tool(stack: Path, name: str, extra: list[str] | None = None) -> None:
    if name not in ALLOWED_STACK_TOOLS:
        raise SystemExit(f"Refusing non-allowlisted stack tool: {name}")
    tool = stack / "tools" / name
    if not tool.is_file():
        raise SystemExit(f"Missing stack tool: {tool}")
    # Soft integrity: must live under stack/tools and be .py
    if tool.suffix != ".py" or ".." in tool.parts:
        raise SystemExit(f"Invalid tool path: {tool}")
    cmd = [sys.executable, str(tool)]
    if extra:
        cmd.extend(extra)
    subprocess.check_call(cmd, cwd=stack)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Core kernel egg planter: preflight → build → anchor → mandatory verify. "
            "Does not run champions/stubs/catalog side workflows (use dedicated scripts). "
            "Never git-push / clawhub.ai publish / social."
        )
    )
    ap.add_argument("--i-consent", action="store_true", help="Required plant consent")
    ap.add_argument(
        "--i-trust-stack",
        action="store_true",
        help="Required: affirm LYGO_STACK_ROOT is a stack you control (executable trust)",
    )
    ap.add_argument("--stack-root", default=None)
    ap.add_argument(
        "--local-only",
        action="store_true",
        help="Skip Turbo/permaweb; local CA + registry only (recommended default for most users)",
    )
    ap.add_argument("--dry-run", action="store_true")
    # Legacy surfaces: only local/turbo/registry affect core; others print redirect
    ap.add_argument(
        "--surfaces",
        default="local,registry",
        help="local,turbo,registry (pages/clawhub/champions/stubs redirect to dedicated scripts)",
    )
    args = ap.parse_args()
    require_consent(args.i_consent)

    if not args.i_trust_stack:
        print(
            "Stack trust required: --i-trust-stack (you must control LYGO_STACK_ROOT; "
            "this skill executes allowlisted tools under that root).",
            file=sys.stderr,
        )
        return 2

    stack = resolve_stack_root(args.stack_root)
    subprocess.check_call([sys.executable, str(SCRIPT_DIR / "preflight.py"), "--stack-root", str(stack)])

    surfaces = {s.strip().lower() for s in args.surfaces.split(",") if s.strip()}
    # Redirect expanded surfaces — keep function via separate scripts, not silent expansion
    redirects = {
        "clawhub": "python scripts/plant_clawhub_catalog.py --i-consent --stack-root <STACK>",
        "champions": "python scripts/plant_champion_council.py --i-consent",
        "stubs": "python scripts/write_book_brain_stubs.py --i-consent --stack-root <STACK>",
        "pages": "prepare docs/KernelEggRegistry.json after plant; human git push",
    }
    for s, hint in redirects.items():
        if s in surfaces:
            print(f"[redirect] surface '{s}' is not inlined in core planter — run: {hint}")

    use_turbo = "turbo" in surfaces and not args.local_only

    print("Δ9Φ963 Kernel Egg Planter v1.3.1 (core)")
    print(f"  stack: {stack}")
    print(f"  turbo: {use_turbo}")
    print("  verify: ALWAYS")
    print("  publish: NEVER from this skill")

    reg_path = stack / "data" / "kernel_eggs" / "registry.json"
    if reg_path.is_file() and not args.dry_run:
        print("[*] Pre-plant tamper verify (baseline)")
        if run_verify(stack) != 0:
            print("[FAIL] Pre-plant verify QUARANTINE", file=sys.stderr)
            return 1

    if args.dry_run:
        print("[dry-run] would run allowlisted build + anchor + verify")
        return 0

    run_stack_tool(stack, "build_kernel_eggs.py")
    anchor_extra = ["--local-only"] if not use_turbo else []
    run_stack_tool(stack, "anchor_kernel_eggs.py", anchor_extra)

    if run_verify(stack) != 0:
        print("[FAIL] Post-plant verify QUARANTINE — do not distribute", file=sys.stderr)
        return 1

    if "pages" in surfaces:
        src = stack / "docs" / "KernelEggRegistry.json"
        if src.is_file():
            print(f"[pages] ready at {src} — human must git push")

    if reg_path.is_file():
        data = json.loads(reg_path.read_text(encoding="utf-8"))
        print(f"[done] registry_merkle_root={data.get('registry_merkle_root', '')}")
        print("[done] ALIGNED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
