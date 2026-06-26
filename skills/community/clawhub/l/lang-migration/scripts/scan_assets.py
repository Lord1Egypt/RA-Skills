#!/usr/bin/env python3
"""
scan_assets.py — Phase 1 asset scanner for lang-migration skill.

Usage:
    python scan_assets.py --source <source_dir> --output <path/to/asset-inventory.yaml>

Generates a starter asset-inventory.yaml by walking the source directory.
The AI agent then fills in `purpose`, `migration_strategy`, and other fields.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)

# Maps file extension to likely asset type
EXTENSION_TYPE_MAP = {
    # Source code
    ".py": "source_code", ".go": "source_code", ".rs": "source_code",
    ".c": "source_code", ".cpp": "source_code", ".cc": "source_code",
    ".h": "source_code", ".hpp": "source_code",
    ".ts": "source_code", ".js": "source_code", ".jsx": "source_code", ".tsx": "source_code",
    ".zig": "source_code", ".rb": "source_code", ".java": "source_code",
    ".cs": "source_code", ".swift": "source_code", ".kt": "source_code",

    # Test fixtures / data
    ".npy": "test_fixture", ".npz": "test_fixture",
    ".csv": "test_fixture", ".tsv": "test_fixture",
    ".json": "asset_text",  # may be test fixture or config — AI to determine
    ".jsonl": "test_fixture",
    ".pkl": "test_fixture", ".pickle": "test_fixture",
    ".parquet": "test_fixture", ".arrow": "test_fixture",
    ".bin": "asset_binary", ".dat": "asset_binary",

    # Documentation
    ".md": "documentation", ".rst": "documentation",
    ".txt": "documentation", ".tex": "documentation",
    ".pdf": "documentation",

    # Build config
    "Makefile": "build_config", "CMakeLists.txt": "build_config",
    ".toml": "build_config",  # Cargo.toml, pyproject.toml — AI to refine
    ".gradle": "build_config", "build.gradle": "build_config",
    ".gradle.kts": "build_config",

    # Dependency manifests
    "requirements.txt": "dependency_manifest",
    "requirements-dev.txt": "dependency_manifest",
    "Pipfile": "dependency_manifest", "Pipfile.lock": "dependency_manifest",
    "poetry.lock": "dependency_manifest",
    "go.mod": "dependency_manifest", "go.sum": "dependency_manifest",
    "Cargo.lock": "dependency_manifest",
    "package.json": "dependency_manifest", "package-lock.json": "dependency_manifest",
    "yarn.lock": "dependency_manifest", "bun.lockb": "dependency_manifest",

    # Environment / config
    # Both .yml and .yaml default to environment_config (strategy: preserve).
    # The classify_file() refine block promotes .github/workflows/*.yml|yaml → ci_config.
    ".env": "environment_config", ".env.example": "environment_config",
    ".yml": "environment_config",
    ".yaml": "environment_config",
    "Dockerfile": "environment_config",
    "docker-compose.yml": "environment_config",
    "docker-compose.yaml": "environment_config",

    # Scripts
    ".sh": "script", ".bash": "script", ".zsh": "script",
    ".ps1": "script", ".bat": "script", ".cmd": "script",

    # Images / media
    ".png": "asset_binary", ".jpg": "asset_binary", ".jpeg": "asset_binary",
    ".gif": "asset_binary", ".svg": "asset_text",
    ".mp4": "asset_binary", ".avi": "asset_binary",
}

# Files/dirs to always skip
SKIP_PATTERNS = {
    ".git", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".venv", "venv", "env", ".env",
    "dist", "build", "target", "_build", ".build",
    ".DS_Store", "Thumbs.db",
    "migration_workspace",  # skip our own workspace
}

# Files where migration_strategy can be pre-assigned with high confidence
STRATEGY_HINTS = {
    "requirements.txt": "adapt",
    "requirements-dev.txt": "adapt",
    "Pipfile": "adapt",
    "Cargo.toml": "adapt",
    "go.mod": "adapt",
    "package.json": "adapt",
    "pyproject.toml": "adapt",
    "Makefile": "adapt",
    "CMakeLists.txt": "adapt",
    "Dockerfile": "adapt",
    "docker-compose.yml": "adapt",
    "docker-compose.yaml": "adapt",
    ".gitignore": "preserve",
    ".gitattributes": "preserve",
    "LICENSE": "preserve",
    "CHANGELOG.md": "preserve",
    "CONTRIBUTING.md": "preserve",
}

# Test-related name patterns
TEST_PATTERNS = ["test_", "_test.", "spec.", "_spec.", "tests/", "test/", "spec/"]


def classify_file(rel_path: str) -> dict:
    """Classify a single file and return a starter inventory entry."""
    path = Path(rel_path)
    name = path.name
    suffix = path.suffix.lower()
    parts = rel_path.replace("\\", "/").split("/")

    # Determine type
    file_type = EXTENSION_TYPE_MAP.get(name) or EXTENSION_TYPE_MAP.get(suffix, "other")

    # Refine: is this a test file?
    is_test = any(p in rel_path for p in TEST_PATTERNS)
    if is_test and file_type == "source_code":
        file_type = "test_code"

    # Refine: .github/workflows/*.yml is CI
    if ".github/workflows" in rel_path and suffix in (".yml", ".yaml"):
        file_type = "ci_config"

    # Determine migration strategy hint
    strategy = STRATEGY_HINTS.get(name, "")
    if not strategy:
        if file_type == "source_code":
            strategy = "translate"
        elif file_type == "test_code":
            strategy = "translate"
        elif file_type == "test_fixture":
            strategy = "direct_use"
        elif file_type == "documentation":
            strategy = "reference_only"
        elif file_type == "asset_binary":
            strategy = "direct_use"
        elif file_type == "ci_config":
            strategy = "adapt"
        elif file_type == "build_config":
            strategy = "adapt"
        elif file_type == "dependency_manifest":
            strategy = "adapt"
        elif file_type == "environment_config":
            strategy = "preserve"
        elif file_type == "script":
            strategy = "adapt"
        else:
            strategy = "preserve"

    # Docs that mention algorithms should be marked p3_required
    p3 = file_type in ("documentation",) and any(
        kw in name.lower() for kw in ["algo", "math", "design", "spec", "note", "theory"]
    )

    return {
        "path": rel_path,
        "type": file_type,
        "purpose": "",   # AI must fill this in
        "migration_strategy": strategy,
        "depends_on_ecosystem": [],
        "status": "TODO",
        "target_path": "",
        "notes": f"[AUTO-CLASSIFIED: review and confirm type={file_type}, strategy={strategy}]",
        "p3_required": p3,
    }


def scan(source_dir: str, output_path: str):
    source = Path(source_dir).resolve()
    assets = []
    skipped = []

    for root, dirs, files in os.walk(source):
        # Prune skip dirs in-place
        dirs[:] = [d for d in dirs if d not in SKIP_PATTERNS]

        for fname in sorted(files):
            if fname in SKIP_PATTERNS:
                continue
            abs_path = Path(root) / fname
            rel_path = str(abs_path.relative_to(source))
            entry = classify_file(rel_path)
            assets.append(entry)

    # Count by strategy
    by_strategy = {}
    for a in assets:
        s = a["migration_strategy"]
        by_strategy[s] = by_strategy.get(s, 0) + 1

    inventory = {
        "meta": {
            "scanned_at": datetime.now().isoformat(),
            "total_files": len(assets),
            "by_strategy": by_strategy,
            "note": (
                "Auto-generated by scan_assets.py. "
                "AI agent must review every entry: fill in 'purpose', "
                "confirm 'migration_strategy', populate 'depends_on_ecosystem'."
            ),
        },
        "assets": assets,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(inventory, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Scanned {len(assets)} files → {output_path}")
    print("By strategy:")
    for strategy, count in sorted(by_strategy.items()):
        print(f"  {strategy:20s} {count}")
    print("\nNext: AI agent reviews each entry, fills 'purpose' and confirms strategy.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lang-migration asset scanner")
    parser.add_argument("--source", required=True, help="Path to source project root")
    parser.add_argument("--output", required=True, help="Path to write asset-inventory.yaml")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: source dir not found: {args.source}")
        raise SystemExit(1)

    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    scan(args.source, args.output)
