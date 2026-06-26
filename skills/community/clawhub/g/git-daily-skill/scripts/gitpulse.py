#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
# 强制 stdout 使用 UTF-8，解决 Windows GBK 乱码/报错
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
╔══════════════════════════════════════════════════════╗
║  ⚡ GitPulse · 今日 Git 提交复盘脚本                 ║
║  扫描多仓库，聚合当日（含次日凌晨6点前）commit 记录    ║
║  Zero external dependencies · Python 3.8+            ║
╚══════════════════════════════════════════════════════╝
"""

import argparse
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


# ─────────────────────────────────────────────────────────
# 1. 时间窗口计算
# ─────────────────────────────────────────────────────────

def get_time_window(date_str: str | None = None):
    """
    返回 (start_dt, end_dt)。
    规则：当天 06:00:00 ~ 次日 05:59:59
    这样满足：凌晨还在敲代码的情况被统计进"当天"。
    """
    if date_str:
        base = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        now = datetime.now()
        # 如果当前时间在 00:00 ~ 05:59，视为"昨天"的工作区间
        if now.hour < 6:
            base = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            base = now.replace(hour=0, minute=0, second=0, microsecond=0)

    start_dt = base.replace(hour=6, minute=0, second=0, microsecond=0)
    end_dt = (base + timedelta(days=1)).replace(hour=5, minute=59, second=59, microsecond=0)
    return start_dt, end_dt


# ─────────────────────────────────────────────────────────
# 2. 查找 Git 仓库
# ─────────────────────────────────────────────────────────

def find_git_repos(root: str, max_depth: int = 3) -> list[str]:
    """
    从 root 开始向下最多 max_depth 层，找所有含 .git 目录的路径。
    """
    repos = []
    root_path = Path(root)

    def _scan(path: Path, depth: int):
        if depth > max_depth:
            return
        git_dir = path / ".git"
        if git_dir.exists() and git_dir.is_dir():
            repos.append(str(path))
            return  # 找到仓库后不再递归进去
        try:
            for child in path.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    _scan(child, depth + 1)
        except PermissionError:
            pass

    _scan(root_path, 0)
    return sorted(repos)


# ─────────────────────────────────────────────────────────
# 3. 读取单个仓库的 commit
# ─────────────────────────────────────────────────────────

# git log 格式：hash|作者|ISO时间|subject
GIT_LOG_FORMAT = "%H|%an|%ai|%s"
GIT_LOG_SEP = "|||GITPULSE|||"


def get_current_git_user(repo_path: str = ".") -> str:
    """读取当前仓库（或全局）git config user.name"""
    for scope in (["-C", repo_path], ["--global"]):
        try:
            r = subprocess.run(
                ["git"] + scope + ["config", "user.name"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5,
            )
            name = r.stdout.strip()
            if name:
                return name
        except Exception:
            pass
    return ""


def get_commits_in_window(repo_path: str, start_dt: datetime, end_dt: datetime, author: str = "") -> list[dict]:
    """
    调用 git log，返回时间窗口内的 commit 列表。
    每条 commit 格式：
      {
        "hash": "abc1234",
        "author": "张三",
        "timestamp": "2026-04-10 14:23:01",
        "time_label": "14:23",
        "message": "feat: 实现 OTA 价格爬虫"
      }
    """
    after = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    before = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    cmd = [
        "git", "-C", repo_path,
        "log",
        "--all",
        f"--after={after}",
        f"--before={before}",
        f"--format={GIT_LOG_FORMAT}",
        "--no-merges",
    ]
    if author:
        cmd.append(f"--author={author}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except subprocess.TimeoutExpired:
        return []
    except FileNotFoundError:
        print("[错误] 未找到 git 命令，请确认 git 已安装并在 PATH 中。", file=sys.stderr)
        sys.exit(1)

    commits = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        hash_val, author, ts_raw, message = parts
        try:
            # git 输出带时区，如 "2026-04-10 14:23:01 +0800"
            # 统一格式化为本地时间字符串
            ts_clean = ts_raw.strip()
            # 解析带时区的 ISO 格式
            if "+" in ts_clean[10:] or ts_clean.endswith("Z"):
                # Python 3.7+ fromisoformat 不支持带时区的空格分隔，手动处理
                ts_clean = ts_clean.replace(" ", "T", 1)
                dt = datetime.fromisoformat(ts_clean)
                # 转为 naive local（去掉 tz info，因为 git 输出的已是本地时间）
                ts_display = dt.strftime("%Y-%m-%d %H:%M:%S")
                time_label = dt.strftime("%H:%M")
            else:
                ts_display = ts_clean
                time_label = ts_clean[11:16] if len(ts_clean) >= 16 else "??"
        except Exception:
            ts_display = ts_raw.strip()
            time_label = ts_raw.strip()[11:16] if len(ts_raw.strip()) >= 16 else "??"

        commits.append({
            "hash": hash_val.strip()[:7],
            "hash_full": hash_val.strip(),
            "author": author.strip(),
            "timestamp": ts_display,
            "time_label": time_label,
            "message": message.strip(),
        })

    # 按时间升序
    commits.sort(key=lambda c: c["timestamp"])
    return commits


# ─────────────────────────────────────────────────────────
# 4. 统计活跃时段
# ─────────────────────────────────────────────────────────

def calc_active_period(all_commits: list[dict]) -> str:
    if not all_commits:
        return "无"
    times = sorted(c["time_label"] for c in all_commits if c["time_label"] != "??")
    if not times:
        return "未知"
    return f"{times[0]} ~ {times[-1]}"


# ─────────────────────────────────────────────────────────
# 5. AI 点评生成（本地规则，无需联网）
# ─────────────────────────────────────────────────────────

def gen_ai_comment(total: int, all_commits: list[dict]) -> str:
    if total == 0:
        return "今天一条 commit 都没有……是在摸鱼还是在想人生？"

    latest_time = ""
    for c in reversed(all_commits):
        if c["time_label"] != "??":
            latest_time = c["time_label"]
            break

    hour = -1
    if latest_time:
        try:
            hour = int(latest_time.split(":")[0])
        except Exception:
            pass

    # 判断是否跨午夜（凌晨0~5点）
    if 0 <= hour < 6:
        tone = f"凌晨 {latest_time} 还在敲代码！今天属于传说级暴肝，明天记得补觉。"
    elif 22 <= hour <= 23:
        tone = f"晚上 {latest_time} 才收手，妥妥的夜猫子开发者，保重身体。"
    elif 18 <= hour < 22:
        tone = "下班后还在提交，职业选手！"
    elif 9 <= hour < 18:
        tone = "工作时间高效输出，今天很标准的打工人节奏。"
    else:
        tone = "提交时间比较随机，看来今天是「随心流」编程。"

    if total >= 10:
        prefix = f"今日共 {total} 条 commit，堪称日更大神！"
    elif total >= 5:
        prefix = f"今日 {total} 条 commit，产出稳定，继续保持！"
    elif total >= 2:
        prefix = f"今日 {total} 条 commit，小步快跑，没问题。"
    else:
        prefix = f"今日仅 {total} 条 commit，质量大于数量？"

    return f"{prefix}{tone}"


# ─────────────────────────────────────────────────────────
# 6. 格式化输出
# ─────────────────────────────────────────────────────────

BORDER_TOP    = "╔══════════════════════════════════════════════════╗"
BORDER_BOTTOM = "╚══════════════════════════════════════════════════╝"
BORDER_MID    = "╟──────────────────────────────────────────────────╢"


def format_text(result: dict) -> str:
    lines = []
    user_label = result.get("current_user", "")
    lines.append(BORDER_TOP)
    lines.append(f"║  ⚡ GitPulse · 今日提交日报{' ' * 22}║")
    lines.append(f"║  统计日期: {result['date']}{' ' * 37}║")
    lines.append(f"║  时间窗口: {result['window_start']} ~ 次日 {result['window_end']}{' ' * 16}║")
    lines.append(f"║  当前用户: {user_label}{' ' * (38 - len(user_label))}║")
    lines.append(BORDER_BOTTOM)
    lines.append("")

    repos = result["repos"]
    total_commits = result["total_commits"]

    if not repos:
        lines.append("  📭 本次扫描范围内未找到任何 Git 仓库。")
    else:
        for repo in repos:
            repo_name = repo["path"]
            commits = repo["commits"]
            count = len(commits)
            lines.append(f"📦 仓库: {repo_name}  (共 {count} 条提交)")
            lines.append("")
            if not commits:
                lines.append("  （今日无提交）")
            else:
                for i, c in enumerate(commits):
                    lines.append(f"  {i + 1}. [{c['time_label']}] {c['hash']}  {c['message']}")
            lines.append("")

    lines.append(BORDER_MID.replace("╟", "─").replace("╢", "─").replace("─", "─"))
    lines.append("📊 今日统计:")
    lines.append(f"  · 扫描仓库数: {result['repo_count']}")
    lines.append(f"  · 有效提交数: {total_commits}")
    lines.append(f"  · 活跃时段:   {result['active_period']}")
    lines.append("")
    lines.append(f"💬 AI 点评: {result['ai_comment']}")
    lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# 7. 主入口
# ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="⚡ GitPulse — 今日 Git 提交复盘助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gitpulse.py --root e:\\py
  python gitpulse.py --root e:\\py --date 2026-04-09
  python gitpulse.py --root e:\\py --format json
        """,
    )
    parser.add_argument(
        "--root",
        default=os.getcwd(),
        help="Git 仓库根目录（默认: 当前工作目录）",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="指定统计日期，格式 YYYY-MM-DD（默认: 今天）",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式：text（默认，人类可读）或 json（供 AI 解析）",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="子目录最大搜索深度（默认: 3）",
    )

    args = parser.parse_args()

    # 1. 计算时间窗口
    start_dt, end_dt = get_time_window(args.date)
    date_label = start_dt.strftime("%Y-%m-%d")

    # 2. 查找仓库
    repo_paths = find_git_repos(args.root, max_depth=args.depth)

    if not repo_paths and args.format == "text":
        print(f"[GitPulse] ⚠️  在 {args.root} 下（深度{args.depth}）未找到任何 Git 仓库。")
        print(f"  请确认路径正确，或使用 --root 参数指定仓库根目录。")
        return

    # 3. 获取当前 git 用户（取第一个仓库的配置，fallback 全局）
    current_user = get_current_git_user(repo_paths[0] if repo_paths else ".")

    # 4. 收集 commits（仅限当前用户）
    repo_results = []
    all_commits_flat = []

    for repo_path in repo_paths:
        commits = get_commits_in_window(repo_path, start_dt, end_dt, author=current_user)
        repo_results.append({
            "path": repo_path,
            "commits": commits,
        })
        all_commits_flat.extend(commits)

    # 5. 构造汇总结构
    result = {
        "current_user": current_user,
        "date": date_label,
        "window_start": start_dt.strftime("%H:%M"),
        "window_end": end_dt.strftime("%H:%M"),
        "scan_root": args.root,
        "repo_count": len(repo_paths),
        "total_commits": len(all_commits_flat),
        "active_period": calc_active_period(all_commits_flat),
        "ai_comment": gen_ai_comment(len(all_commits_flat), all_commits_flat),
        "repos": repo_results,
    }

    # 5. 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
