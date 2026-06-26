#!/usr/bin/env python3
"""
site_monitor.py — 统一网站监控入口

整合 Canvas 和 FSP 监控，同步到 workspace/upcoming.md。

upcoming.md 分区格式:
  ## 🔮 FUTURE   — 7天内事件（自动+手动）
  ## 📌 MANUAL   — 手动添加的长期事件
  ## ✅ DONE     — 已完成事件（@done:日期 超7天后自动删除）
  ## ⏰ OVERDUE  — 已过期未完成事件
"""

import logging
import re
from datetime import datetime, timedelta, date
from pathlib import Path

logger = logging.getLogger("heartbeat.site_monitor")

WORKSPACE = Path(__file__).parent.parent / "workspace"
UPCOMING_FILE = WORKSPACE / "upcoming.md"

# 分区标识
SECTION_FUTURE = "FUTURE"
SECTION_MANUAL = "MANUAL"
SECTION_DONE = "DONE"
SECTION_OVERDUE = "OVERDUE"

# 正则：解析事件行
# 格式: - YYYY-MM-DD | 描述 | [分类] @tag:value ...
# 或完成: - [x] YYYY-MM-DD | 描述 | [分类] @done:YYYY-MM-DD ...
EVENT_RE = re.compile(
    r"^-\s*(?:\[([xX ])\]\s*)?(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)(?:\s*\|\s*(.+))?$"
)

# 提取标签 @key:value
TAG_RE = re.compile(r"@(\w+):([^\s@]+)")


def run_sync() -> dict:
    """
    执行完整同步流程:
    1. 调用 canvas_monitor.sync()
    2. 调用 fsp_monitor.sync()
    3. 读取当前 upcoming.md
    4. 合并事件（去重、更新、新增）
    5. 区域迁移（过期→OVERDUE）
    6. 清理 DONE 超7天记录
    7. 写回 upcoming.md

    返回: {"added": int, "updated": int, "removed": int, "errors": list}
    """
    result = {"added": 0, "updated": 0, "removed": 0, "errors": []}
    today = datetime.now().date()

    # 1-2. 获取远程事件
    # active_sources: 实际成功运行并返回数据的来源集合
    # 只有 active_sources 里的来源，才会触发"删除已消失事件"逻辑
    remote_events = []
    active_sources: set[str] = set()

    try:
        from tools.canvas_monitor import sync as canvas_sync, is_configured as canvas_configured
        if canvas_configured():
            canvas_events = canvas_sync()
            remote_events.extend(canvas_events)
            active_sources.add("canvas")
            logger.info("Canvas: %d 个事件", len(canvas_events))
        else:
            logger.info("Canvas: 未配置 token，跳过（保留现有数据）")
    except Exception as e:
        msg = f"Canvas 同步失败: {e}"
        logger.error(msg)
        result["errors"].append(msg)

    try:
        from tools.fsp_monitor import sync as fsp_sync, is_configured as fsp_configured
        if fsp_configured():
            fsp_events = fsp_sync()
            remote_events.extend(fsp_events)
            active_sources.add("fsp")
            logger.info("FSP: %d 个事件", len(fsp_events))
        else:
            logger.info("FSP: 未配置 token，跳过（保留现有数据）")
    except Exception as e:
        msg = f"FSP 同步失败: {e}"
        logger.error(msg)
        result["errors"].append(msg)

    # 3. 读取当前 upcoming.md
    sections = _read_upcoming()

    # 4. 合并远程事件到 FUTURE 区
    remote_ids = {e["id"] for e in remote_events}
    existing_ids = {}  # id -> section_name, index

    # 索引所有自动事件的 ID
    for section_name in (SECTION_FUTURE, SECTION_DONE, SECTION_OVERDUE):
        for i, entry in enumerate(sections[section_name]):
            eid = entry.get("tags", {}).get("id")
            if eid:
                existing_ids[eid] = (section_name, i)

    # 添加/更新远程事件
    for event in remote_events:
        eid = event["id"]
        new_entry = _event_to_entry(event)

        if eid in existing_ids:
            section_name, idx = existing_ids[eid]
            old_entry = sections[section_name][idx]
            # 只更新 FUTURE/OVERDUE 中的事件（DONE 的不覆盖）
            if section_name != SECTION_DONE:
                sections[section_name][idx] = new_entry
                result["updated"] += 1
        else:
            sections[SECTION_FUTURE].append(new_entry)
            result["added"] += 1

    # 删除已消失的自动事件（仅 FUTURE 区中有 @src 且该 src 已激活的）
    future_keep = []
    for entry in sections[SECTION_FUTURE]:
        src = entry.get("tags", {}).get("src")
        eid = entry.get("tags", {}).get("id")
        # 只删除来自"已激活来源"且不在 remote_ids 中的事件
        if src and eid and src in active_sources and eid not in remote_ids:
            result["removed"] += 1
            logger.info("移除已消失事件: %s", entry.get("description", eid))
        else:
            future_keep.append(entry)
    sections[SECTION_FUTURE] = future_keep

    # 5. 区域迁移
    _migrate_sections(sections, today)

    # 6. 清理 DONE 超7天记录
    _cleanup_done(sections, today)

    # 7. 写回
    _write_upcoming(sections)

    logger.info(
        "site_monitor 同步完成: +%d ~%d -%d (错误:%d)",
        result["added"], result["updated"], result["removed"], len(result["errors"]),
    )
    return result


