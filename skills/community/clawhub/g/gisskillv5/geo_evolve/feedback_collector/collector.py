#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoEvolve 反馈采集层 - 可执行脚本
全局唯一知识ID: GIS-EVO-001 | 版本: V5.0 | 坤图_GIS:V5.0

功能: 自动解析用户反馈日志，识别报错/知识缺口/精度不足/新需求，
      生成分类归因报告并推送至 knowledge_fixer 子模块。
"""

import json
import os
import re
import sys
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# ── 配置 ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FEEDBACK_DIR = BASE_DIR / "feedback"
LOG_FILE = BASE_DIR / "geo_evolve" / "logs" / "collector.log"
PUSH_DIR = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "inbox"
VERSION = "V5.0"
COLLECTOR_ID = "GIS-EVO-001"

# 反馈类型定义（与 feedback/feedback_log.md 对齐）
FEEDBACK_TYPES = {
    "纠正": {"triggers": ["不对", "错了", "不是这样", "应该是", "其实是"], "priority": "P0"},
    "补充": {"triggers": ["补充一下", "还有", "另外", "相关项目", "相关单位"], "priority": "P1"},
    "追问": {"triggers": ["还有呢", "还有别的", "具体怎么操作", "能详细点"], "priority": "P2"},
    "报错": {"triggers": ["报错", "Error", "失败", "Exception", "无法"], "priority": "P0"},
    "精度不足": {"triggers": ["精度不够", "偏差大", "不准确", "误差"], "priority": "P1"},
    "打分": {"triggers": ["很好", "没用", "一般", "有帮助", "没帮助"], "priority": "P3"},
}


@dataclass
class FeedbackItem:
    """单条反馈数据结构"""
    id: str
    timestamp: str
    feedback_type: str
    raw_text: str
    topic: str
    priority: str
    status: str = "待处理"
    source_file: str = ""


@dataclass
class CollectorReport:
    """反馈采集汇总报告"""
    collector_id: str = COLLECTOR_ID
    version: str = VERSION
    generated_at: str = ""
    period_start: str = ""
    period_end: str = ""
    total_items: int = 0
    items: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    push_target: str = "knowledge_fixer/inbox"


def setup_logging() -> logging.Logger:
    """配置日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("collector")
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


# ── 核心逻辑 ──────────────────────────────────────────────────────────────

def classify_feedback(text: str) -> Tuple[str, str]:
    """根据关键词分类反馈类型和优先级"""
    text_lower = text.lower()
    for ftype, meta in FEEDBACK_TYPES.items():
        for trigger in meta["triggers"]:
            if trigger.lower() in text_lower:
                return ftype, meta["priority"]
    return "补充", "P2"  # 默认


