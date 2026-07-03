#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoEvolve 索引重建层 - 可执行脚本
全局唯一知识ID: GIS-EVO-004 | 版本: V5.0 | 坤图_GIS:V5.0

功能: 接收知识修正层的差异更新包，增量刷新向量索引、知识图谱、
      全局检索索引、KNOWLEDGE_ID_MAP。支持灰度发布和一键回滚。
"""

import hashlib
import json
import logging
import os
import shutil
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

# ── 配置 ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INBOX_DIR = BASE_DIR / "geo_evolve" / "index_rebuilder" / "inbox"
ARCHIVE_DIR = BASE_DIR / "geo_evolve" / "index_rebuilder" / "archive"
LOG_FILE = BASE_DIR / "geo_evolve" / "logs" / "rebuilder.log"
REBUILD_STATE_FILE = BASE_DIR / "geo_evolve" / "index_rebuilder" / "rebuild_state.json"
BACKUP_ROOT = BASE_DIR / "geo_evolve" / "index_rebuilder" / "index_snapshots"

# 索引路径
VECTOR_INDEX_DIR = BASE_DIR / "geo_kg" / "vector_index"
VECTOR_INDEX_V2_DIR = BASE_DIR / "geo_kg" / "vector_index_v2"
KG_TRIPLES_FILE = BASE_DIR / "geo_kg" / "relations" / "TRIPLES.json"
KG_INDEX_FILE = BASE_DIR / "geo_kg" / "index" / "GEOKG_INDEX.md"
KNOWLEDGE_ID_MAP = BASE_DIR / "geo_kg" / "entities" / "KNOWLEDGE_ID_MAP.md"
GLOBAL_INDEX_FILE = BASE_DIR / "knowledge_base" / "FULL_INDEX.md"
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"
ATOMIC_SKILLS = BASE_DIR / "atomic_skills"

VERSION = "V5.0"
REBUILDER_ID = "GIS-EVO-004"

# 重建策略阈值
THRESHOLD_NEW_DOCS = 10
THRESHOLD_NEW_ENTITIES = 5
THRESHOLD_GRAYSCALE_DAYS = 7


@dataclass
class IndexSnapshot:
    """索引快照"""
    timestamp: str
    version: str
    vector_docs: int = 0
    kg_triples: int = 0
    global_entries: int = 0
    knowledge_ids: int = 0
    source_patch: str = ""


@dataclass
class RebuildReport:
    """重建报告"""
    rebuilder_id: str = REBUILDER_ID
    version: str = VERSION
    generated_at: str = ""
    actions: List[str] = field(default_factory=list)
    vector_updated: bool = False
    kg_updated: bool = False
    global_index_updated: bool = False
    id_map_updated: bool = False
    snapshot_id: str = ""
    rollback_supported: bool = True


def setup_logging() -> logging.Logger:
    """配置日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("rebuilder")
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
    """加载待处理修复报告"""
    reports = []
    if not INBOX_DIR.exists():
        return reports
    for f in sorted(INBOX_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_source"] = str(f)
            reports.append(data)
        except Exception as e:
            logger.warning(f"跳过损坏报告 {f}: {e}")
    return reports


def archive_report(report_path: str) -> None:
    """归档已处理报告"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    src = Path(report_path)
    if src.exists():
        dst = ARCHIVE_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{src.name}"
        src.rename(dst)


# ── 索引重建逻辑 ──────────────────────────────────────────────────────────

def scan_knowledge_base() -> Dict[str, Any]:
    """扫描知识库获取当前统计"""
    stats = {
        "total_files": 0,
        "total_lines": 0,
        "files_by_group": {},
        "atomic_skills": 0,
        "entities": set(),
    }

    for md_file in KNOWLEDGE_BASE.rglob("*.md"):
        stats["total_files"] += 1
        group = md_file.parent.name if md_file.parent != KNOWLEDGE_BASE else "root"
        stats["files_by_group"][group] = stats["files_by_group"].get(group, 0) + 1

        try:
            content = md_file.read_text(encoding="utf-8")
            stats["total_lines"] += len(content.splitlines())

            # 提取知识ID
            for match in re.finditer(r'GIS-(?:REF|SKL|EVO|KG)-\d+', content):
                stats["entities"].add(match.group(0))
        except Exception:
            pass

    for skill_dir in ATOMIC_SKILLS.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            stats["atomic_skills"] += 1

    stats["entities"] = sorted(stats["entities"])
    return stats


def rebuild_vector_index(stats: Dict) -> bool:
    """重建/增量更新向量索引"""
    VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_INDEX_V2_DIR.mkdir(parents=True, exist_ok=True)

    # 生成文档嵌入清单
    manifest = {
        "version": VERSION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_docs": stats["total_files"],
        "doc_embeddings_available": False,
        "note": "向量嵌入需在有embedding模型的环境中生成。当前索引记录文档路径及元数据，支持后续批量嵌入。",
        "docs": [],
    }

    doc_id = 0
    for md_file in sorted(KNOWLEDGE_BASE.rglob("*.md")):
        doc_id += 1
        manifest["docs"].append({
            "id": doc_id,
            "path": str(md_file.relative_to(BASE_DIR)),
            "title": md_file.stem,
            "size_bytes": md_file.stat().st_size,
            "last_modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
        })

    manifest_path = VECTOR_INDEX_V2_DIR / "vector_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"向量索引清单已生成: {manifest_path} ({manifest['total_docs']} 文档)")

    # 灰度发布：V2目录写入新索引，7天后切换
    return True


def rebuild_knowledge_graph(stats: Dict, patches: List[Dict]) -> bool:
    """增量更新知识图谱三元组"""
    # 加载现有三元组
    existing_triples = []
    if KG_TRIPLES_FILE.exists():
        try:
            existing_triples = json.loads(KG_TRIPLES_FILE.read_text(encoding="utf-8"))
        except Exception:
            existing_triples = []

    # 从扫描结果生成新三元组
    new_triples = []
    for entity in stats["entities"]:
        parts = entity.split("-")
        if len(parts) >= 3:
            category = parts[1] if len(parts) > 1 else "UNK"
            new_triples.append({
                "subject": entity,
                "predicate": "belongsTo",
                "object": f"Category:{category}",
                "source": "rebuilder_scan",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            })

    # 从补丁中提取三元组变更
    if patches:
        for patch in patches:
            task_id = patch.get("task_id", "")
            file_path = patch.get("file_path", "")
            if file_path:
                new_triples.append({
                    "subject": task_id,
                    "predicate": "modifies",
                    "object": file_path,
                    "source": "fix_patch",
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })

    # 合并去重
    seen = set()
    merged = []
    for t in existing_triples + new_triples:
        key = (t["subject"], t["predicate"], t["object"])
        if key not in seen:
            seen.add(key)
            merged.append(t)

    KG_TRIPLES_FILE.parent.mkdir(parents=True, exist_ok=True)
    KG_TRIPLES_FILE.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"知识图谱已更新: {len(merged)} 三元组 (+{len(new_triples)} 新增)")

    return len(new_triples) > 0


def rebuild_global_index(stats: Dict) -> bool:
    """重建全局检索索引（倒排索引）"""
    need_full = stats["total_files"] > THRESHOLD_NEW_DOCS

    index_entries = [
        f"# GIS_SKILL V5.0 全局检索索引",
        f"> 重建时间: {datetime.now().isoformat(timespec='seconds')}",
        f"> 总文件: {stats['total_files']} | 总行数: {stats['total_lines']}",
        "",
    ]

    if need_full:
        # 按群组组织索引
        for group_name in sorted(stats["files_by_group"].keys()):
            count = stats["files_by_group"][group_name]
            index_entries.append(f"## {group_name} ({count} 文件)")
            group_dir = KNOWLEDGE_BASE / group_name
            if group_dir.is_dir():
                for md_file in sorted(group_dir.glob("*.md")):
                    title = md_file.stem
                    rel_path = str(md_file.relative_to(BASE_DIR))
                    size_kb = md_file.stat().st_size / 1024
                    index_entries.append(f"- [{title}]({rel_path}) ({size_kb:.1f}KB)")
            index_entries.append("")

        # 原子Skill索引
        index_entries.append(f"## atomic_skills ({stats['atomic_skills']} 技能)")
        for skill_dir in sorted(ATOMIC_SKILLS.iterdir()):
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    rel_path = str(skill_md.relative_to(BASE_DIR))
                    index_entries.append(f"- [{skill_dir.name}]({rel_path})")
        index_entries.append("")

        # 知识ID索引
        index_entries.append(f"## 知识ID映射 ({len(stats['entities'])} 实体)")
        for entity in sorted(stats["entities"]):
            index_entries.append(f"- `{entity}`")
    else:
        index_entries.append("> 增量更新模式：文件数未达全量重建阈值。")
        index_entries.append(f"> 当前文件数: {stats['total_files']} / 阈值: {THRESHOLD_NEW_DOCS}")

    GLOBAL_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    GLOBAL_INDEX_FILE.write_text("\n".join(index_entries), encoding="utf-8")
    logger.info(f"全局索引已更新: {GLOBAL_INDEX_FILE}")

    return need_full


def rebuild_id_map(stats: Dict) -> bool:
    """更新KNOWLEDGE_ID_MAP"""
    content_lines = [
        f"# 知识ID映射表",
        f"> 版本: {VERSION} | 更新: {datetime.now().isoformat(timespec='seconds')}",
        f"> 总知识ID: {len(stats['entities'])}",
        "",
        "| 知识ID | 类型 | 对应文件 | 状态 |",
        "|--------|------|----------|------|",
    ]

    id_type_map = {
        "REF": "参考文档",
        "SKL": "原子Skill",
        "EVO": "自进化模块",
        "KG": "知识图谱节点",
    }

    for entity in stats["entities"]:
        parts = entity.split("-")
        id_type = parts[1] if len(parts) > 1 else "UNK"
        type_name = id_type_map.get(id_type, "未知")

        # 查找对应文件
        matching_files = []
        for md_file in KNOWLEDGE_BASE.rglob("*.md"):
            try:
                if entity in md_file.read_text(encoding="utf-8"):
                    matching_files.append(str(md_file.relative_to(BASE_DIR)))
            except Exception:
                pass
        file_ref = matching_files[0] if matching_files else "未找到"

        content_lines.append(f"| `{entity}` | {type_name} | {file_ref} | 活跃 |")

    KNOWLEDGE_ID_MAP.parent.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_ID_MAP.write_text("\n".join(content_lines), encoding="utf-8")
    logger.info(f"ID映射已更新: {len(stats['entities'])} 实体")

    return True


def create_snapshot(report: RebuildReport) -> str:
    """创建索引快照，支持回滚"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_id = f"snapshot_{timestamp}"
    snapshot_dir = BACKUP_ROOT / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # 备份关键索引文件
    files_to_backup = {
        "TRIPLES.json": KG_TRIPLES_FILE,
        "GEOKG_INDEX.md": KG_INDEX_FILE,
        "KNOWLEDGE_ID_MAP.md": KNOWLEDGE_ID_MAP,
        "FULL_INDEX.md": GLOBAL_INDEX_FILE,
        "vector_manifest.json": VECTOR_INDEX_V2_DIR / "vector_manifest.json",
    }

    backed_up = []
    for name, file_path in files_to_backup.items():
        if file_path.exists():
            dst = snapshot_dir / name
            shutil.copy2(file_path, dst)
            backed_up.append(name)

    # 写快照元数据
    metadata = asdict(IndexSnapshot(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        version=VERSION,
        vector_docs=len(list(VECTOR_INDEX_V2_DIR.glob("*"))) if VECTOR_INDEX_V2_DIR.exists() else 0,
        kg_triples=len(json.loads(KG_TRIPLES_FILE.read_text(encoding="utf-8"))) if KG_TRIPLES_FILE.exists() else 0,
        global_entries=len(GLOBAL_INDEX_FILE.read_text(encoding="utf-8").splitlines()) if GLOBAL_INDEX_FILE.exists() else 0,
        knowledge_ids=len(KNOWLEDGE_ID_MAP.read_text(encoding="utf-8").splitlines()) if KNOWLEDGE_ID_MAP.exists() else 0,
        source_patch="manual" if not report.vector_updated else "auto",
    ))
    (snapshot_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"快照已创建: {snapshot_id} ({len(backed_up)} 文件)")
    return snapshot_id


# ── 回滚功能 ──────────────────────────────────────────────────────────────

def list_snapshots() -> List[str]:
    """列出所有可用快照"""
    if not BACKUP_ROOT.exists():
        return []
    return sorted(
        [d.name for d in BACKUP_ROOT.iterdir() if d.is_dir() and d.name.startswith("snapshot_")],
        reverse=True,
    )


def rollback_to(snapshot_id: str) -> bool:
    """回滚到指定快照"""
    snapshot_dir = BACKUP_ROOT / snapshot_id
    if not snapshot_dir.exists():
        logger.error(f"快照不存在: {snapshot_id}")
        return False

    files_to_restore = {
        "TRIPLES.json": KG_TRIPLES_FILE,
        "GEOKG_INDEX.md": KG_INDEX_FILE,
        "KNOWLEDGE_ID_MAP.md": KNOWLEDGE_ID_MAP,
        "FULL_INDEX.md": GLOBAL_INDEX_FILE,
        "vector_manifest.json": VECTOR_INDEX_V2_DIR / "vector_manifest.json",
    }

    restored = 0
    for name, target in files_to_restore.items():
        src = snapshot_dir / name
        if src.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            restored += 1

    logger.info(f"回滚完成: {snapshot_id} (恢复{restored}个文件)")
    return True


# ── 灰度发布 ──────────────────────────────────────────────────────────────

def check_grayscale_switch() -> bool:
    """检查是否应切换灰度索引（V2 → 主索引）"""
    if not VECTOR_INDEX_V2_DIR.exists():
        return False

    manifest_path = VECTOR_INDEX_V2_DIR / "vector_manifest.json"
    if not manifest_path.exists():
        return False

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        generated_at = datetime.fromisoformat(manifest["generated_at"])
        elapsed = (datetime.now() - generated_at).days
        return elapsed >= THRESHOLD_GRAYSCALE_DAYS
    except Exception:
        return False


def switch_grayscale() -> bool:
    """执行灰度切换：V2 → 主索引"""
    if not check_grayscale_switch():
        return False

    # 备份旧索引
    if VECTOR_INDEX_DIR.exists():
        old_backup = VECTOR_INDEX_DIR.with_name("vector_index_v1_bak")
        if old_backup.exists():
            shutil.rmtree(old_backup)
        shutil.copytree(VECTOR_INDEX_DIR, old_backup)
        shutil.rmtree(VECTOR_INDEX_DIR)

    # 切换
    shutil.copytree(VECTOR_INDEX_V2_DIR, VECTOR_INDEX_DIR)
    logger.info("灰度切换完成: V2 → 主索引")
    return True


# ── 清理旧快照 ────────────────────────────────────────────────────────────

def cleanup_old_snapshots(keep: int = 10) -> int:
    """保留最近N个快照，删除旧的"""
    snapshots = list_snapshots()
    if len(snapshots) <= keep:
        return 0

    removed = 0
    for old in snapshots[keep:]:
        old_dir = BACKUP_ROOT / old
        shutil.rmtree(old_dir)
        removed += 1
        logger.info(f"清理旧快照: {old}")

    return removed


# ── 主流程 ──────────────────────────────────────────────────────────────────

def run() -> RebuildReport:
    """主执行入口"""
    logger.info("=" * 60)
    logger.info(f"GeoEvolve 索引重建层启动 | {REBUILDER_ID} | {VERSION}")
    logger.info("=" * 60)

    report = RebuildReport(generated_at=datetime.now().isoformat(timespec="seconds"))

    # 1. 加载收件箱报告
    inbox_reports = load_inbox_reports()
    if inbox_reports:
        report.actions.append(f"收件箱: {len(inbox_reports)} 个报告")
        logger.info(f"收件箱: {len(inbox_reports)} 个报告")

    # 2. 扫描知识库
    stats = scan_knowledge_base()
    report.actions.append(
        f"扫描: {stats['total_files']}文件, {stats['total_lines']}行, "
        f"{stats['atomic_skills']}技能, {len(stats['entities'])}知识ID"
    )
    logger.info(f"扫描: {stats['total_files']}文件, {len(stats['entities'])}知识ID")

    # 3. 重建向量索引
    report.vector_updated = rebuild_vector_index(stats)
    if report.vector_updated:
        report.actions.append("向量索引已更新")

    # 4. 增量更新知识图谱
    patches = []
    for r in inbox_reports:
        patches.extend(r.get("patches", []))
    report.kg_updated = rebuild_knowledge_graph(stats, patches)
    if report.kg_updated:
        report.actions.append(f"知识图谱已更新")

    # 5. 重建全局检索索引
    report.global_index_updated = rebuild_global_index(stats)
    if report.global_index_updated:
        report.actions.append("全局检索索引已全量重建")
    else:
        report.actions.append("全局检索索引: 增量模式（未达全量阈值）")

    # 6. 更新知识ID映射
    report.id_map_updated = rebuild_id_map(stats)
    if report.id_map_updated:
        report.actions.append("知识ID映射已更新")

    # 7. 创建快照
    snapshot_id = create_snapshot(report)
    report.snapshot_id = snapshot_id
    report.actions.append(f"快照: {snapshot_id}")

    # 8. 检查灰度切换
    if check_grayscale_switch():
        switched = switch_grayscale()
        if switched:
            report.actions.append("灰度索引已切换: V2 → 主索引")

    # 9. 清理旧快照
    cleaned = cleanup_old_snapshots(keep=10)
    if cleaned > 0:
        report.actions.append(f"清理 {cleaned} 个旧快照")

    # 10. 归档已处理报告
    for r in inbox_reports:
        archive_report(r["_source"])

    logger.info(f"重建完成: 快照={snapshot_id}")
    return report


# ── CLI 入口 ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GeoEvolve 索引重建层")
    parser.add_argument("--rollback-to", type=str, help="回滚到指定快照ID")
    parser.add_argument("--list-snapshots", action="store_true", help="列出所有快照")
    parser.add_argument("--switch-grayscale", action="store_true", help="手动执行灰度切换")
    parser.add_argument("--output", "-o", type=str, help="输出报告路径")
    args = parser.parse_args()

    try:
        if args.list_snapshots:
            snaps = list_snapshots()
            print(f"可用快照: {len(snaps)} 个")
            for s in snaps:
                print(f"  {s}")
        elif args.rollback_to:
            ok = rollback_to(args.rollback_to)
            if ok:
                print(f"回滚成功: {args.rollback_to}")
            else:
                print(f"回滚失败: 快照 {args.rollback_to} 不存在")
                sys.exit(1)
        elif args.switch_grayscale:
            ok = switch_grayscale()
            print(f"灰度切换: {'成功' if ok else '未满足切换条件'}")
        else:
            report = run()
            if args.output:
                Path(args.output).write_text(
                    json.dumps(asdict(report), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            print(f"\n完成: {'; '.join(report.actions)}")
        sys.exit(0)
    except Exception as e:
        logger.exception("重建异常")
        print(f"错误: {e}")
        sys.exit(1)
