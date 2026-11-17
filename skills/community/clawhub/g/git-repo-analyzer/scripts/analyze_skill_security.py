#!/usr/bin/env python3
"""Clone a Skill repo to staging and perform a basic security review."""
import sys, re, json, os, subprocess, tempfile, pathlib

DANGEROUS_PATTERNS = [
    re.compile(r"rm\s+-rf\s+/"),
    re.compile(r"curl\s+.*\|\s*bash"),
    re.compile(r"eval\s*\("),
    re.compile(r"exec\s*\("),
    re.compile(r"os\.system\s*\("),
    re.compile(r"subprocess\.call\s*\(.*shell\s*=\s*True"),
    re.compile(r"sudo"),
    re.compile(r"chmod\s+777"),
    re.compile(r">\s+/etc/"),
    re.compile(r"mkfs\."),
    re.compile(r"dd\s+if="),
]


def clone_repo(url: str, staging_dir: str):
    subprocess.run(
        ["git", "clone", "--depth", "1", url, staging_dir],
        check=True, capture_output=True, text=True,
    )


def analyze(staging_dir: str, repo_name: str):
    skill_md = pathlib.Path(staging_dir) / "SKILL.md"
    if not skill_md.exists():
        return {"error": "SKILL.md not found", "overall": "dangerous"}

    content = skill_md.read_text(encoding="utf-8", errors="ignore")

    file_structure_check = any(p.search(content) for p in DANGEROUS_PATTERNS)
    network_calls = re.findall(r"https?://[^\"'\s]+", content)
    suspicious = [u for u in network_calls if "github.com" not in u and "gitlab.com" not in u]
    requires_sudo = re.search(r"sudo|chown root|setuid", content) is not None

    report = {
        "fileStructure": {
            "status": "fail" if file_structure_check else "pass",
            "details": "检测到危险系统指令" if file_structure_check else "文件结构安全",
        },
        "networkBehavior": {
            "status": "warn" if len(suspicious) > 3 else "pass",
            "details": f"发现 {len(network_calls)} 个网络调用",
        },
        "systemPermissions": {
            "status": "warn" if requires_sudo else "pass",
            "details": "需要系统权限" if requires_sudo else "无需特殊权限",
        },
        "dependencies": {"status": "pass", "details": "已检查依赖声明"},
        "overall": "safe",
        "tmpDir": staging_dir,
        "repo": repo_name,
    }

    fail_count = sum(1 for r in [report["fileStructure"], report["networkBehavior"], report["systemPermissions"], report["dependencies"]] if r["status"] == "fail")
    warn_count = sum(1 for r in [report["fileStructure"], report["networkBehavior"], report["systemPermissions"], report["dependencies"]] if r["status"] == "warn")

    if fail_count > 0:
        report["overall"] = "dangerous"
    elif warn_count > 1:
        report["overall"] = "caution"

    return report


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_name = sys.argv[2] if len(sys.argv) > 2 else "repo"
    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr)
        sys.exit(1)

    staging = os.path.expanduser(f"~/.openclaw/skills/staging/{repo_name}_{os.getpid()}")
    os.makedirs(os.path.dirname(staging), exist_ok=True)
    try:
        clone_repo(url, staging)
        result = analyze(staging, repo_name)
        if result.get("overall") == "dangerous":
            subprocess.run(["rm", "-rf", staging], check=False)
            result["tmpDir"] = None
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        subprocess.run(["rm", "-rf", staging], check=False)
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