def extract_topic(text: str) -> str:
    """从反馈文字中提取主题"""
    patterns = [
        r"(?:关于|关于这个)?['\"\u201c](.+?)['\"\u201d]",
        r"([\w\u4e00-\u9fff]+(?:坐标系|投影|转换|模型|标准|规范|数据|格式|软件|参数))",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return "通用"


def parse_feedback_log(log_path: Path, since: Optional[datetime] = None) -> List[FeedbackItem]:
    """解析 feedback_log.md 提取所有反馈条目"""
    if not log_path.exists():
        logger.warning(f"反馈日志不存在: {log_path}")
        return []

    items = []
    content = log_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("| 2026"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 6:
            continue

        date_str = parts[0]
        ftype = parts[1]
        raw_text = parts[2]
        topic = parts[3]
        status = parts[5] if len(parts) > 5 else "待处理"

        if since:
            try:
                dt = datetime.fromisoformat(date_str)
                if dt < since:
                    continue
            except (ValueError, TypeError):
                pass

        ftype_auto, priority_auto = classify_feedback(raw_text)
        if ftype_auto == "纠正" and ftype != "纠正":
            ftype = ftype_auto
            priority_auto = "P0"

        item_id = hashlib.md5(f"{date_str}:{raw_text}".encode()).hexdigest()[:8]
        items.append(FeedbackItem(
            id=f"FB-{item_id}",
            timestamp=date_str,
            feedback_type=ftype,
            raw_text=raw_text,
            topic=extract_topic(raw_text),
            priority=priority_auto,
            status=status,
            source_file=str(log_path.name),
        ))

    logger.info(f"解析反馈日志: {len(items)} 条")
    return items


def parse_knowledge_gaps(gaps_path: Path) -> List[FeedbackItem]:
    """解析 knowledge_gaps.md 追踪表"""
    if not gaps_path.exists():
        logger.warning(f"知识缺口表不存在: {gaps_path}")
        return []

    items = []
    content = gaps_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("| G0"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 5:
            continue

        gap_id = parts[0]
        date_str = parts[1]
        desc = parts[2]
        priority = parts[3] if len(parts) > 3 else "P2"
        status = parts[4] if len(parts) > 4 else "待处理"

        items.append(FeedbackItem(
            id=gap_id,
            timestamp=date_str,
            feedback_type="知识缺口",
            raw_text=desc,
            topic=extract_topic(desc),
            priority=priority,
            status=status,
            source_file=gaps_path.name,
        ))

    logger.info(f"解析知识缺口表: {len(items)} 条")
    return items


def deduplicate(items: List[FeedbackItem]) -> List[FeedbackItem]:
    """去重：同话题+同类型保留最新"""
    seen: Dict[str, FeedbackItem] = {}
    for item in sorted(items, key=lambda x: x.timestamp):
        key = f"{item.topic}:{item.feedback_type}"
        seen[key] = item
    return list(seen.values())


def generate_report(items: List[FeedbackItem], period_days: int = 30) -> CollectorReport:
    """生成反馈采集汇总报告"""
    now = datetime.now()
    since = now - timedelta(days=period_days)
    recent = [i for i in items if i.timestamp >= since.strftime("%Y-%m-%d")]

    report = CollectorReport(
        generated_at=now.isoformat(timespec="seconds"),
        period_start=since.strftime("%Y-%m-%d"),
        period_end=now.strftime("%Y-%m-%d"),
        total_items=len(recent),
        items=[asdict(i) for i in recent],
        summary={
            "按类型统计": {},
            "按优先级统计": {},
            "按状态统计": {},
            "需要立即处理(P0)": [],
            "高优(P1)": [],
        }
    )

    for item in recent:
        report.summary["按类型统计"][item.feedback_type] = \
            report.summary["按类型统计"].get(item.feedback_type, 0) + 1
        report.summary["按优先级统计"][item.priority] = \
            report.summary["按优先级统计"].get(item.priority, 0) + 1
        report.summary["按状态统计"][item.status] = \
            report.summary["按状态统计"].get(item.status, 0) + 1
        if item.priority == "P0":
            report.summary["需要立即处理(P0)"].append(item.id)
        elif item.priority == "P1":
            report.summary["高优(P1)"].append(item.id)

    return report


def push_to_fixer(report: CollectorReport) -> Optional[Path]:
    """推送报告至 knowledge_fixer/inbox"""
    PUSH_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"collector_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = PUSH_DIR / filename

    output_path.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"报告已推送: {output_path}")
    return output_path


def run(period_days: int = 30) -> CollectorReport:
    """主执行入口"""
    logger.info("=" * 60)
    logger.info(f"GeoEvolve 反馈采集层启动 | {COLLECTOR_ID} | {VERSION}")
    logger.info("=" * 60)

    all_items = []

    # 1. 解析反馈日志
    feedback_log = FEEDBACK_DIR / "feedback_log.md"
    all_items.extend(parse_feedback_log(feedback_log))

    # 2. 解析知识缺口表
    gaps_file = FEEDBACK_DIR / "knowledge_gaps.md"
    all_items.extend(parse_knowledge_gaps(gaps_file))

    # 3. 去重
    before = len(all_items)
    all_items = deduplicate(all_items)
    logger.info(f"去重: {before} → {len(all_items)}")

    # 4. 生成报告
    report = generate_report(all_items, period_days)
    logger.info(f"报告生成: {report.total_items} 条反馈 (近{period_days}天)")

    # 5. 推送至 knowledge_fixer
    push_to_fixer(report)

    # 6. 输出摘要
    logger.info(f"按优先级: {report.summary['按优先级统计']}")
    logger.info(f"P0紧急项: {len(report.summary['需要立即处理(P0)'])}")
    logger.info(f"P1高优项: {len(report.summary['高优(P1)'])}")
    logger.info("采集完成。")

    return report


# ── CLI 入口 ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GeoEvolve 反馈采集层")
    parser.add_argument("--days", type=int, default=30, help="统计天数 (默认30)")
    parser.add_argument("--output", "-o", type=str, help="输出报告路径")
    args = parser.parse_args()

    try:
        report = run(period_days=args.days)
        if args.output:
            Path(args.output).write_text(
                json.dumps(asdict(report), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        print(f"\n完成: {report.total_items} 条反馈已采集，已推送至 knowledge_fixer。")
        sys.exit(0)
    except Exception as e:
        logger.exception("采集异常")
        print(f"错误: {e}")
        sys.exit(1)
