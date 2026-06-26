#!/usr/bin/env python3
"""
lobster-novel: lesson bridge — 创作教训 → lobster-evolver 自进化系统

把写作过程中的问题（质量评审P0/P1、API错误、连续性风险）
自动转化为 ATOMIC/FUNCTIONAL lessons，驱动自进化。

用法:
  python3 novel_lesson_bridge.py --from-review report.json
  python3 novel_lesson_bridge.py --from-error "API timeout"
  python3 novel_lesson_bridge.py --aggregate
  python3 novel_lesson_bridge.py --sync          # 同步到 self-improving
"""
import json, sys
from pathlib import Path
from datetime import datetime, timezone

# ── 路径 ──────────────────────────────────────────────────────────
LOBSTER_EVOLVER = Path(os.environ.get("LOBSTER_EVOLVER", "."))
ATOMIC_DIR = LOBSTER_EVOLVER / "lessons" / "ATOMIC"
FUNC_DIR   = LOBSTER_EVOLVER / "lessons" / "FUNCTIONAL"
BRIDGE_SCRIPT = LOBSTER_EVOLVER / "scripts" / "bridge_to_self_improving.py"


def _lesson_id(prefix: str, description: str) -> str:
    """生成唯一 lesson ID: novel_<prefix>_<date>_<slug>"""
    from hashlib import md5
    slug = md5(description.encode()).hexdigest()[:8]
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"novel_{prefix}_{now}_{slug}"


def _write_atomic(lesson: dict):
    """写入 ATOMIC lesson JSON 文件"""
    ATOMIC_DIR.mkdir(parents=True, exist_ok=True)
    fpath = ATOMIC_DIR / f"{lesson['id']}.json"
    fpath.write_text(json.dumps(lesson, ensure_ascii=False, indent=2))
    return fpath


# ── Quality Check Issues → ATOMIC ────────────────────────────────

def from_quality_check(issues: list, chapter: int):
    """把 quality_check 的 P0/P1 问题写为 ATOMIC lessons"""
    written = []
    for iss in issues:
        sev = iss.get("severity", "P1")
        if sev not in ("P0", "P1"):
            continue

        desc = iss.get("description", "")
        cat = iss.get("category", "quality")
        role = iss.get("role", "Editor")
        fix = iss.get("suggestion", "")

        lesson = {
            "id": _lesson_id("qc", desc),
            "type": "ATOMIC",
            "source": "lobster-novel/quality_check",
            "severity": "MAJOR" if sev == "P0" else "MINOR",
            "rule": f"[写作质量] {role}: {cat} — {desc[:80]}",
            "context": f"Chapter {chapter} — {desc}",
            "suggestion": fix or "修复质量问题",
            "file": f"skills/lobster-novel/chapters/ch{chapter:03d}.md",
            "line": iss.get("line", 0),
            "dimension": cat,
            "novel_chapter": chapter,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _write_atomic(lesson)
        written.append(lesson["id"])
    return written


# ── API / Runtime Errors → ATOMIC ────────────────────────────────

def from_error(error_msg: str, chapter: int = 0, source: str = "chapter_generator"):
    """把运行时错误写为 ATOMIC lesson，返回 [lesson_id]"""
    lesson = {
        "id": _lesson_id("err", error_msg),
        "type": "ATOMIC",
        "source": f"lobster-novel/{source}",
        "severity": "MAJOR",
        "rule": f"[运行错误] {error_msg[:100]}",
        "context": f"Chapter {chapter}: {error_msg}",
        "suggestion": "检查 API key、网络、或输入格式",
        "file": f"skills/lobster-novel/chapters/ch{chapter:03d}.md" if chapter else "",
        "line": 0,
        "dimension": "Runtime",
        "novel_chapter": chapter,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    fpath = _write_atomic(lesson)
    return [str(fpath.stem)]


# ── 聚合 → FUNCTIONAL lessons ────────────────────────────────────

def aggregate():
    """聚合近期 novel ATOMIC lessons 为 FUNCTIONAL lessons"""
    if not ATOMIC_DIR.exists():
        print("ATOMIC dir not found")
        return

    novel_lessons = []
    for f in sorted(ATOMIC_DIR.glob("novel_*.json")):
        try:
            novel_lessons.append(json.loads(f.read_text()))
        except Exception:
            continue

    if not novel_lessons:
        print(f"No novel lessons to aggregate")
        return

    # 按 dimension / category 分组
    from collections import Counter
    by_cat = {}
    for l in novel_lessons:
        key = l.get("dimension", l.get("rule", "other"))[:40]
        by_cat.setdefault(key, []).append(l)

    # 生成 FUNCTIONAL lesson
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    func = {
        "id": f"novel_func_{now}",
        "type": "FUNCTIONAL",
        "source": "lobster-novel/aggregator",
        "chapter_range": {
            "min": min(l.get("novel_chapter", 0) for l in novel_lessons),
            "max": max(l.get("novel_chapter", 0) for l in novel_lessons),
        },
        "total_lessons": len(novel_lessons),
        "categories": dict(Counter(l.get("dimension", "other") for l in novel_lessons)),
        "rules": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    for cat, lessons in by_cat.items():
        func["rules"].append({
            "category": cat,
            "count": len(lessons),
            "consolidated_rule": _consolidate(cat, lessons),
        })

    FUNC_DIR.mkdir(parents=True, exist_ok=True)
    fpath = FUNC_DIR / f"{func['id']}.json"
    fpath.write_text(json.dumps(func, ensure_ascii=False, indent=2))
    print(f"Aggregated {len(novel_lessons)} lessons → {fpath.name}")
    return str(fpath)


def _consolidate(cat: str, lessons: list) -> str:
    """从一组 lessons 提炼通用规则"""
    suggestions = set(l.get("suggestion", "") for l in lessons if l.get("suggestion"))
    combined = "; ".join(f for f in suggestions if f)
    if not combined:
        rules = set(l.get("rule", "") for l in lessons)
        combined = "; ".join(r[:60] for r in list(rules)[:3])
    return combined or "注意写作规范"


# ── Sync → self-improving ────────────────────────────────────────

def sync():
    """调用 bridge_to_self_improving 同步到 ~/self-improving/"""
    if BRIDGE_SCRIPT.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(BRIDGE_SCRIPT)],
            capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.returncode != 0:
            print(f"sync stderr: {result.stderr[:300]}")
            return False
        return True
    else:
        print(f"bridge script not found: {BRIDGE_SCRIPT}")
        return False


# ── CLI ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="novel lesson bridge")
    parser.add_argument("--from-review", help="quality report JSON file")
    parser.add_argument("--from-error", help="error message string")
    parser.add_argument("--chapter", type=int, default=0, help="chapter number")
    parser.add_argument("--aggregate", action="store_true", help="aggregate lessons")
    parser.add_argument("--sync", action="store_true", help="sync to self-improving")
    args = parser.parse_args()

    if args.from_review:
        try:
            report = json.loads(Path(args.from_review).read_text())
            issues = report.get("issues", [])
            ids = from_quality_check(issues, args.chapter)
            print(f"Written {len(ids)} lessons from review")
        except Exception as e:
            print(f"Error reading review file: {e}")

    if args.from_error:
        lids = from_error(args.from_error, args.chapter)
        print(f"Written error lesson: {lids[0]}")

    if args.aggregate:
        aggregate()

    if args.sync:
        sync()