def _read_upcoming() -> dict:
    """
    读取 upcoming.md，解析为分区结构。

    返回: {
        "FUTURE": [entry, ...],
        "MANUAL": [entry, ...],
        "DONE": [entry, ...],
        "OVERDUE": [entry, ...],
    }

    如果文件不存在或是旧格式，自动迁移。
    """
    sections = {
        SECTION_FUTURE: [],
        SECTION_MANUAL: [],
        SECTION_DONE: [],
        SECTION_OVERDUE: [],
    }

    if not UPCOMING_FILE.exists():
        return sections

    content = UPCOMING_FILE.read_text(encoding="utf-8")

    # 检查是否是新分区格式
    if "## 🔮 FUTURE" in content or "## FUTURE" in content:
        return _parse_sectioned(content)
    else:
        # 旧格式，迁移到新格式
        return _migrate_old_format(content)


def _parse_sectioned(content: str) -> dict:
    """解析分区格式的 upcoming.md"""
    sections = {
        SECTION_FUTURE: [],
        SECTION_MANUAL: [],
        SECTION_DONE: [],
        SECTION_OVERDUE: [],
    }

    current_section = None

    for line in content.splitlines():
        stripped = line.strip()

        # 检测分区标题
        if "FUTURE" in stripped and stripped.startswith("##"):
            current_section = SECTION_FUTURE
            continue
        elif "MANUAL" in stripped and stripped.startswith("##"):
            current_section = SECTION_MANUAL
            continue
        elif "DONE" in stripped and stripped.startswith("##"):
            current_section = SECTION_DONE
            continue
        elif "OVERDUE" in stripped and stripped.startswith("##"):
            current_section = SECTION_OVERDUE
            continue
        elif stripped.startswith("# "):
            # 一级标题，不改变分区
            continue

        if current_section is None:
            continue

        # 跳过空行和注释
        if not stripped or stripped.startswith("<!--"):
            continue

        # 解析事件行
        entry = _parse_event_line(stripped)
        if entry:
            sections[current_section].append(entry)

    return sections


def _migrate_old_format(content: str) -> dict:
    """将旧格式 upcoming.md 迁移为分区结构"""
    sections = {
        SECTION_FUTURE: [],
        SECTION_MANUAL: [],
        SECTION_DONE: [],
        SECTION_OVERDUE: [],
    }

    today = datetime.now().date()

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        entry = _parse_event_line(stripped)
        if not entry:
            continue

        if entry.get("done"):
            sections[SECTION_DONE].append(entry)
        elif entry.get("date") and entry["date"] < today:
            sections[SECTION_OVERDUE].append(entry)
        else:
            # 有 @src 的进 FUTURE，无 @src 的进 MANUAL
            if entry.get("tags", {}).get("src"):
                sections[SECTION_FUTURE].append(entry)
            else:
                sections[SECTION_FUTURE].append(entry)

    logger.info("旧格式 upcoming.md 已迁移到分区格式")
    return sections


def _parse_event_line(line: str) -> dict | None:
    """
    解析单行事件。

    返回: {
        "date": date,
        "date_str": "YYYY-MM-DD",
        "description": str,
        "category": str | None,
        "tags": {"time": ..., "src": ..., "id": ..., "due": ..., "done": ...},
        "done": bool,
        "raw_rest": str,  # | 后面的原始内容（用于写回）
    }
    """
    m = EVENT_RE.match(line)
    if not m:
        return None

    checkbox = m.group(1)
    date_str = m.group(2)
    description = m.group(3).strip()
    rest = m.group(4) or ""

    try:
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    done = checkbox is not None and checkbox.lower() == "x"

    # 解析分类 [tag]
    category = None
    cat_match = re.search(r"\[([^\]]+)\]", rest)
    if cat_match:
        category = cat_match.group(1)

    # 解析所有 @key:value 标签
    tags = {}
    for tag_match in TAG_RE.finditer(rest):
        tags[tag_match.group(1)] = tag_match.group(2)
    # 也检查 description 中的标签
    for tag_match in TAG_RE.finditer(description):
        tags[tag_match.group(1)] = tag_match.group(2)

    return {
        "date": event_date,
        "date_str": date_str,
        "description": description,
        "category": category,
        "tags": tags,
        "done": done,
        "raw_rest": rest.strip(),
    }


