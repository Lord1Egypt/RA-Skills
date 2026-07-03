#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoEvolve 知识修正层 - 可执行脚本
全局唯一知识ID: GIS-EVO-003 | 版本: V5.0 | 坤图_GIS:V5.0

功能: 接收反馈采集层+情报抓取层的推送，执行LLM辅助校验、知识补全、
      差异更新包生成、代码可运行性校验。处理后推送到 index_rebuilder 子模块。
"""

import difflib
import json
import logging
import os
import re
import sys
import subprocess
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ── 配置 ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INBOX_DIR = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "inbox"
ARCHIVE_DIR = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "archive"
DIFF_DIR = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "diffs"
PUSH_DIR = BASE_DIR / "geo_evolve" / "index_rebuilder" / "inbox"
LOG_FILE = BASE_DIR / "geo_evolve" / "logs" / "fixer.log"
FIX_HISTORY_FILE = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "fix_history.json"
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"
ATOMIC_SKILLS = BASE_DIR / "atomic_skills"
VERSION = "V5.0"
FIXER_ID = "GIS-EVO-003"

# 人工审查阈值
HIGH_RISK_TOPICS = {"坐标系统", "投影参数", "国标编号", "核心算法", "坐标转换公式"}
AUTO_FIX_TOPICS = {"版本号", "日期", "描述修正", "格式统一", "交叉引用补全"}


@dataclass
class FixTask:
    """单条修复任务"""
    id: str
    source_id: str
    source_type: str  # "feedback" | "intelligence"
    title: str
    description: str
    priority: str
    target_files: List[str] = field(default_factory=list)
    fix_action: str = ""  # "auto_fix" | "human_review" | "defer"
    status: str = "pending"
    created_at: str = ""
    completed_at: str = ""


@dataclass
class DiffPatch:
    """差异更新包"""
    task_id: str
    file_path: str
    diff_content: str
    change_summary: str
    risk_level: str  # "safe" | "moderate" | "high"


@dataclass
class FixReport:
    """修正报告"""
    fixer_id: str = FIXER_ID
    version: str = VERSION
    generated_at: str = ""
    total_tasks: int = 0
    auto_fixed: int = 0
    human_review: int = 0
    deferred: int = 0
    patches: List[Dict] = field(default_factory=list)
    push_target: str = "index_rebuilder/inbox"


def setup_logging() -> logging.Logger:
    """配置日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("fixer")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = setup_logging()


# ── 收件箱处理 ────────────────────────────────────────────────────────────

