#!/usr/bin/env python3
"""
lobster_submit.py — Lobster Rank data collector & submission client

Scans locally installed OpenClaw skills, packages raw metadata,
and submits to the lobster ranking server for evaluation.
Scoring logic lives entirely on the server.

Usage:
  python3 lobster_submit.py                        # scan + submit
  python3 lobster_submit.py --dry-run              # scan only, no submit
  python3 lobster_submit.py --confirm <token>      # confirm upload to leaderboard
  python3 lobster_submit.py --mode live-challenge --challenge-score 87
  python3 lobster_submit.py --root /path/to/skills
  python3 lobster_submit.py --api-key lbk_xxx
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List, Dict

# ── Constants ────────────────────────────────────────────────────────────────

DEFAULT_API_URL = "https://lobster-rank.wondercv.com/api"

SYSTEM_SKILL_NAMES = {
    "lobster-evaluator",
    "lobster-rank",
    "update-config",
    "simplify",
    "loop",
    "claude-api",
    "skill-creator",
}

SKILL_SEARCH_PATHS = [
    Path.home() / ".openclaw" / "workspace" / "skills",
    Path.home() / "Library" / "Application Support" / "QClaw" / "openclaw" / "config" / "skills",
]

CONFIG_SEARCH_PATHS = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path.home() / "Library" / "Application Support" / "QClaw" / "openclaw" / "config" / "openclaw.json",
]

LOG_SEARCH_PATHS = [
    Path.home() / "Library" / "Logs" / "QClaw" / "openclaw",
]


# ── API key resolution ────────────────────────────────────────────────────────

def resolve_api_key(cli_key: Optional[str]) -> Optional[str]:
    """Precedence: CLI arg > env var > config file."""
    if cli_key:
        return cli_key

    env = os.environ.get("OPENCLAW_API_KEY")
    if env:
        return env

    for cfg_path in CONFIG_SEARCH_PATHS:
        if cfg_path.exists():
            try:
                data = json.loads(cfg_path.read_text(encoding="utf-8"))
                key = data.get("apiKey") or data.get("api_key")
                if key:
                    return key
            except Exception:
                pass

    return None


def resolve_api_url(cli_url: Optional[str]) -> str:
    if cli_url:
        return cli_url.rstrip("/")
    env = os.environ.get("LOBSTER_API_URL")
    if env:
        return env.rstrip("/")
    return DEFAULT_API_URL


# ── Skill scanner ─────────────────────────────────────────────────────────────

def scan_skill_dir(skill_dir: Path) -> dict:
    """Extract raw metadata from a single skill directory."""
    name = skill_dir.name

    has_skill_md = (skill_dir / "SKILL.md").exists()

    scripts_dir = skill_dir / "scripts"
    has_scripts = scripts_dir.is_dir() and any(
        f.suffix in (".py", ".sh", ".js", ".ts", ".rb")
        for f in scripts_dir.iterdir()
        if f.is_file()
    ) if scripts_dir.is_dir() else False

    references_dir = skill_dir / "references"
    has_references = references_dir.is_dir() and any(
        f.is_file() for f in references_dir.iterdir()
    ) if references_dir.is_dir() else False

    assets_dir = skill_dir / "assets"
    has_assets = assets_dir.is_dir() and any(
        f.is_file() for f in assets_dir.iterdir()
    ) if assets_dir.is_dir() else False

    file_count = sum(1 for f in skill_dir.rglob("*") if f.is_file())

    description = ""
    if has_skill_md:
        try:
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("description:"):
                    description = line[len("description:"):].strip().strip('"').strip("'")
                    break
        except Exception:
            pass

    is_system = name in SYSTEM_SKILL_NAMES

    return {
        "name": name,
        "is_system": is_system,
        "has_scripts": has_scripts,
        "has_references": has_references,
        "has_assets": has_assets,
        "has_skill_md": has_skill_md,
        "file_count": file_count,
        "description": description,
    }


def scan_all_skills(extra_root: Optional[Path] = None) -> List[Dict]:
    """Scan all configured skill locations, deduplicate by name."""
    search_paths = list(SKILL_SEARCH_PATHS)
    if extra_root:
        search_paths.insert(0, extra_root)

    seen = set()
    skills = []

    for base in search_paths:
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            if not entry.is_dir():
                continue
            name = entry.name
            if name in seen:
                continue
            seen.add(name)
            skills.append(scan_skill_dir(entry))

    return skills


# ── Config / log detection ────────────────────────────────────────────────────

def detect_multi_model(skills: List[Dict]) -> Dict:
    """
    Heuristic: inspect all SKILL.md files for multi-model / routing signals.
    Returns flags that the server uses as a quality signal.
    """
    detected = False
    has_routing = False
    has_fallback = False
    cost_aware = False

    model_keywords = {
        "gpt-4", "gpt-3", "claude", "gemini", "o1", "o3",
        "deepseek", "llama", "mistral", "qwen",
    }
    routing_keywords = {"routing", "route", "dispatch", "select model", "选择模型", "路由"}
    fallback_keywords = {"fallback", "retry", "backup model", "备用", "降级"}
    cost_keywords = {"cost", "token budget", "cheap", "economy", "省钱", "成本"}

    search_paths = list(SKILL_SEARCH_PATHS)
    for base in search_paths:
        if not base.is_dir():
            continue
        for skill_dir in base.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            try:
                text = skill_md.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue

            models_found = sum(1 for kw in model_keywords if kw in text)
            if models_found >= 2:
                detected = True
            if any(kw in text for kw in routing_keywords):
                has_routing = True
            if any(kw in text for kw in fallback_keywords):
                has_fallback = True
            if any(kw in text for kw in cost_keywords):
                cost_aware = True

    return {
        "detected": detected,
        "has_routing": has_routing,
        "has_fallback": has_fallback,
        "cost_aware": cost_aware,
    }


def detect_logs_available() -> bool:
    for log_path in LOG_SEARCH_PATHS:
        if log_path.is_dir():
            log_files = [f for f in log_path.rglob("*.log") if f.is_file()]
            if log_files:
                return True
    return False


# ── Build payload ─────────────────────────────────────────────────────────────

def build_payload(
    skills: List[Dict],
    mode: str,
    challenge_score: Optional[float],
) -> Dict:
    user_skills = [s for s in skills if not s["is_system"]]
    system_skill_count = sum(1 for s in skills if s["is_system"])

    multi_model = detect_multi_model(skills)
    logs_available = detect_logs_available()

    payload: dict = {
        "eval_mode": mode,
        "skills": skills,
        "multi_model": multi_model,
        "logs_available": logs_available,
        "total_found": len(skills),
        "system_skill_count": system_skill_count,
    }

    if mode == "live-challenge" and challenge_score is not None:
        payload["challenge_score"] = challenge_score

    return payload


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def post_json(url: str, payload: dict, api_key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="ignore")
        try:
            err_data = json.loads(body_text)
            raise RuntimeError(err_data.get("error", body_text)) from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e


def post_confirm(url: str, token: str, api_key: str) -> dict:
    return post_json(url, {"token": token}, api_key)


# ── Display helpers ───────────────────────────────────────────────────────────

GRADE_LABELS = {
    "S": "🦞 龙虾王",
    "A": "🦐 精英虾",
    "B": "🍤 进阶虾",
    "C": "🌱 入门虾",
    "D": "🪸 虾苗",
}


def print_score_result(result: Dict) -> None:
    grade = result.get("grade", "?")
    label = GRADE_LABELS.get(grade, grade)
    total = result.get("total_score", "?")
    title = result.get("title", "")
    skill_count = result.get("skill_count", "?")
    mode = result.get("eval_mode", "")
    version = result.get("rules_version", "")
    pending_token = result.get("pending_token", "")
    expires_at = result.get("expires_at", "")

    print()
    print("━" * 52)
    print(f"  🦞 龙虾评分结果")
    print("━" * 52)
    print(f"  总分：{total} / 100")
    print(f"  等级：{grade}  {label}")
    print(f"  称号：{title}")
    print(f"  技能数：{skill_count}")
    print(f"  评分模式：{mode}")
    print(f"  规则版本：{version}")

    dims = result.get("dimensions")
    if dims:
        print()
        print("  六维雷达：")
        dim_names = {
            "core_skill_depth":    "核心技能深度",
            "problem_solving":     "问题解决能力",
            "human_collaboration": "人机协作",
            "agent_orchestration": "Agent 编排",
            "stability_trust":     "稳定性与可信度",
            "productization":      "产品化能力",
        }
        for key, label_cn in dim_names.items():
            val = dims.get(key, 0)
            bar_len = int(val / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {label_cn:<12}  {bar}  {val:3d}")

    top_skills = result.get("top_skills")
    if top_skills:
        print()
        print(f"  Top 3 核心 Skill：{', '.join(top_skills)}")

    if pending_token:
        print()
        print(f"  ✅ 评分已生成，待确认上传")
        print(f"  Token：{pending_token}")
        if expires_at:
            print(f"  有效至：{expires_at}")
    print("━" * 52)
    print()


def print_scan_summary(skills: List[Dict]) -> None:
    user_skills = [s for s in skills if not s["is_system"]]
    system_skills = [s for s in skills if s["is_system"]]
    print(f"\n  扫描完成：发现 {len(user_skills)} 个用户 Skill，{len(system_skills)} 个系统 Skill")
    if user_skills:
        print("  用户 Skill 列表：")
        for s in user_skills:
            flags = []
            if s["has_scripts"]:    flags.append("scripts")
            if s["has_references"]: flags.append("refs")
            if s["has_assets"]:     flags.append("assets")
            flag_str = f"  [{', '.join(flags)}]" if flags else ""
            print(f"    · {s['name']}{flag_str}")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect lobster skill data and submit to the ranking server.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key",  metavar="KEY",   help="Lobster API key (overrides env / config)")
    parser.add_argument("--api-url",  metavar="URL",   help=f"API base URL (default: {DEFAULT_API_URL})")
    parser.add_argument("--root",     metavar="PATH",  help="Extra skill directory to scan")
    parser.add_argument("--mode",     metavar="MODE",  default="quick-auto",
                        choices=["quick-auto", "evidence-augmented", "live-challenge"],
                        help="Evaluation mode (default: quick-auto)")
    parser.add_argument("--challenge-score", metavar="N", type=float,
                        help="Live challenge score (0-100), only for --mode live-challenge")
    parser.add_argument("--confirm",  metavar="TOKEN",
                        help="Confirm upload of a pending score using its token")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Scan locally and print payload, do not send to server")
    args = parser.parse_args()

    api_url = resolve_api_url(args.api_url)

    # ── Confirm mode ──────────────────────────────────────────────────────────
    if args.confirm:
        api_key = resolve_api_key(args.api_key)
        if not api_key:
            print("错误：缺少 API Key。请用 --api-key 传入，或设置环境变量 OPENCLAW_API_KEY。")
            print("获取地址：https://lobster-rank.wondercv.com/me")
            sys.exit(1)

        print(f"\n  正在确认上传…")
        try:
            result = post_confirm(f"{api_url}/score/confirm", args.confirm, api_key)
        except RuntimeError as e:
            print(f"  ❌ 上传失败：{e}")
            sys.exit(1)

        print(f"  🎉 上传成功！排行榜已更新")
        print(f"  Score ID: {result.get('scoreId')}")
        print(f"\n  查看排行榜：https://lobster-rank.wondercv.com\n")
        return

    # ── Scan ──────────────────────────────────────────────────────────────────
    extra_root = Path(args.root) if args.root else None
    print("\n  正在扫描本地技能…")
    skills = scan_all_skills(extra_root)
    print_scan_summary(skills)

    user_skills = [s for s in skills if not s["is_system"]]
    if not user_skills:
        print("  ❌ 未发现用户自装 Skill，无法生成评分。")
        print("  请先安装至少一个自己的 Skill，再重新运行此命令。")
        sys.exit(1)

    payload = build_payload(skills, args.mode, args.challenge_score)

    # ── Dry run ───────────────────────────────────────────────────────────────
    if args.dry_run:
        print("  [dry-run] 将发送的数据：")
        # Strip descriptions to reduce noise in dry-run output
        dry_payload = dict(payload)
        dry_payload["skills"] = [
            {k: v for k, v in s.items() if k != "description"}
            for s in payload["skills"]
        ]
        print(json.dumps(dry_payload, ensure_ascii=False, indent=2))
        return

    # ── Submit ────────────────────────────────────────────────────────────────
    api_key = resolve_api_key(args.api_key)
    if not api_key:
        print("  错误：缺少 API Key。")
        print("  请用 --api-key 传入，或设置环境变量 OPENCLAW_API_KEY。")
        print("  获取地址：https://lobster-rank.wondercv.com/me\n")
        sys.exit(1)

    print(f"  正在提交到评分服务器…")
    try:
        result = post_json(f"{api_url}/score/evaluate", payload, api_key)
    except RuntimeError as e:
        print(f"\n  ❌ 提交失败：{e}\n")
        sys.exit(1)

    print_score_result(result)

    # ── Prompt for confirm ────────────────────────────────────────────────────
    pending_token = result.get("pending_token")
    if pending_token:
        print("  若要将此成绩上传到排行榜，请运行：")
        print(f"\n    python3 scripts/lobster_submit.py --confirm {pending_token}\n")
        print("  或者直接在网站上确认：https://lobster-rank.wondercv.com/me\n")


if __name__ == "__main__":
    main()
