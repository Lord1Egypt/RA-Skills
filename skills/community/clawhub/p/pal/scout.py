#!/usr/bin/env python3

"""
scout.py — Project Scout
========================
Called by the OpenClaw skill to gather raw facts about a project.
Outputs structured JSON so the agent can format it for any chat channel.

Usage:
  python3 scout.py --path /path/to/project
  python3 scout.py --path . --json     # machine-readable output
  python3 scout.py --path . --text     # human-readable text (default)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

SKIP_DIRS = {
    ".git", ".svn", ".hg",
    "node_modules", "__pycache__", ".venv", "venv", "env", ".env",
    ".tox", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".hypothesis",
    "dist", "build", "target", ".next", ".nuxt", ".output", "out",
    ".idea", ".vscode",
    "coverage", "htmlcov", ".coverage",
    "vendor", "third_party", "bower_components",
    ".turbo", ".vercel", ".netlify",
}

# Files we always try to read (in priority order)
PRIORITY_FILES = [
    "README.md", "README.rst", "README.txt", "readme.md",
    "CLAUDE.md", ".claude/CLAUDE.md",
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "go.sum",
    "pom.xml", "build.gradle", "build.gradle.kts",
    "composer.json", "Gemfile",
    "docker-compose.yml", "docker-compose.yaml", "Dockerfile",
    "Makefile", "justfile", "Taskfile.yml",
    ".env.example", ".env.sample", ".env.template",
    "requirements.txt", "requirements-dev.txt", "Pipfile", "uv.lock",
    "tsconfig.json", "jsconfig.json",
    "vite.config.ts", "vite.config.js",
    "next.config.js", "next.config.ts",
    "webpack.config.js",
    "angular.json", "nuxt.config.ts",
]

# Extension → language label
EXT_LANGUAGE = {
    ".py": "Python", ".pyi": "Python",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".jsx": "TypeScript/React",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java", ".kt": "Kotlin", ".scala": "Scala",
    ".c": "C", ".h": "C",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".dart": "Dart",
    ".lua": "Lua",
    ".r": "R", ".R": "R",
    ".jl": "Julia",
    ".zig": "Zig",
    ".ex": "Elixir", ".exs": "Elixir",
    ".erl": "Erlang",
    ".hs": "Haskell",
    ".clj": "Clojure",
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell", ".fish": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".graphql": "GraphQL", ".gql": "GraphQL",
    ".proto": "Protobuf",
    ".tf": "Terraform", ".hcl": "HCL",
    ".yaml": "YAML", ".yml": "YAML",
    ".toml": "TOML",
    ".json": "JSON",
    ".html": "HTML", ".htm": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".sass": "SASS", ".less": "LESS",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".md": "Markdown", ".mdx": "Markdown",
}

# Framework fingerprints: file path fragment → framework label
FRAMEWORK_HINTS = {
    "next.config": "Next.js",
    "nuxt.config": "Nuxt.js",
    "angular.json": "Angular",
    "svelte.config": "SvelteKit",
    "vite.config": "Vite",
    "astro.config": "Astro",
    "remix.config": "Remix",
    "gatsby-config": "Gatsby",
    "expo/": "Expo (React Native)",
    "react-native": "React Native",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "rails": "Ruby on Rails",
    "laravel": "Laravel",
    "spring": "Spring",
    "express": "Express.js",
    "fastify": "Fastify",
    "nest": "NestJS",
    "tauri": "Tauri",
    "electron": "Electron",
    "cargo.toml": "Rust (Cargo)",
    "go.mod": "Go Modules",
    "docker-compose": "Docker Compose",
    "kubernetes": "Kubernetes",
    "terraform": "Terraform",
}

MAX_READ_LINES = 80
MAX_SAMPLE_FILES = 15
MAX_TREE_DEPTH = 4

# ── Helpers ───────────────────────────────────────────────────────────────────

def read_file(path: Path, max_lines: int = MAX_READ_LINES) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        if len(lines) <= max_lines:
            return text.strip()
        head = "\n".join(lines[:60])
        tail = "\n".join(lines[-15:])
        return f"{head}\n\n[... {len(lines) - 75} lines omitted ...]\n\n{tail}"
    except Exception as e:
        return f"[unreadable: {e}]"


def build_tree(root: Path, max_depth: int = MAX_TREE_DEPTH) -> str:
    lines = []

    def walk(path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return
        try:
            entries = sorted(
                path.iterdir(),
                key=lambda e: (e.is_file(), e.name.lower()),
            )
        except PermissionError:
            return

        visible = [e for e in entries if e.name not in SKIP_DIRS and not e.name.startswith(".")]

        for i, entry in enumerate(visible):
            last = i == len(visible) - 1
            connector = "└── " if last else "├── "
            size_hint = ""
            if entry.is_file():
                try:
                    s = entry.stat().st_size
                    if s > 1_000_000:
                        size_hint = f"  ({s // 1_000_000} MB)"
                    elif s > 10_000:
                        size_hint = f"  ({s // 1_000} KB)"
                except OSError:
                    pass
            lines.append(f"{prefix}{connector}{entry.name}{size_hint}")
            if entry.is_dir():
                ext = "    " if last else "│   "
                walk(entry, prefix + ext, depth + 1)

    walk(root)
    return "\n".join(lines) if lines else "(empty directory)"


def detect_frameworks(priority_content: dict, all_files: list) -> list:
    found = set()
    combined = " ".join(
        [k.lower() for k in priority_content.keys()]
        + [v.lower()[:500] for v in priority_content.values()]
    )
    file_names = " ".join(str(f).lower() for f in all_files)

    for hint, label in FRAMEWORK_HINTS.items():
        if hint in combined or hint in file_names:
            found.add(label)

    # package.json deep scan
    if "package.json" in priority_content:
        pkg = priority_content["package.json"].lower()
        for dep, label in [
            ('"react"', "React"), ('"vue"', "Vue"), ('"angular"', "Angular"),
            ('"svelte"', "Svelte"), ('"express"', "Express.js"),
            ('"fastify"', "Fastify"), ('"nestjs"', "NestJS"),
            ('"next"', "Next.js"), ('"nuxt"', "Nuxt.js"),
            ('"gatsby"', "Gatsby"), ('"remix"', "Remix"),
            ('"electron"', "Electron"), ('"tauri"', "Tauri"),
            ('"prisma"', "Prisma"), ('"mongoose"', "Mongoose"),
            ('"typeorm"', "TypeORM"), ('"drizzle-orm"', "Drizzle ORM"),
            ('"trpc"', "tRPC"), ('"graphql"', "GraphQL"),
        ]:
            if dep in pkg:
                found.add(label)

    # pyproject.toml / requirements.txt deep scan
    for fname in ["pyproject.toml", "requirements.txt", "Pipfile"]:
        if fname in priority_content:
            py = priority_content[fname].lower()
            for dep, label in [
                ("django", "Django"), ("flask", "Flask"), ("fastapi", "FastAPI"),
                ("starlette", "Starlette"), ("tornado", "Tornado"),
                ("celery", "Celery"), ("sqlalchemy", "SQLAlchemy"),
                ("pydantic", "Pydantic"), ("langchain", "LangChain"),
                ("anthropic", "Anthropic SDK"), ("openai", "OpenAI SDK"),
                ("numpy", "NumPy"), ("pandas", "Pandas"), ("pytorch", "PyTorch"),
                ("tensorflow", "TensorFlow"), ("scikit-learn", "scikit-learn"),
            ]:
                if dep in py:
                    found.add(label)

    return sorted(found)


def guess_entry_points(root: Path, all_files: list) -> list:
    candidates = []
    common_names = [
        "main.py", "app.py", "server.py", "run.py", "manage.py", "cli.py",
        "index.js", "index.ts", "main.js", "main.ts", "server.js", "server.ts",
        "app.js", "app.ts",
        "main.go", "cmd/main.go",
        "main.rs", "src/main.rs",
        "main.java", "Application.java",
        "index.html",
    ]
    for name in common_names:
        candidate = root / name
        if candidate.exists():
            candidates.append(str(candidate.relative_to(root)))

    # also look one level deep
    for f in all_files:
        rel = str(f.relative_to(root))
        parts = rel.split(os.sep)
        if len(parts) == 2 and parts[1] in common_names:
            if rel not in candidates:
                candidates.append(rel)

    return candidates[:5]


def extract_scripts(priority_content: dict) -> dict:
    scripts = {}
    if "package.json" in priority_content:
        try:
            import json as _json
            data = _json.loads(priority_content["package.json"])
            if "scripts" in data:
                scripts = {k: v for k, v in list(data["scripts"].items())[:8]}
        except Exception:
            pass

    run_hints = []
    for fname in ["Makefile", "justfile", "README.md", "README.rst"]:
        if fname in priority_content:
            content = priority_content[fname]
            for line in content.splitlines():
                ll = line.strip().lower()
                if any(kw in ll for kw in ["npm run", "python", "go run", "cargo run", "make ", "docker"]):
                    run_hints.append(line.strip())
            if run_hints:
                break

    return {"npm_scripts": scripts, "run_hints": run_hints[:6]}


# ── Main scanner ──────────────────────────────────────────────────────────────

def scan(root: Path) -> dict:
    result = {
        "root": str(root),
        "name": root.name,
        "tree": "",
        "priority_files": {},
        "lang_counts": {},
        "frameworks": [],
        "entry_points": [],
        "run_info": {},
        "source_samples": {},
        "total_files": 0,
        "errors": [],
    }

    # Walk all files
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
        ]
        for fname in filenames:
            all_files.append(Path(dirpath) / fname)

    result["total_files"] = len(all_files)

    # Count by language
    for f in all_files:
        lang = EXT_LANGUAGE.get(f.suffix.lower())
        if lang:
            result["lang_counts"][lang] = result["lang_counts"].get(lang, 0) + 1

    # Read priority files
    for name in PRIORITY_FILES:
        candidate = root / name
        if candidate.exists() and candidate.is_file():
            result["priority_files"][name] = read_file(candidate, max_lines=100)

    # Directory tree
    result["tree"] = build_tree(root)

    # Framework detection
    result["frameworks"] = detect_frameworks(result["priority_files"], all_files)

    # Entry points
    result["entry_points"] = guess_entry_points(root, all_files)

    # Run info
    result["run_info"] = extract_scripts(result["priority_files"])

    # Sample interesting source files not already in priority_files
    priority_names = set(result["priority_files"].keys())
    sampled = 0
    for f in sorted(all_files, key=lambda x: len(x.parts)):
        if sampled >= MAX_SAMPLE_FILES:
            break
        ext = f.suffix.lower()
        if ext not in EXT_LANGUAGE:
            continue
        rel = str(f.relative_to(root))
        if f.name in priority_names or rel in priority_names:
            continue
        if len(f.parts) - len(root.parts) > 5:
            continue
        try:
            sz = f.stat().st_size
            if sz < 50 or sz > 200_000:
                continue
        except OSError:
            continue
        result["source_samples"][rel] = read_file(f, max_lines=50)
        sampled += 1

    return result


def format_text(data: dict) -> str:
    """Human-readable output for direct terminal use."""
    lines = []
    lines.append(f"PROJECT SCOUT REPORT")
    lines.append(f"====================")
    lines.append(f"Project : {data['name']}")
    lines.append(f"Path    : {data['root']}")
    lines.append(f"Files   : {data['total_files']}")
    lines.append("")

    # Languages
    if data["lang_counts"]:
        top = sorted(data["lang_counts"].items(), key=lambda x: -x[1])[:8]
        lines.append("LANGUAGES")
        for lang, count in top:
            lines.append(f"  {lang}: {count} files")
        lines.append("")

    # Frameworks
    if data["frameworks"]:
        lines.append("FRAMEWORKS / LIBRARIES DETECTED")
        for fw in data["frameworks"]:
            lines.append(f"  • {fw}")
        lines.append("")

    # Entry points
    if data["entry_points"]:
        lines.append("LIKELY ENTRY POINTS")
        for ep in data["entry_points"]:
            lines.append(f"  • {ep}")
        lines.append("")

    # Run commands
    ri = data.get("run_info", {})
    if ri.get("npm_scripts"):
        lines.append("NPM SCRIPTS")
        for k, v in ri["npm_scripts"].items():
            lines.append(f"  npm run {k}  →  {v}")
        lines.append("")
    if ri.get("run_hints"):
        lines.append("RUN HINTS (from README/Makefile)")
        for h in ri["run_hints"]:
            lines.append(f"  {h}")
        lines.append("")

    # Directory tree
    lines.append("DIRECTORY STRUCTURE")
    lines.append(data["tree"])
    lines.append("")

    # Priority files
    if data["priority_files"]:
        lines.append("KEY FILES")
        lines.append("-" * 40)
        for name, content in data["priority_files"].items():
            lines.append(f"\n### {name}")
            lines.append(content)
        lines.append("")

    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Project Scout — scan a project directory")
    parser.add_argument("--path", default=".", help="Directory to scan (default: current dir)")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Output as JSON")
    parser.add_argument("--text", action="store_true", help="Output as plain text (default)")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}))
        sys.exit(1)

    data = scan(root)

    if args.json_out:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(format_text(data))


if __name__ == "__main__":
    main()