def _event_to_entry(event: dict) -> dict:
    """将标准化事件转换为 entry 格式"""
    event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
    tags = {"src": event["src"], "id": event["id"]}
    if event.get("time"):
        tags["time"] = event["time"]
    if event.get("due"):
        tags["due"] = event["due"]

    return {
        "date": event_date,
        "date_str": event["date"],
        "description": event["description"],
        "category": event.get("category"),
        "tags": tags,
        "done": False,
        "raw_rest": "",  # 写回时重新生成
    }


def _migrate_sections(sections: dict, today: date):
    """区域迁移：过期的 FUTURE 事件移到 OVERDUE"""
    future_keep = []
    for entry in sections[SECTION_FUTURE]:
        if entry.get("done"):
            # 完成的移到 DONE
            if "done" not in entry.get("tags", {}):
                entry.setdefault("tags", {})["done"] = today.isoformat()
            sections[SECTION_DONE].append(entry)
        elif entry["date"] < today:
            # 过期的移到 OVERDUE
            sections[SECTION_OVERDUE].append(entry)
        else:
            future_keep.append(entry)
    sections[SECTION_FUTURE] = future_keep

    # MANUAL 中过期的不移动（用户自己管理）


def _cleanup_done(sections: dict, today: date):
    """清理 DONE 区超7天的记录"""
    cutoff = today - timedelta(days=7)
    keep = []
    removed = 0

    for entry in sections[SECTION_DONE]:
        done_date_str = entry.get("tags", {}).get("done")
        if done_date_str:
            try:
                done_date = datetime.strptime(done_date_str, "%Y-%m-%d").date()
                if done_date < cutoff:
                    removed += 1
                    continue
            except ValueError:
                pass
        keep.append(entry)

    if removed:
        logger.info("清理了 %d 条超过7天的已完成事件", removed)
    sections[SECTION_DONE] = keep


def _entry_to_line(entry: dict, done: bool = False) -> str:
    """将 entry 转换回 markdown 行"""
    parts = []

    if done or entry.get("done"):
        parts.append(f"- [x] {entry['date_str']}")
    else:
        parts.append(f"- {entry['date_str']}")

    parts.append(entry["description"])

    # 第三部分：分类 + 标签
    rest_parts = []
    if entry.get("category"):
        rest_parts.append(f"[{entry['category']}]")

    tags = entry.get("tags", {})
    for key in ("time", "due", "src", "id", "done"):
        if key in tags:
            rest_parts.append(f"@{key}:{tags[key]}")

    if rest_parts:
        parts.append(" ".join(rest_parts))

    return " | ".join(parts)


def _write_upcoming(sections: dict):
    """将分区结构写回 upcoming.md"""
    lines = []
    lines.append("# Upcoming Events")
    lines.append("<!-- 自动生成部分由 site_monitor.py 维护，手动添加的事件请在 MANUAL 区域 -->")
    lines.append("")

    # FUTURE
    lines.append("## 🔮 FUTURE （7天内事件，自动+手动）")
    future_sorted = sorted(sections[SECTION_FUTURE], key=lambda e: (e["date"], e.get("tags", {}).get("time", "99:99")))
    if future_sorted:
        for entry in future_sorted:
            lines.append(_entry_to_line(entry))
    else:
        lines.append("（暂无近期事件）")
    lines.append("")

    # MANUAL
    lines.append("## 📌 MANUAL （手动添加的长期事件，不受自动清理影响）")
    if sections[SECTION_MANUAL]:
        for entry in sorted(sections[SECTION_MANUAL], key=lambda e: e["date"]):
            lines.append(_entry_to_line(entry))
    else:
        lines.append("（暂无手动事件）")
    lines.append("")

    # DONE
    lines.append("## ✅ DONE （已完成，事件日期+7天后自动删除）")
    if sections[SECTION_DONE]:
        for entry in sorted(sections[SECTION_DONE], key=lambda e: e["date"], reverse=True):
            lines.append(_entry_to_line(entry, done=True))
    else:
        lines.append("（暂无已完成事件）")
    lines.append("")

    # OVERDUE
    lines.append("## ⏰ OVERDUE （已过期未完成）")
    if sections[SECTION_OVERDUE]:
        for entry in sorted(sections[SECTION_OVERDUE], key=lambda e: e["date"]):
            lines.append(_entry_to_line(entry))
    else:
        lines.append("（暂无过期事件）")
    lines.append("")

    # 原子写入
    content = "\n".join(lines)
    tmp = UPCOMING_FILE.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.rename(UPCOMING_FILE)
    logger.info("upcoming.md 已更新")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
    result = run_sync()
    print(f"\n同步结果: +{result['added']} ~{result['updated']} -{result['removed']}")
    if result["errors"]:
        print("错误:")
        for e in result["errors"]:
            print(f"  - {e}")