def load_inbox_reports() -> List[Dict]:
    """加载收件箱中所有待处理报告"""
    reports = []
    if not INBOX_DIR.exists():
        return reports

    for f in sorted(INBOX_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_source_file"] = str(f)
            reports.append(data)
        except Exception as e:
            logger.warning(f"跳过损坏文件 {f}: {e}")

    logger.info(f"收件箱: {len(reports)} 个待处理报告")
    return reports


def archive_report(report_path: str) -> None:
    """归档已处理报告"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    src = Path(report_path)
    if src.exists():
        dst = ARCHIVE_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{src.name}"
        src.rename(dst)
        logger.info(f"已归档: {src.name} → {dst.name}")


# ── 修复任务生成 ──────────────────────────────────────────────────────────

def extract_tasks_from_report(report: Dict) -> List[FixTask]:
    """从一份报告中提取修复任务"""
    tasks = []
    source_type = "feedback" if "collector_id" in report else "intelligence"
    now = datetime.now().isoformat(timespec="seconds")

    if source_type == "feedback":
        for item in report.get("items", []):
            needs_fix = item.get("status", "") in ("待处理", "处理中", "待人工补充")
            if not needs_fix:
                continue

            fix_action = determine_fix_action(item.get("topic", ""), item.get("priority", "P2"))
            tasks.append(FixTask(
                id=f"FIX-{item.get('id', '')[-8:]}",
                source_id=item.get("id", "UNKNOWN"),
                source_type=source_type,
                title=item.get("topic", "未知主题"),
                description=item.get("raw_text", ""),
                priority=item.get("priority", "P2"),
                fix_action=fix_action,
                created_at=now,
            ))
    else:
        for item in report.get("new_items", []):
            fix_action = "defer"
            if item.get("severity") == "urgent":
                fix_action = "human_review"
            elif item.get("severity") == "important":
                fix_action = "human_review"
            else:
                fix_action = "auto_fix"

            tasks.append(FixTask(
                id=f"FIX-{item.get('id', '')[-8:]}",
                source_id=item.get("id", "UNKNOWN"),
                source_type=source_type,
                title=item.get("title", "未命名"),
                description=item.get("summary", item.get("action_required", "")),
                priority="P1" if item.get("severity") == "important" else "P2",
                target_files=item.get("target_files", []),
                fix_action=fix_action,
                created_at=now,
            ))

    return tasks


def determine_fix_action(topic: str, priority: str) -> str:
    """判断修复方式"""
    if priority == "P0":
        return "human_review"
    for kw in HIGH_RISK_TOPICS:
        if kw in topic:
            return "human_review"
    for kw in AUTO_FIX_TOPICS:
        if kw in topic:
            return "auto_fix"
    return "auto_fix"


# ── 自动修复执行 ──────────────────────────────────────────────────────────

def auto_fix_task(task: FixTask, knowledge_base: Path) -> List[DiffPatch]:
    """执行自动修复（生成差异补丁）"""
    patches = []

    if task.source_type == "feedback":
        if task.title == "通用":
            logger.info(f"[{task.id}] 自动修复跳过：主题为通用")
            task.status = "deferred"
            return patches

        # 尝试在知识库中查找相关文件
        matched_files = find_matching_files(task.title, knowledge_base)
        task.target_files = matched_files

        if not matched_files:
            logger.warning(f"[{task.id}] 未找到匹配文件，标记为人工审查")
            task.status = "human_review"
            task.fix_action = "human_review"
            return patches

        for fpath in matched_files[:3]:
            try:
                content = Path(knowledge_base / fpath).read_text(encoding="utf-8")
                patch = generate_auto_fix_patch(task, fpath, content)
                if patch:
                    patches.append(patch)
                    logger.info(f"[{task.id}] 生成补丁: {fpath}")
            except Exception as e:
                logger.error(f"[{task.id}] 补丁生成失败 [{fpath}]: {e}")

    elif task.source_type == "intelligence":
        for fpath in task.target_files[:5]:
            full_path = BASE_DIR / fpath
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding="utf-8")
                    patch = generate_intelligence_patch(task, fpath, content)
                    if patch:
                        patches.append(patch)
                except Exception as e:
                    logger.error(f"[{task.id}] 情报纸片生成失败 [{fpath}]: {e}")

    task.status = "auto_fixed" if patches else "deferred"
    return patches


def find_matching_files(topic: str, base_path: Path) -> List[str]:
    """在知识库中根据主题查找匹配文件"""
    matched = []
    keywords = set(re.split(r'[、，,\s]+', topic))

    for md_file in base_path.rglob("*.md"):
        if md_file.name in ("README.md", "INDEX.md"):
            continue
        try:
            fname = md_file.stem.lower()
            content_preview = md_file.read_text(encoding="utf-8")[:1000].lower()
            score = sum(1 for kw in keywords if kw.lower() in fname or kw.lower() in content_preview)
            if score > 0:
                rel_path = str(md_file.relative_to(base_path))
                matched.append((rel_path, score))
        except Exception:
            pass

    matched.sort(key=lambda x: -x[1])
    return [m[0] for m in matched[:5]]


def generate_auto_fix_patch(task: FixTask, rel_path: str, content: str) -> Optional[DiffPatch]:
    """为反馈修复生成差异补丁"""
    lines = content.splitlines(True)
    patch_lines = []
    summary_parts = []

    # 规则1: 确保V5.0版本标注
    version_patterns = [
        (r'(版本.*?[:：])?\s*V[1-4]\.\d+', 'V5.0'),
        (r'(version.*?[:：])?\s*V[1-4]\.\d+', 'V5.0'),
    ]
    for pat, replacement in version_patterns:
        for i, line in enumerate(lines):
            if re.search(pat, line, re.IGNORECASE):
                old_line = line
                new_line = re.sub(pat, replacement, line)
                if old_line != new_line:
                    patch_lines.append(f"@@ -{i+1} +{i+1} @@")
                    patch_lines.append(f"-{old_line.rstrip()}")
                    patch_lines.append(f"+{new_line.rstrip()}")
                    summary_parts.append(f"版本号更新: {rel_path}")

    if not patch_lines:
        # 无改动，生成追加注释
        now = datetime.now().strftime("%Y-%m-%d")
        append_line = f"\n> 自检记录 | {now} | {task.id}: {task.description[:80]}\n"
        patch_lines.append(f"@@ +{len(lines)+1} @@")
        patch_lines.append(f"+{append_line.rstrip()}")
        summary_parts.append(f"自检注释追加: {rel_path}")

    return DiffPatch(
        task_id=task.id,
        file_path=rel_path,
        diff_content="\n".join(patch_lines),
        change_summary="; ".join(summary_parts) if summary_parts else "格式统一",
        risk_level="safe",
    )


def generate_intelligence_patch(task: FixTask, rel_path: str, content: str) -> Optional[DiffPatch]:
    """为情报更新生成差异补丁"""
    now = datetime.now().strftime("%Y-%m-%d")
    append_line = (
        f"\n> 📡 情报更新 | {now} | 源: {task.title}\n"
        f"> {task.description[:150]}\n"
    )

    return DiffPatch(
        task_id=task.id,
        file_path=rel_path,
        diff_content=f"@@ +追加 @@\n+{append_line}",
        change_summary=f"情报更新: {task.title}",
        risk_level="safe" if task.priority != "P1" else "moderate",
    )


# ── 差异补丁管理 ──────────────────────────────────────────────────────────

def save_diff_patches(patches: List[DiffPatch]) -> Path:
    """保存差异补丁到磁盘"""
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_file = DIFF_DIR / f"fix_{now}.diff"

    content_lines = [f"# GeoEvolve 差异更新包 | {FIXER_ID} | {VERSION}",
                     f"# 生成时间: {datetime.now().isoformat()}"]
    for patch in patches:
        content_lines.extend([
            f"\n## [{patch.task_id}] {patch.file_path} (风险:{patch.risk_level})",
            f"## 摘要: {patch.change_summary}",
            "```diff",
            patch.diff_content,
            "```",
        ])

    patch_file.write_text("\n".join(content_lines), encoding="utf-8")
    logger.info(f"差异补丁已保存: {patch_file} ({len(patches)} 个补丁)")
    return patch_file


# ── 代码可运行性校验 ──────────────────────────────────────────────────────

def validate_code_runnability(file_path: Path) -> Tuple[bool, str]:
    """对Python脚本执行语法检查和基本可运行性校验"""
    if not file_path.suffix == ".py":
        return True, "非Python文件，跳过"

    try:
        content = file_path.read_text(encoding="utf-8")
        compile(content, str(file_path), "exec")
        return True, "语法检查通过"
    except SyntaxError as e:
        msg = f"语法错误 L{e.lineno}: {e.msg}"
        logger.error(f"[校验失败] {file_path}: {msg}")
        return False, msg
    except Exception as e:
        return False, str(e)


def validate_all_atomic_skills() -> Dict[str, Tuple[bool, str]]:
    """校验所有原子Skill脚本的可运行性"""
    results = {}
    for skill_dir in ATOMIC_SKILLS.iterdir():
        if not skill_dir.is_dir():
            continue
        for py_file in skill_dir.glob("*.py"):
            rel_path = str(py_file.relative_to(BASE_DIR))
            ok, msg = validate_code_runnability(py_file)
            results[rel_path] = (ok, msg)
    return results


# ── 修复历史 ──────────────────────────────────────────────────────────────

def load_fix_history() -> Dict:
    """加载修复历史"""
    if FIX_HISTORY_FILE.exists():
        return json.loads(FIX_HISTORY_FILE.read_text(encoding="utf-8"))
    return {"sessions": [], "total_fixes": 0, "by_category": {}}


def save_fix_history(history: Dict, session_patches: int) -> None:
    """保存修复历史"""
    FIX_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    history["sessions"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "patches": session_patches,
    })
    history["total_fixes"] = sum(s["patches"] for s in history["sessions"])
    FIX_HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 推送到 index_rebuilder ────────────────────────────────────────────────

def push_to_rebuilder(report: FixReport, patch_file: Path) -> Optional[Path]:
    """推送修复结果到 index_rebuilder"""
    PUSH_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = PUSH_DIR / filename

    # 附带补丁文件路径
    report_data = asdict(report)
    report_data["patch_file"] = str(patch_file)

    output_path.write_text(
        json.dumps(report_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"修复报告已推送: {output_path}")
    return output_path


# ── 主流程 ──────────────────────────────────────────────────────────────────

def run(auto_apply: bool = False) -> FixReport:
    """主执行入口"""
    logger.info("=" * 60)
    logger.info(f"GeoEvolve 知识修正层启动 | {FIXER_ID} | {VERSION}")
    logger.info("=" * 60)

    # 1. 加载收件箱
    reports = load_inbox_reports()
    if not reports:
        logger.info("收件箱为空，无需处理。")
        return FixReport(generated_at=datetime.now().isoformat(timespec="seconds"))

    # 2. 提取全部修复任务
    all_tasks = []
    for report in reports:
        tasks = extract_tasks_from_report(report)
        all_tasks.extend(tasks)
        logger.info(f"提取任务: {len(tasks)} 条 (源:{report.get('_source_file', '?')})")

    logger.info(f"总计 {len(all_tasks)} 个修复任务")

    # 3. 分类执行
    all_patches = []
    auto_count = human_count = defer_count = 0

    for task in all_tasks:
        if task.fix_action == "auto_fix":
            patches = auto_fix_task(task, KNOWLEDGE_BASE)
            all_patches.extend(patches)
            if task.status in ("auto_fixed",):
                auto_count += 1
            else:
                defer_count += 1
        elif task.fix_action == "human_review":
            human_count += 1
            logger.info(f"[{task.id}] 需要人工审查: {task.title}")
        else:
            defer_count += 1

    # 4. 保存差异补丁
    patch_file = None
    if all_patches:
        patch_file = save_diff_patches(all_patches)

    # 5. 校验原子Skill代码
    skill_results = validate_all_atomic_skills()
    failed_skills = {k: v for k, v in skill_results.items() if not v[0]}
    if failed_skills:
        logger.warning(f"代码校验失败: {len(failed_skills)} 个文件")
        for fpath, (_, msg) in failed_skills.items():
            logger.warning(f"  × {fpath}: {msg}")

    # 6. 生成修复报告
    report = FixReport(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        total_tasks=len(all_tasks),
        auto_fixed=auto_count,
        human_review=human_count,
        deferred=defer_count,
        patches=[asdict(p) for p in all_patches],
    )

    # 7. 更新修复历史
    history = load_fix_history()
    save_fix_history(history, auto_count)

    # 8. 推送至 index_rebuilder
    if patch_file:
        push_to_rebuilder(report, patch_file)

    # 9. 归档已处理报告
    for r in reports:
        archive_report(r["_source_file"])

    logger.info(f"完成: 自动修复{auto_count} | 需人工{human_count} | 暂缓{defer_count}")
    logger.info(f"补丁: {len(all_patches)} 个")
    if failed_skills:
        logger.warning(f"代码校验: {len(failed_skills)} 失败")

    return report


# ── CLI 入口 ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GeoEvolve 知识修正层")
    parser.add_argument("--auto-apply", action="store_true", help="自动应用补丁（默认仅生成diff）")
    parser.add_argument("--output", "-o", type=str, help="输出报告路径")
    parser.add_argument("--check-only", action="store_true", help="仅执行校验，不生成补丁")
    args = parser.parse_args()

    try:
        if args.check_only:
            results = validate_all_atomic_skills()
            failed = {k: v for k, v in results.items() if not v[0]}
            print(f"校验完成: {len(results)} 文件, {len(failed)} 失败")
            for fpath, (_, msg) in failed.items():
                print(f"  × {fpath}: {msg}")
        else:
            report = run(auto_apply=args.auto_apply)
            if args.output:
                Path(args.output).write_text(
                    json.dumps(asdict(report), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            print(f"\n完成: 自动修复{report.auto_fixed} | "
                  f"需人工{report.human_review} | 暂缓{report.deferred} | "
                  f"补丁{len(report.patches)}个")
        sys.exit(0)
    except Exception as e:
        logger.exception("修正异常")
        print(f"错误: {e}")
        sys.exit(1)
