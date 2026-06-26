#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({' '.join(cmd)}): {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def git_changed_files(repo: Path, base: str, head: str) -> list[str]:
    out = run(["git", "diff", "--name-only", f"{base}...{head}"], repo)
    return [line.strip() for line in out.splitlines() if line.strip()]


def detect_default_base(repo: Path) -> str:
    for candidate in ("upstream/main", "origin/main", "main"):
        result = subprocess.run(["git", "rev-parse", "--verify", candidate], cwd=repo, text=True, capture_output=True)
        if result.returncode == 0:
            return candidate
    return "main"


def classify(files: list[str]) -> dict:
    categories = {
        "docs": [],
        "ui": [],
        "ios": [],
        "android": [],
        "extensions": [],
        "gateway": [],
        "channels": [],
        "memory": [],
        "security": [],
        "tests": [],
        "skills": [],
        "misc": [],
    }

    for f in files:
        if f.startswith("docs/") or f in {"README.md", "CONTRIBUTING.md", "SECURITY.md", "VISION.md", "CHANGELOG.md"}:
            categories["docs"].append(f)
        elif f.startswith("ui/") or f.startswith("src/ui/"):
            categories["ui"].append(f)
        elif f.startswith("apps/ios/") or f.startswith("apps/macos/"):
            categories["ios"].append(f)
        elif f.startswith("apps/android/"):
            categories["android"].append(f)
        elif f.startswith("extensions/"):
            categories["extensions"].append(f)
        elif f.startswith("src/gateway") or f.startswith("src/daemon") or f.startswith("src/process"):
            categories["gateway"].append(f)
        elif any(seg in f for seg in ["telegram", "discord", "whatsapp", "slack", "signal", "imessage", "bluebubbles", "matrix", "line", "msteams", "irc", "zalo"]):
            categories["channels"].append(f)
        elif "memory" in f or "qmd" in f:
            categories["memory"].append(f)
        elif any(seg in f.lower() for seg in ["auth", "security", "secret", "token", "oauth", "webhook"]):
            categories["security"].append(f)
        elif ".test." in f or f.startswith("test/") or f.startswith("vitest"):
            categories["tests"].append(f)
        elif f.startswith("skills/"):
            categories["skills"].append(f)
        else:
            categories["misc"].append(f)

    return categories


def unique_ordered(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def recommended_commands(categories: dict, files: list[str]) -> list[str]:
    commands = []
    docs_only = files and all(f in categories["docs"] or f in categories["tests"] for f in files)

    if docs_only:
        commands.extend([
            "pnpm format:docs:check",
            "pnpm lint:docs",
            "pnpm docs:check-links",
        ])
        return unique_ordered(commands)

    commands.extend([
        "pnpm build",
        "pnpm check",
        "pnpm test",
    ])

    if categories["ui"]:
        commands.append("pnpm test:ui")
    if categories["ios"]:
        commands.extend(["pnpm ios:gen", "pnpm ios:build"])
    if categories["android"]:
        commands.extend(["pnpm android:lint", "pnpm android:test"])
    if categories["extensions"]:
        commands.append("pnpm test:extensions")
        if any("voice-call" in f for f in categories["extensions"]):
            commands.append("pnpm test:voicecall:closedloop")
    if categories["gateway"] or categories["security"] or categories["channels"]:
        commands.append("pnpm test:gateway")
    if categories["memory"]:
        commands.append("pnpm test:fast")
    if categories["docs"] and not docs_only:
        commands.extend(["pnpm format:docs:check", "pnpm lint:docs"])

    return unique_ordered(commands)


def maintainers(categories: dict) -> list[str]:
    owners = []
    if categories["memory"]:
        owners.append("Vignesh (@vignesh07) — Memory (QMD), formal modeling, TUI, IRC, Lobster")
    if categories["channels"]:
        if any("telegram" in f for f in categories["channels"]):
            owners.append("Jos (@joshp123) / Ayaan Zaidi (@obviyus) — Telegram")
        if any("discord" in f for f in categories["channels"]):
            owners.append("Shadow (@thewilloftheshadow) — Discord")
    if categories["gateway"]:
        owners.append("Josh Avant (@joshavant) / Jonathan Taylor (@visionik) — Gateway / ACP / core CLI")
    if categories["security"]:
        owners.append("Mariano Belinky (@mbelinky) / Vincent Koc (@vincentkoc) / Josh Avant (@joshavant) — Security/Auth")
    if categories["ui"]:
        owners.append("Val Alexander (@BunsDev) / Gustavo Madeira Santana (@gumadeiras) — UI/UX / web UI")
    if categories["ios"]:
        owners.append("Ayaan Zaidi (@obviyus) / Nimrod Gutman (@ngutman) / Mariano Belinky (@mbelinky) — iOS/macOS")
    if categories["extensions"] or categories["misc"]:
        owners.append("Peter Steinberger (@steipete) / appropriate subsystem maintainer based on touched area")
    return unique_ordered(owners)


def warnings(categories: dict, files: list[str]) -> list[str]:
    out = []
    if categories["ui"]:
        out.append("Include before/after screenshots for UI or visual changes.")
        out.append("Keep Control UI decorators in legacy style (`@state() foo = ...`, `@property(...) count = ...`).")
    if categories["security"]:
        out.append("Keep the PR tightly scoped and explain impact/risk clearly; security/auth changes deserve extra review.")
    if categories["skills"] and len(files) == len(categories["skills"]):
        out.append("Skill contributions belong on ClawHub; only send core-repo skill changes here if they are part of OpenClaw itself.")
    if categories["docs"] and len(files) == len(categories["docs"]):
        out.append("Docs-only changes can usually skip the full build/test path; run docs checks instead.")
    out.append("Mark AI-assisted work in the PR title or description and state the testing level.")
    out.append("Keep the PR focused: one bugfix/feature per PR; use Discussions first for new features or architecture changes.")
    return unique_ordered(out)


def main():
    parser = argparse.ArgumentParser(description="Recommend OpenClaw validation commands and PR notes from a repo diff.")
    parser.add_argument("--repo", default=".", help="Path to the OpenClaw git repo")
    parser.add_argument("--base", help="Base ref for git diff (default: upstream/main if available)")
    parser.add_argument("--head", default="HEAD", help="Head ref for git diff (default: HEAD)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"Not a git repo: {repo}")
    if not (repo / "CONTRIBUTING.md").exists() or not (repo / "package.json").exists():
        raise SystemExit(f"Repo does not look like OpenClaw: {repo}")

    base = args.base or detect_default_base(repo)
    files = git_changed_files(repo, base, args.head)
    categories = classify(files)
    data = {
        "repo": str(repo),
        "base": base,
        "head": args.head,
        "changedFiles": files,
        "categories": {k: v for k, v in categories.items() if v},
        "recommendedCommands": recommended_commands(categories, files),
        "maintainersToConsider": maintainers(categories),
        "warnings": warnings(categories, files),
    }

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(f"Repo: {data['repo']}")
    print(f"Diff: {base}...{args.head}")
    print()
    print("Changed files:")
    if files:
        for f in files:
            print(f"- {f}")
    else:
        print("- (none)")
    print()
    print("Recommended commands:")
    for cmd in data["recommendedCommands"]:
        print(f"- {cmd}")
    print()
    print("Maintainers to consider:")
    if data["maintainersToConsider"]:
        for owner in data["maintainersToConsider"]:
            print(f"- {owner}")
    else:
        print("- No subsystem-specific maintainer hint; use normal reviewer flow.")
    print()
    print("Warnings / PR notes:")
    for note in data["warnings"]:
        print(f"- {note}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
