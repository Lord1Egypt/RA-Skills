#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Inspect a Promptfoo workspace and suggest next steps.")
    parser.add_argument("path", nargs="?", default=".", help="Workspace path")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    config = root / "promptfooconfig.yaml"
    env = root / ".env"
    prompt_files = sorted(root.glob("*.txt"))
    docs_dir = root / "docs"
    agents_dir = root / "agents"
    tools_dir = root / "tools"

    print(f"Workspace: {root}")
    print()

    if config.exists():
        print("[OK] Found promptfooconfig.yaml")
        print("Next: promptfoo validate")
    else:
        print("[WARN] No promptfooconfig.yaml found")
        print("Next: generate one with scaffold-promptfoo-config.py or run `promptfoo init`")

    if env.exists():
        print("[OK] Found .env")
    else:
        print("[INFO] No .env found; provider credentials may need environment variables")

    if prompt_files:
        print(f"[INFO] Found text prompt files: {', '.join(p.name for p in prompt_files[:8])}")
    else:
        print("[INFO] No top-level .txt prompt files found")

    if docs_dir.exists():
        print("[INFO] Found docs/ directory; repo may be a good fit for RAG evals with file://docs/... context")

    if agents_dir.exists() or tools_dir.exists():
        print("[INFO] Found agents/ or tools/ directory; repo may be a good fit for agent-style provider configs")

    print()
    print("Suggested command ladder:")
    if config.exists():
        print("1. promptfoo validate")
        print("2. promptfoo eval --filter-first-n 5")
        print("3. promptfoo view")
    else:
        print("1. scaffold-promptfoo-config.py <basic|compare|rag|agent|redteam>")
        print("2. edit promptfooconfig.yaml")
        print("3. promptfoo validate")
        print("4. promptfoo eval --filter-first-n 5")


if __name__ == "__main__":
    main()
