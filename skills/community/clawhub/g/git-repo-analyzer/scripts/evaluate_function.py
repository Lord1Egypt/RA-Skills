#!/usr/bin/env python3
"""Clone a function project repo, analyze code structure, and evaluate OpenClaw skill feasibility."""
import sys, os, re, shutil, subprocess, pathlib, json


def clone_repo(url: str, dest: str):
    subprocess.run(
        ["git", "clone", "--depth", "1", url, dest],
        check=True, capture_output=True, text=True,
    )


def run_cloc(root: pathlib.Path):
    try:
        result = subprocess.run(
            ["cloc", "--json", "."],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return json.loads(result.stdout)
    except Exception:
        return {}


def gather_files(root: pathlib.Path):
    files = []
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in str(p.relative_to(root)).split(os.sep):
            files.append(str(p.relative_to(root)))
    return files


def count_dependencies(root: pathlib.Path):
    deps = 0

    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
            deps += len(data.get("dependencies", {})) + len(data.get("devDependencies", {}))
        except Exception:
            pass

    req = root / "requirements.txt"
    if req.exists():
        content = req.read_text(encoding="utf-8", errors="ignore")
        deps += sum(1 for line in content.splitlines() if line.strip() and not line.strip().startswith("#"))

    cargo = root / "Cargo.toml"
    if cargo.exists():
        content = cargo.read_text(encoding="utf-8", errors="ignore")
        deps += len(re.findall(r"^\[dependencies\]", content, re.M))

    gomod = root / "go.mod"
    if gomod.exists():
        content = gomod.read_text(encoding="utf-8", errors="ignore")
        deps += sum(
            1 for line in content.splitlines()
            if line.strip() and not line.strip().startswith("//") and " " in line.strip()
        )

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8", errors="ignore")
        deps += sum(1 for line in content.splitlines() if re.search(r"^[\"']?[\w-]+[\"']?\s*[=~!<>]", line))

    return deps


def analyze(root: pathlib.Path):
    stats = run_cloc(root)
    languages = [k for k in stats.keys() if k not in ("header", "SUM", "N/A")]
    lines_of_code = stats.get("SUM", {}).get("code", 0)

    files = gather_files(root)

    has_cli = any(
        re.search(r"(cli|cmd|main\.go|main\.rs|__main__\.py)$", f, re.I) for f in files
    )

    has_api = any(
        re.search(r"(api|lib|server|index\.js|fastapi|flask)", f, re.I) for f in files
    )

    dependencies = count_dependencies(root)

    complexity = "simple"
    if lines_of_code > 10000 or dependencies > 50:
        complexity = "complex"
    elif lines_of_code > 2000 or dependencies > 10:
        complexity = "medium"

    entry_points = [f for f in files if re.search(r"(main|index|cli|cmd)\.(js|py|go|rs|ts)$", f, re.I)]

    return {
        "languages": languages,
        "complexity": complexity,
        "linesOfCode": lines_of_code,
        "dependencies": dependencies,
        "hasCLI": has_cli,
        "hasAPI": has_api,
        "entryPoints": entry_points,
    }


def evaluate(analysis: dict):
    skill_wrap = 2 if analysis["hasCLI"] else (3 if analysis["hasAPI"] else 4)
    toolchain = 5 if any(l in ["Python", "JavaScript", "TypeScript"] for l in analysis["languages"]) else 3
    learning = 3 if analysis["complexity"] == "simple" else (4 if analysis["complexity"] == "medium" else 5)
    maintenance = 2 if analysis["complexity"] == "simple" else (3 if analysis["complexity"] == "medium" else 5)

    if analysis["hasCLI"] and analysis["complexity"] == "simple":
        approach = "skill"
    elif analysis["hasAPI"] and toolchain >= 4:
        approach = "integration"
    elif analysis["complexity"] == "complex":
        approach = "external"
    else:
        approach = "skill"

    return {
        "skillWrapDifficulty": skill_wrap,
        "toolchainCompatibility": toolchain,
        "learningValue": learning,
        "maintenanceCost": maintenance,
        "recommendedApproach": approach,
    }


def stars(n: int) -> str:
    n = max(1, min(5, int(n)))
    return "⭐" * n + "☆" * (5 - n)


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_name = sys.argv[2] if len(sys.argv) > 2 else "repo"
    if not url or not repo_name:
        print(json.dumps({"error": "URL and repo_name required"}), file=sys.stderr)
        sys.exit(1)

    staging = os.path.expanduser(f"~/.openclaw/skills/staging/{repo_name}_{os.getpid()}")
    os.makedirs(os.path.dirname(staging), exist_ok=True)
    try:
        clone_repo(url, staging)
        analysis = analyze(pathlib.Path(staging))
        feasibility = evaluate(analysis)
        shutil.rmtree(staging, ignore_errors=True)

        result = {
            "repoName": repo_name,
            "url": url,
            "analysis": analysis,
            "feasibility": feasibility,
            "skillWrapDifficultyStars": stars(feasibility["skillWrapDifficulty"]),
            "toolchainCompatibilityStars": stars(feasibility["toolchainCompatibility"]),
            "learningValueStars": stars(feasibility["learningValue"]),
            "maintenanceCostStars": stars(6 - feasibility["maintenanceCost"]),
        }
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        shutil.rmtree(staging, ignore_errors=True)
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
