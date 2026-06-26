#!/usr/bin/env python3
"""
resolve_paths.py — Path resolution for skill evaluation

Given a skill name, resolves all paths needed for evaluation:
- skill_path: location of SKILL.md
- evals_dir: location of evals (skill-specific or fallback to examples)
- output_dir: next available iter-N directory

Usage:
    python resolve_paths.py <skill-name> [--mode trigger|quality|all]

Output (JSON):
    {
        "skill_name": "weather",
        "skill_path": "/path/to/weather/SKILL.md",
        "evals": {
            "triggers": "/path/to/triggers.json",
            "quality": "/path/to/quality.json"
        },
        "output_dir": "eval-workspace/weather/iter-1",
        "mode": "all",
        "warnings": ["Using example evals, consider creating evals/weather/"]
    }
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def find_skill_path(skill_name: str, extra_dirs: list[str]) -> str | None:
    """Find SKILL.md for the given skill name."""
    candidates = []
    
    # Check extra_dirs first (user skills)
    for extra_dir in extra_dirs:
        candidate = Path(extra_dir).expanduser() / skill_name / "SKILL.md"
        candidates.append(candidate)
        if candidate.exists():
            return str(candidate)
    
    # Check OpenClaw built-in skills
    builtin_paths = [
        Path("/opt/homebrew/lib/node_modules/openclaw/skills") / skill_name / "SKILL.md",
        Path("/usr/local/lib/node_modules/openclaw/skills") / skill_name / "SKILL.md",
        Path.home() / ".npm-global/lib/node_modules/openclaw/skills" / skill_name / "SKILL.md",
    ]
    
    for candidate in builtin_paths:
        candidates.append(candidate)
        if candidate.exists():
            return str(candidate)
    
    return None


def find_evals(skill_name: str, evals_base: Path, mode: str) -> dict:
    """Find evals files for the skill."""
    result = {"triggers": None, "quality": None}
    warnings = []
    
    # Check skill-specific evals first
    skill_evals_dir = evals_base / skill_name
    
    if skill_evals_dir.exists():
        triggers = skill_evals_dir / "triggers.json"
        quality = skill_evals_dir / "quality.json"
        
        if triggers.exists():
            result["triggers"] = str(triggers)
        if quality.exists():
            result["quality"] = str(quality)
    
    # Fallback to examples if needed
    if mode in ("trigger", "all") and not result["triggers"]:
        fallback = evals_base / "example-triggers.json"
        if fallback.exists():
            result["triggers"] = str(fallback)
            warnings.append(f"Using example triggers. Consider creating evals/{skill_name}/triggers.json")
    
    if mode in ("quality", "all") and not result["quality"]:
        fallback = evals_base / "example-quality.json"
        if fallback.exists():
            result["quality"] = str(fallback)
            warnings.append(f"Using example quality evals. Consider creating evals/{skill_name}/quality.json")
    
    return result, warnings


def get_next_output_dir(skill_name: str, workspace_base: Path) -> str:
    """Get the next available iter-N directory."""
    skill_workspace = workspace_base / skill_name
    
    if not skill_workspace.exists():
        return str(skill_workspace / "iter-1")
    
    # Find existing iter-N directories
    existing = list(skill_workspace.glob("iter-*"))
    if not existing:
        return str(skill_workspace / "iter-1")
    
    # Extract numbers and find max
    numbers = []
    for p in existing:
        match = re.search(r"iter-(\d+)", p.name)
        if match:
            numbers.append(int(match.group(1)))
    
    next_n = max(numbers) + 1 if numbers else 1
    return str(skill_workspace / f"iter-{next_n}")


def resolve_paths(skill_name: str, mode: str = "all", extra_dirs: list[str] = None) -> dict:
    """Main resolution function."""
    if extra_dirs is None:
        extra_dirs = []
    
    warnings = []
    
    # Find skill path
    skill_path = find_skill_path(skill_name, extra_dirs)
    if not skill_path:
        return {
            "error": f"Skill '{skill_name}' not found. Check spelling or ensure it's registered in extraDirs.",
            "searched": extra_dirs + ["/opt/homebrew/lib/node_modules/openclaw/skills/"],
        }
    
    # Find this script's location to locate evals/
    script_dir = Path(__file__).parent.parent  # skill-eval root
    evals_base = script_dir / "evals"
    workspace_base = script_dir / "eval-workspace"
    
    # Find evals
    evals, evals_warnings = find_evals(skill_name, evals_base, mode)
    warnings.extend(evals_warnings)
    
    # Validate we have required evals for the mode
    if mode in ("trigger", "all") and not evals["triggers"]:
        return {"error": f"No triggers.json found for '{skill_name}' and no fallback available."}
    if mode in ("quality", "all") and not evals["quality"]:
        return {"error": f"No quality.json found for '{skill_name}' and no fallback available."}
    
    # Get output directory
    output_dir = get_next_output_dir(skill_name, workspace_base)
    
    return {
        "skill_name": skill_name,
        "skill_path": skill_path,
        "evals": evals,
        "output_dir": output_dir,
        "mode": mode,
        "warnings": warnings,
    }


def load_extra_dirs_from_config() -> list[str]:
    """Load extraDirs from openclaw.json if available."""
    config_paths = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path.home() / ".config" / "openclaw" / "openclaw.json",
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                return config.get("skills", {}).get("load", {}).get("extraDirs", [])
            except (json.JSONDecodeError, KeyError):
                pass
    return []


def main():
    parser = argparse.ArgumentParser(description="Resolve paths for skill evaluation")
    parser.add_argument("skill_name", help="Name of the skill to evaluate")
    parser.add_argument("--mode", choices=["trigger", "quality", "all"], default="all",
                        help="Evaluation mode (default: all)")
    parser.add_argument("--extra-dirs", nargs="*", default=None,
                        help="Additional directories to search for skills (auto-detected from openclaw.json if not specified)")
    
    args = parser.parse_args()
    
    # Auto-load extraDirs from config if not specified
    extra_dirs = args.extra_dirs if args.extra_dirs is not None else load_extra_dirs_from_config()
    
    result = resolve_paths(args.skill_name, args.mode, extra_dirs)
    print(json.dumps(result, indent=2))
    
    # Exit with error code if resolution failed
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
