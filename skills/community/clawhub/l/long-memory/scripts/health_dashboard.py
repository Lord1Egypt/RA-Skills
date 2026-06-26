#!/usr/bin/env python3
"""记忆健康仪表盘：综合健康报告"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def check_health(memory_dir: Path) -> dict:
    """生成综合健康报告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "scores": {},
        "checks": [],
        "summary": "",
        "recommendations": [],
    }

    total_score = 100
    checks = []

    # 1. 文件完整性
    conv_dir = memory_dir / "conversations"
    if conv_dir.exists():
        files = list(conv_dir.glob("*.md"))
        total_size = sum(f.stat().st_size for f in files)
        checks.append({
            "name": "文件完整性",
            "status": "healthy" if len(files) > 0 else "warning",
            "detail": f"{len(files)} 个对话文件，{total_size / 1024:.1f} KB",
            "score": 10 if len(files) > 0 else 5,
            "max_score": 10,
        })
    else:
        total_score -= 10
        checks.append({"name": "文件完整性", "status": "error", "detail": "对话目录不存在", "score": 0, "max_score": 10})

    # 2. MEMORY.md 状态
    memory_md = memory_dir.parent / "MEMORY.md"
    if memory_md.exists():
        md_size = len(memory_md.read_text(encoding="utf-8"))
        if md_size <= 8000:
            checks.append({"name": "MEMORY.md", "status": "healthy",
                          "detail": f"{md_size} 字（限制 8000）", "score": 10, "max_score": 10})
        else:
            total_score -= 5
            checks.append({"name": "MEMORY.md", "status": "warning",
                          "detail": f"{md_size} 字（超限 {md_size - 8000}）", "score": 5, "max_score": 10})
    else:
        total_score -= 5
        checks.append({"name": "MEMORY.md", "status": "warning", "detail": "文件不存在", "score": 5, "max_score": 10})

    # 3. 标签覆盖率
    if conv_dir.exists():
        tagged = 0
        untagged = 0
        for f in conv_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if "标签" in content:
                tagged += 1
            else:
                untagged += 1
        total = tagged + untagged
        coverage = tagged / max(total, 1) * 100
        status = "healthy" if coverage >= 80 else "warning" if coverage >= 50 else "error"
        score = int(coverage / 10)
        if status != "healthy":
            total_score -= (10 - score)
        checks.append({"name": "标签覆盖率", "status": status,
                      "detail": f"{coverage:.0f}%（{tagged}/{total}）", "score": score, "max_score": 10})

    # 4. 决策标记率
    if conv_dir.exists():
        with_decisions = 0
        total_sessions = 0
        for f in conv_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            sessions = content.count("## [")
            total_sessions += sessions
            if "**关键决策" in content:
                with_decisions += 1
        rate = with_decisions / max(len(list(conv_dir.glob("*.md"))), 1) * 100
        score = int(rate / 10)
        checks.append({"name": "决策标记率", "status": "healthy" if rate >= 50 else "info",
                      "detail": f"{rate:.0f}% 文件有决策标记", "score": score, "max_score": 10})

    # 5. 蒸馏状态
    distill_dir = memory_dir / "distillations"
    if distill_dir.exists():
        distill_count = len(list(distill_dir.glob("*.md")))
        checks.append({"name": "蒸馏文件", "status": "healthy" if distill_count > 0 else "info",
                      "detail": f"{distill_count} 个周蒸馏", "score": min(distill_count * 3, 10), "max_score": 10})
    else:
        checks.append({"name": "蒸馏文件", "status": "info", "detail": "尚未蒸馏", "score": 0, "max_score": 10})

    # 6. 索引状态
    index_file = memory_dir / ".memory_index.json"
    if index_file.exists():
        checks.append({"name": "索引", "status": "healthy", "detail": "索引存在", "score": 10, "max_score": 10})
    else:
        checks.append({"name": "索引", "status": "info", "detail": "索引未构建", "score": 5, "max_score": 10})

    # 7. 备份状态
    import subprocess
    try:
        result = subprocess.run(["git", "status", "--porcelain"], cwd=memory_dir,
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            is_dirty = bool(result.stdout.strip())
            checks.append({"name": "Git 备份", "status": "warning" if is_dirty else "healthy",
                          "detail": "有未提交变更" if is_dirty else "工作区干净", 
                          "score": 5 if is_dirty else 10, "max_score": 10})
        else:
            checks.append({"name": "Git 备份", "status": "info", "detail": "未初始化 Git", "score": 3, "max_score": 10})
    except Exception:
        checks.append({"name": "Git 备份", "status": "info", "detail": "无法检查", "score": 5, "max_score": 10})

    # 8. 完整性校验
    checksum_file = memory_dir / ".checksums.json"
    if checksum_file.exists():
        checks.append({"name": "完整性校验", "status": "healthy", "detail": "校验和文件存在", "score": 10, "max_score": 10})
    else:
        checks.append({"name": "完整性校验", "status": "info", "detail": "未建立校验和", "score": 3, "max_score": 10})

    # 计算总分
    actual_score = sum(c["score"] for c in checks)
    max_score = sum(c["max_score"] for c in checks)
    health_pct = round(actual_score / max(max_score, 1) * 100, 1)

    # 生成建议
    recommendations = []
    for check in checks:
        if check["status"] == "warning":
            recommendations.append(f"⚠️ {check['name']}：{check['detail']}，建议处理")
        elif check["status"] == "error":
            recommendations.append(f"🔴 {check['name']}：{check['detail']}，需要立即修复")
        elif check["status"] == "info":
            recommendations.append(f"ℹ️ {check['name']}：{check['detail']}")

    if health_pct >= 80:
        overall = "🟢 健康"
    elif health_pct >= 60:
        overall = "🟡 良好"
    else:
        overall = "🔴 需要关注"

    report["scores"] = {"health": health_pct, "actual": actual_score, "max": max_score}
    report["checks"] = checks
    report["summary"] = f"{overall}（{health_pct}%）"
    report["recommendations"] = recommendations

    return report


def print_dashboard(report: dict):
    print("=" * 60)
    print(f"🏥 记忆健康仪表盘 {report['summary']}")
    print("=" * 60)

    # 健康条
    pct = report["scores"]["health"]
    filled = int(pct / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"\n  [{bar}] {pct}%")

    print(f"\n📋 检查项：")
    for check in report["checks"]:
        status_icon = {"healthy": "✅", "warning": "⚠️", "error": "🔴", "info": "ℹ️"}
        icon = status_icon.get(check["status"], "•")
        score_bar = "█" * check["score"] + "░" * (check["max_score"] - check["score"])
        print(f"  {icon} {check['name']:<15s} [{score_bar}] {check['detail']}")

    if report["recommendations"]:
        print(f"\n💡 建议：")
        for rec in report["recommendations"]:
            print(f"  {rec}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆健康仪表盘")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    report = check_health(md)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_dashboard(report)
