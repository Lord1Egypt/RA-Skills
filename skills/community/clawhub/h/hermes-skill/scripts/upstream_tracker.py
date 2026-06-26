#!/usr/bin/env python3
"""
Hermes Agent 上游追踪与融合系统 v2
- 空闲时自动 fetch 最新 commit
- 比对本地实现
- 有新思路就写 diff 记录并评估是否值得融合进 SKILL.md
"""

import argparse
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ── Paths ────────────────────────────────────────────────────────────────
SELF_IMPROVING = Path.home() / "self-improving"
TRACKER_DIR = SELF_IMPROVING / "upstream-tracker"
CONFIG_FILE = TRACKER_DIR / "config.json"
STATE_FILE = TRACKER_DIR / "state.json"
CHANGELOG_FILE = TRACKER_DIR / "changelog.md"
SKILL_DIR = Path.home() / ".qclaw" / "skills" / "hermes-skill"
LOCAL_SCRIPTS_DIR = SKILL_DIR / "scripts"

UPSTREAM_REPO = "nousresearch/hermes-agent"
UPSTREAM_API = f"https://api.github.com/repos/{UPSTREAM_REPO}"

# 不追踪的路径模式
IGNORE_PATTERNS = [
    "test", "messaging", "discord", "telegram", "slack", "signal",
    "whatsapp", "gateway", "cli/", "setup", "install", "docs/",
    "assets/", ".git", ".github", "web",
    "optional-skills/blockchain",
    "optional-skills/health",
    "optional-skills/creative",
    "optional-skills/devops",
    "optional-skills/email",
    "optional-skills/communication",
]

# 上游文件 → 本地文件映射
LOCAL_MAP = {
    "agent/memory_manager.py":   LOCAL_SCRIPTS_DIR / "memory_tool.py",
    "agent/memory_provider.py":  LOCAL_SCRIPTS_DIR / "memory_tool.py",
    "agent/skill_commands.py":   LOCAL_SCRIPTS_DIR / "auto_skill_creator.py",
    "agent/skill_utils.py":      LOCAL_SCRIPTS_DIR / "auto_skill_creator.py",
    "agent/prompt_builder.py":   LOCAL_SCRIPTS_DIR / "nudge_system.py",
    "agent/prompt_caching.py":  None,  # 暂不需要
}


# ── HTTP ────────────────────────────────────────────────────────────────
def gh_get(url: str, timeout: int = 10) -> tuple[dict | list | None, bool]:
    """Fetch JSON from GitHub API. Returns (data, ok)."""
    req = Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "hermes-upstream-tracker/1.0",
    })
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read()), True
    except HTTPError as e:
        if e.code == 403:
            print(f"   ⚠️  GitHub API 限速，等待 30s...")
            time.sleep(30)
            return None, False
        return None, False
    except (URLError, TimeoutError):
        return None, False


def fetch(url: str, timeout: int = 10) -> str | None:
    """Fetch raw text from URL."""
    req = Request(url, headers={"User-Agent": "hermes-upstream-tracker/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


# ── State ────────────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "last_commit_sha": None,
        "last_check": None,
        "last_commit_date": None,
        "pending_diffs": [],     # 未处理的 diff
        "last_full_check": None,
    }


def save_state(state: dict):
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ── Commit Fetching ──────────────────────────────────────────────────────
def fetch_recent_commits(since_sha: str | None = None, limit: int = 30) -> list[dict]:
    """Fetch recent commits. Returns list of commit dicts."""
    data, ok = gh_get(f"{UPSTREAM_API}/commits?per_page={limit}&sha=main")
    if not ok or not isinstance(data, list):
        return []
    
    commits = []
    for c in data:
        sha = c["sha"]
        if since_sha and sha == since_sha:
            break
        commits.append({
            "sha": sha,
            "message": c["commit"]["message"].split("\n")[0][:80],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"][:10],
        })
    
    return commits


def fetch_changed_files_for_commits(commits: list[dict]) -> dict[str, list[str]]:
    """Batch fetch changed files for commits. Returns {sha: [filenames]}.
    Only fetches first 10 commits to avoid rate limiting.
    """
    result = {}
    for c in commits[:10]:
        data, ok = gh_get(f"{UPSTREAM_API}/commits/{c['sha']}")
        if ok and isinstance(data, dict):
            files = [f["filename"] for f in data.get("files", [])
                     if not should_ignore(f["filename"])]
            result[c["sha"]] = files
    return result


def should_ignore(path: str) -> bool:
    pl = path.lower()
    return any(p in pl for p in IGNORE_PATTERNS)


# ── Content Fetching & Analysis ─────────────────────────────────────────
def local_for(upstream_path: str) -> Path | None:
    name = Path(upstream_path).name
    for k, v in LOCAL_MAP.items():
        if name in k or k in upstream_path:
            return v
    return None


def analyze_file(upstream_path: str, upstream_sha: str, commit_msg: str) -> dict | None:
    """Fetch upstream content and analyze fusion value vs local."""
    content = fetch(f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/main/{upstream_path}")
    if content is None:
        return None
    
    local_path = local_for(upstream_path)
    local_exists = local_path is not None and local_path.exists()
    local_content = local_path.read_text() if local_exists else ""
    
    upstream_lines = content.splitlines()
    
    # Analyze what new patterns exist
    additions = []
    
    # Memory system
    if "memory" in upstream_path.lower():
        new_methods = re.findall(r'def (\w+)\(', content)
        existing_methods = re.findall(r'def (\w+)\(', local_content)
        for m in new_methods:
            if m not in existing_methods:
                additions.append(f"新方法: def {m}()")
        
        if "class MemoryManager" in content and "MemoryManager" not in local_content:
            additions.append("MemoryManager 编排层")
        if "Honcho" in content or "honcho" in content.lower():
            additions.append("Honcho dialectic 用户建模")
        if "build_system_prompt" in content and "build_system_prompt" not in local_content:
            additions.append("系统提示集成点")
        if "prefetch" in content.lower() and "prefetch" not in local_content.lower():
            additions.append("预取机制")
    
    # Skill system
    elif "skill" in upstream_path.lower():
        if "yaml_load" in content and "yaml" not in local_content.lower():
            additions.append("YAML frontmatter 解析")
        if "parse_frontmatter" in content and "frontmatter" not in local_content.lower():
            additions.append("parse_frontmatter()")
        if "avg_rating" in content and "avg_rating" not in local_content:
            additions.append("avg_rating 评分聚合")
        if "PLATFORM_MAP" in content:
            additions.append("平台兼容映射")
        if "EXCLUDED_SKILL_DIRS" in content:
            additions.append("skill 目录过滤规则")
    
    # Prompt / Nudge
    elif "prompt" in upstream_path.lower():
        if "cache" in content.lower() and "cache" not in local_content.lower():
            additions.append("Prompt 缓存优化")
        if "FENCE" in content or "fence" in content:
            additions.append("Memory context fence 标记")
    
    # Generic: if we have no additions but it's a new file
    if not additions and not local_exists:
        additions.append("全新文件，值得参考")
    
    # Fusion value
    fusion_value = len(additions)
    
    # Local improvements (what we have that upstream might not)
    local_improvements = []
    if "HOT" in local_content and "WARM" in local_content:
        local_improvements.append("HOT/WARM/COLD 三层分层")
    if "qclaw" in local_content.lower():
        local_improvements.append("OpenClaw 适配层")
    if "hermes-skill" in local_content:
        local_improvements.append("自进化 SKILL.md 集成")
    if "evaluate_skill" in local_content and "evaluate_skill" not in content:
        local_improvements.append("Skill 评分与改进")
    
    # Difficulty
    diff_level = "low"
    if len(additions) > 5 or "class MemoryManager" in content:
        diff_level = "medium"
    if len(additions) > 10:
        diff_level = "high"
    
    return {
        "upstream_path": upstream_path,
        "upstream_sha": upstream_sha[:7],
        "commit_msg": commit_msg,
        "local_path": str(local_path) if local_path else None,
        "local_exists": local_exists,
        "upstream_lines": len(upstream_lines),
        "local_lines": len(local_content.splitlines()),
        "additions": additions[:6],
        "fusion_value": fusion_value,
        "diff_level": diff_level,
        "local_improvements": local_improvements,
    }


# ── Diff Generation ─────────────────────────────────────────────────────
def generate_diff_text(upstream_path: str) -> str:
    """Generate a readable diff summary for one file."""
    content = fetch(f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/main/{upstream_path}")
    if content is None:
        return f"无法获取上游文件: {upstream_path}"
    
    local_path = local_for(upstream_path)
    lines = content.splitlines()
    
    if local_path and local_path.exists():
        local = local_path.read_text().splitlines()
        diff_preview = _build_line_diff(lines, local)
        return (
            f"**{upstream_path}**\n"
            f"本地: `{local_path.name}` | "
            f"上游: {len(lines)}L | 本地: {len(local)}L\n"
            f"{diff_preview}"
        )
    else:
        preview = "\n".join(f"  {l}" for l in lines[:40])
        return (
            f"**{upstream_path}** _(本地无对应文件)_\n"
            f"上游 {len(lines)} 行:\n  ```\n{preview}\n  ```"
        )


def _build_line_diff(upstream: list[str], local: list[str], n: int = 50) -> str:
    """Build a simple line-by-line diff preview."""
    # Find the first difference
    diff_idx = None
    for i in range(min(len(upstream), len(local))):
        if upstream[i].strip() != local[i].strip():
            diff_idx = i
            break
    if diff_idx is None and len(upstream) != len(local):
        diff_idx = min(len(local), len(upstream))
    
    if diff_idx is None:
        return "  _(几乎相同)_"
    
    # Show context around first diff
    start = max(0, diff_idx - 2)
    end = min(len(upstream), diff_idx + n + 2)
    lines = []
    for i, ul in enumerate(upstream[start:end], start=start):
        local_l = local[i] if i < len(local) else "(无)"
        marker = "  " if ul.strip() == local_l.strip() else "→ "
        lines.append(f"  {marker}{ul[:100]}")
        if ul.strip() != local_l.strip() and i < len(local) - 1:
            lines.append(f"  ← {local_l[:100]}")
    
    return "  ```\n" + "\n".join(lines) + "\n  ```"


# ── Changelog ────────────────────────────────────────────────────────────
def update_changelog(commits: list[dict], diffs: list[dict]):
    """Append to changelog."""
    now = datetime.now().strftime("%Y-%m-%d")
    
    lines = [f"\n---\n## 同步检查 ({now})\n"]
    
    if commits:
        lines.append(f"\n### 新增提交 ({len(commits)} 个)\n")
        lines.append("| SHA | 作者 | 日期 | 消息 |\n")
        lines.append("|-----|------|------|------|\n")
        for c in commits[:15]:
            msg = c["message"][:55]
            lines.append(f"| `{c['sha'][:7]}` | {c['author']} | {c['date']} | {msg} |\n")
        if len(commits) > 15:
            lines.append(f"\n_...还有 {len(commits)-15} 个提交_\n")
    
    if diffs:
        diffs_sorted = sorted(diffs, key=lambda x: x["fusion_value"], reverse=True)
        
        high = [d for d in diffs_sorted if d["diff_level"] in ("low", "medium")]
        local_wins = [d for d in diffs_sorted if d.get("local_improvements")]
        
        if high:
            lines.append("\n### 🔴 值得融合 (按价值排序)\n")
            for d in high[:5]:
                local = Path(d["local_path"]).name if d.get("local_path") else "—"
                adds = "; ".join(d["additions"][:3]) or "新增内容"
                lines.append(
                    f"- **{d['upstream_path']}** → `{local}` "
                    f"(`{d['upstream_sha']}`)\n"
                )
                lines.append(f"  发现: {adds}\n")
                lines.append(f"  融合价值: {d['fusion_value']}/10 · 难度: {d['diff_level']}\n")
        
        if local_wins:
            lines.append("\n### 🟢 本地超越上游\n")
            for d in local_wins[:3]:
                lines.append(f"- **{d['upstream_path']}**:\n")
                for imp in d["local_improvements"]:
                    lines.append(f"  ✅ {imp}\n")
    
    entry = "".join(lines)
    
    if CHANGELOG_FILE.exists():
        existing = CHANGELOG_FILE.read_text()
        parts = existing.split("\n", 2)
        if len(parts) >= 2:
            parts.insert(2, entry)
            content = "\n".join(parts[:3]) + "\n" + "\n".join(parts[2:])
        else:
            content = existing + entry
    else:
        content = "# Hermes Agent 上游追踪记录\n" + entry
    
    CHANGELOG_FILE.write_text(content)


# ── Main check ──────────────────────────────────────────────────────────
def check_upstream():
    """Full upstream check."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 检查 {UPSTREAM_REPO}/main")
    
    state = load_state()
    since_sha = state.get("last_commit_sha")
    
    commits = fetch_recent_commits(since_sha=since_sha, limit=30)
    
    if not commits:
        print("✅ 无新提交或 API 限速")
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        return {"status": "no_new_commits", "commits": []}
    
    print(f"📦 发现 {len(commits)} 个新提交")
    
    new_sha = commits[0]["sha"]
    state["last_commit_sha"] = new_sha
    state["last_check"] = datetime.now().isoformat()
    state["last_full_check"] = datetime.now().isoformat()
    
    # Get changed files for recent commits
    changed = fetch_changed_files_for_commits(commits)
    
    # Collect all relevant changed files
    all_changed = set()
    for files in changed.values():
        for f in files:
            if not should_ignore(f) and f.endswith(".py"):
                all_changed.add(f)
    
    # Always include our focus files for comparison
    focus_files = list(LOCAL_MAP.keys())
    for f in focus_files:
        all_changed.add(f)
    
    print(f"📁 相关文件: {len(all_changed)} 个，分析中...")
    
    diffs = []
    for path in sorted(all_changed):
        if path not in all_changed:
            continue
        
        # Find the commit that changed this
        msg = ""
        for sha, files in changed.items():
            if path in files:
                for c in commits:
                    if c["sha"] == sha:
                        msg = c["message"]
                        break
                break
        
        diff = analyze_file(path, new_sha, msg)
        if diff and (diff["fusion_value"] >= 1 or not diff["local_exists"]):
            diffs.append(diff)
    
    # Store pending diffs (high value only)
    high_diffs = [d for d in diffs if d["fusion_value"] >= 2]
    state["pending_diffs"] = high_diffs
    save_state(state)
    
    update_changelog(commits, diffs)
    
    print(f"\n✅ 检查完成:")
    print(f"   新提交: {len(commits)} 个")
    print(f"   高价值 diff: {len(high_diffs)} 个")
    print(f"   最新: `{new_sha[:7]}`")
    
    if high_diffs:
        print(f"\n🔥 Top 融合机会:")
        for d in sorted(high_diffs, key=lambda x: x["fusion_value"], reverse=True)[:3]:
            local = Path(d["local_path"]).name if d.get("local_path") else "—"
            print(f"   [{d['fusion_value']}/10] {d['upstream_path']} → {local}")
            for a in d["additions"][:2]:
                print(f"       + {a}")
    
    return {"status": "ok", "commits": commits, "diffs": diffs}


# ── Status ───────────────────────────────────────────────────────────────
def show_status():
    state = load_state()
    
    print("## 📡 Hermes Agent 上游追踪\n")
    print(f"仓库: https://github.com/{UPSTREAM_REPO}")
    
    if state.get("last_check"):
        last = datetime.fromisoformat(state["last_check"]).strftime("%Y-%m-%d %H:%M")
        print(f"最后检查: {last}")
    else:
        print("最后检查: 从未运行")
    
    if state.get("last_commit_sha"):
        print(f"已知最新提交: `{state['last_commit_sha'][:7]}`")
    
    pending = state.get("pending_diffs", [])
    if pending:
        print(f"\n待处理融合: {len(pending)} 个")
        for d in pending[:5]:
            local = Path(d["local_path"]).name if d.get("local_path") else "—"
            print(f"  [{d['fusion_value']}/10] {d['upstream_path']} → {local}")
    else:
        print("\n待处理融合: 无")


# ── Fuse recommendations ────────────────────────────────────────────────
def show_fuse():
    state = load_state()
    diffs = state.get("pending_diffs", [])
    
    if not diffs:
        print("📭 无待融合 diff，先运行 `check`")
        return
    
    print("## 🔬 融合推荐\n")
    for i, d in enumerate(sorted(diffs, key=lambda x: x["fusion_value"], reverse=True), 1):
        print(f"\n### {i}. {d['upstream_path']}")
        print(f"   上游 SHA: `{d['upstream_sha']}` | 融合价值: {d['fusion_value']}/10 | 难度: {d['diff_level']}")
        print(f"   本地对应: {d.get('local_path', '无')}")
        print(f"   **发现内容:**")
        for a in d.get("additions", []):
            print(f"     • {a}")
        if d.get("local_improvements"):
            print(f"   **本地优势:**")
            for imp in d["local_improvements"]:
                print(f"     ✅ {imp}")
        print(f"   **行动:** `python3 upstream_tracker.py diff {d['upstream_path']}`")


# ── CLI ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="Hermes Agent 上游追踪与融合系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  check   检查上游新提交并分析融合价值
  status  查看追踪状态
  diff    显示具体文件对比 (需指定上游路径)
  fuse    显示融合推荐
  list    列出追踪的核心文件
        """
    )
    ap.add_argument("cmd", nargs="?", default="check",
                   choices=["check", "status", "diff", "fuse", "list"])
    ap.add_argument("path", nargs="?", help="上游文件路径")
    ap.add_argument("--json", action="store_true")
    
    args = ap.parse_args()
    
    if args.cmd == "check":
        result = check_upstream()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    
    elif args.cmd == "status":
        show_status()
    
    elif args.cmd == "diff":
        if not args.path:
            print("❌ 需指定路径，如: diff agent/memory_manager.py")
            print("   用 list 查看可用路径")
            return
        print(generate_diff_text(args.path))
    
    elif args.cmd == "fuse":
        show_fuse()
    
    elif args.cmd == "list":
        print("📁 追踪的核心文件:\n")
        for k, v in LOCAL_MAP.items():
            local = v.name if v else "—"
            print(f"  {k:40s} → {local}")


if __name__ == "__main__":
    main()
