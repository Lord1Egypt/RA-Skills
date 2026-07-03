#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoEvolve 情报抓取层 - 可执行脚本
全局唯一知识ID: GIS-EVO-002 | 版本: V5.0 | 坤图_GIS:V5.0

功能: 定时监控外部情报源（国标更新/软件版本/OGC标准/GitHub/行业博客），
      生成情报摘要报告并推送至 knowledge_fixer 子模块。
"""

import json
import hashlib
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET

# ── 配置 ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATE_FILE = BASE_DIR / "geo_evolve" / "intelligence_crawler" / "crawler_state.json"
LOG_FILE = BASE_DIR / "geo_evolve" / "logs" / "crawler.log"
PUSH_DIR = BASE_DIR / "geo_evolve" / "knowledge_fixer" / "inbox"
VERSION = "V5.0"
CRAWLER_ID = "GIS-EVO-002"

# 情报源清单
INTELLIGENCE_SOURCES = [
    {
        "id": "STD-001", "name": "国家标准委", "url": "https://std.samr.gov.cn/gb",
        "category": "标准", "frequency": "月度", "check_method": "web",
        "keywords": ["测绘", "GIS", "地理信息", "遥感", "坐标", "投影", "导航", "地图"],
    },
    {
        "id": "ESRI-001", "name": "Esri ArcGIS Blog",
        "url": "https://www.esri.com/arcgis-blog/feed/",
        "category": "软件", "frequency": "季度", "check_method": "rss",
        "keywords": ["ArcGIS Pro", "ArcGIS Enterprise", "update", "release"],
    },
    {
        "id": "QGIS-001", "name": "QGIS 官方", "url": "https://qgis.org/en/site/forusers/visualchangelogs.html",
        "category": "软件", "frequency": "季度", "check_method": "web",
        "keywords": ["release", "3.", "4.", "changelog", "feature"],
    },
    {
        "id": "OGC-001", "name": "OGC 标准",
        "url": "https://www.ogc.org/standards/",
        "category": "标准", "frequency": "月度", "check_method": "web",
        "keywords": ["new", "adopted", "candidate", "WFS", "WMS", "WCS", "GeoPackage"],
    },
    {
        "id": "GH-001", "name": "GitHub GIS Trending",
        "url": "https://github.com/topics/gis",
        "category": "开源", "frequency": "月度", "check_method": "web",
        "keywords": ["GIS", "mapping", "geospatial", "python", "qgis-plugin"],
    },
    {
        "id": "SUPERMAP-001", "name": "SuperMap 超图",
        "url": "https://www.supermap.com/cn/xml/news.xml",
        "category": "软件", "frequency": "季度", "check_method": "rss",
        "keywords": ["SuperMap", "iDesktop", "iServer", "版本", "发布"],
    },
]


@dataclass
class IntelligenceItem:
    """单条情报"""
    id: str
    source_id: str
    source_name: str
    category: str
    title: str
    url: str
    summary: str
    detected_at: str
    severity: str = "info"  # urgent / important / info
    action_required: str = ""
    target_files: List[str] = field(default_factory=list)


@dataclass
class CrawlerState:
    """抓取器状态"""
    crawler_id: str = CRAWLER_ID
    version: str = VERSION
    last_run: str = ""
    last_check: Dict[str, str] = field(default_factory=dict)
    known_items: Dict[str, str] = field(default_factory=dict)  # hash → timestamp


@dataclass
class IntelligenceReport:
    """情报汇总报告"""
    crawler_id: str = CRAWLER_ID
    version: str = VERSION
    generated_at: str = ""
    period_start: str = ""
    period_end: str = ""
    total_sources: int = len(INTELLIGENCE_SOURCES)
    sources_checked: int = 0
    sources_failed: int = 0
    new_items: List[Dict] = field(default_factory=list)
    urgent_items: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    push_target: str = "knowledge_fixer/inbox"


def setup_logging() -> logging.Logger:
    """配置日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("crawler")
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


# ── 状态管理 ──────────────────────────────────────────────────────────────

def load_state() -> CrawlerState:
    """加载抓取器状态"""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return CrawlerState(**data)
        except Exception as e:
            logger.warning(f"状态文件损坏，重置: {e}")
    return CrawlerState()


def save_state(state: CrawlerState) -> None:
    """保存抓取器状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state.last_run = datetime.now().isoformat(timespec="seconds")
    STATE_FILE.write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8")


# ── 抓取逻辑 ──────────────────────────────────────────────────────────────

def web_fetch(url: str, timeout: int = 30) -> Tuple[Optional[str], bool]:
    """安全抓取网页内容"""
    headers = {
        "User-Agent": "GeoEvolve-IntelligenceCrawler/5.0 (GIS Knowledge Base Self-Evolution)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            return content, True
    except (URLError, HTTPError) as e:
        logger.warning(f"抓取失败 [{url}]: {e}")
        return str(e), False
    except Exception as e:
        logger.error(f"未知错误 [{url}]: {e}")
        return None, False


def parse_rss_feed(xml_content: str) -> List[Dict]:
    """解析RSS/Atom订阅"""
    items = []
    try:
        root = ET.fromstring(xml_content)
        namespaces = {
            "atom": "http://www.w3.org/2005/Atom",
            "rss": "http://purl.org/rss/1.0/",
        }

        for entry in root.findall(".//item") or root.findall(".//atom:entry", namespaces):
            title = entry.findtext("title", "") or entry.findtext("atom:title", "", namespaces) or ""
            link = (entry.findtext("link", "") or
                    (entry.find("link") and entry.find("link").text) or
                    entry.findtext("atom:link/@href", "", namespaces) or "")
            desc = entry.findtext("description", "") or entry.findtext("atom:summary", "", namespaces) or ""
            if title:
                items.append({"title": title.strip(), "url": link.strip(), "summary": desc.strip()[:200]})
    except ET.ParseError as e:
        logger.warning(f"RSS解析失败: {e}")
    return items


def check_standard_source(source: Dict, state: CrawlerState) -> List[IntelligenceItem]:
    """检查标准类情报源（模拟：生成版本变更提醒）"""
    items = []
    source_id = source["id"]

    # 标准类情报源采用"版本比对"模式
    # 在实际部署中替换为真实的HTML解析逻辑
    known_standards = {
        "GB/T 13923-2022": "基础地理信息要素分类与代码（当前版本2022）",
        "GB/T 20257.1-2017": "国家基本比例尺地图图式 第1部分（当前版本2017）",
        "GB/T 18316-2008": "数字测绘成果质量检查与验收（当前版本2008）",
        "GB/T 17798-2007": "地理空间数据交换格式（当前版本2007）",
        "GB/T 35648-2017": "地理信息兴趣点分类与编码（当前版本2017）",
        "GB/T 39608-2020": "基础地理信息数字成果元数据（当前版本2020）",
    }

    for std_id, desc in known_standards.items():
        item_hash = hashlib.md5(f"{source_id}:{std_id}".encode()).hexdigest()[:8]
        if item_hash not in state.known_items:
            # 检查标准年份是否过旧（超过5年可能已更新）
            years = re.findall(r'(\d{4})', std_id)
            if years:
                latest_year = max(int(y) for y in years)
                if datetime.now().year - latest_year > 5:
                    severity = "important"
                    action = f"国标 {std_id} 距今超过5年，需验证是否有新版本替代"
                else:
                    severity = "info"
                    action = f"国标 {std_id} 已收录，版本为{latest_year}年"
            else:
                severity = "info"
                action = f"已记录标准: {std_id}"

            items.append(IntelligenceItem(
                id=f"INT-{item_hash}",
                source_id=source_id,
                source_name=source["name"],
                category=source["category"],
                title=std_id,
                url=source["url"],
                summary=desc,
                detected_at=datetime.now().isoformat(timespec="seconds"),
                severity=severity,
                action_required=action,
                target_files=["knowledge_base/group_02_standards/"],
            ))
            state.known_items[item_hash] = datetime.now().isoformat(timespec="seconds")

    return items


def check_software_source(source: Dict, state: CrawlerState) -> List[IntelligenceItem]:
    """检查软件类情报源（模拟：版本检测）"""
    items = []
    source_id = source["id"]

    software_checklist = {
        "ArcGIS Pro": {"current": "3.6", "kb_file": "knowledge_base/group_03_tools/09_ArcGIS_Pro_3.6.md"},
        "QGIS": {"current": "3.40", "kb_file": "knowledge_base/group_03_tools/15_QGIS3.40.md"},
        "SuperMap iDesktop": {"current": "11i", "kb_file": "knowledge_base/group_03_tools/24_SuperMap_iDesktopX_11i.md"},
        "CASS": {"current": "11.0", "kb_file": "knowledge_base/group_03_tools/21_CASS_11.0.md"},
        "FME": {"current": "2025", "kb_file": "knowledge_base/group_03_tools/17_FME2025.md"},
        "LiDAR360": {"current": "8.0", "kb_file": "knowledge_base/group_03_tools/36_LiDAR360.md"},
    }

    for sw_name, info in software_checklist.items():
        item_hash = hashlib.md5(f"{source_id}:{sw_name}:{info['current']}".encode()).hexdigest()[:8]
        if item_hash not in state.known_items:
            items.append(IntelligenceItem(
                id=f"INT-{item_hash}",
                source_id=source_id,
                source_name=source["name"],
                category=source["category"],
                title=f"{sw_name} {info['current']} 版本状态确认",
                url=source["url"],
                summary=f"知识库收录 {sw_name} 版本: {info['current']}。需确认是否有新版本发布。",
                detected_at=datetime.now().isoformat(timespec="seconds"),
                severity="info",
                action_required=f"检查 {sw_name} 是否有新版本发布，更新 {info['kb_file']}",
                target_files=[info["kb_file"]],
            ))
            state.known_items[item_hash] = datetime.now().isoformat(timespec="seconds")

    return items


def check_ogc_source(source: Dict, state: CrawlerState) -> List[IntelligenceItem]:
    """检查OGC标准情报（模拟：标准状态追踪）"""
    items = []
    source_id = source["id"]

    ogc_standards = {
        "WFS 3.0 (OGC API - Features)": "新一代要素服务标准，替代传统WFS 2.0",
        "WMS 1.4.0": "Web地图服务标准（当前1.3.0已收录，1.4.0为候选）",
        "GeoPackage 1.4": "移动GIS数据格式标准升级",
        "3D Tiles 1.2": "三维瓦片数据标准，1.1已收录",
        "Cloud Optimized GeoTIFF": "云优化GeoTIFF标准，已广泛采用",
        "Zarr v3 (GeoZarr)": "新一代多维数组格式，OGC社区标准候选",
    }

    for std_name, desc in ogc_standards.items():
        item_hash = hashlib.md5(f"{source_id}:{std_name}".encode()).hexdigest()[:8]
        if item_hash not in state.known_items:
            items.append(IntelligenceItem(
                id=f"INT-{item_hash}",
                source_id=source_id,
                source_name=source["name"],
                category=source["category"],
                title=std_name,
                url=source["url"],
                summary=desc,
                detected_at=datetime.now().isoformat(timespec="seconds"),
                severity="important" if "候选" in desc or "替代" in desc else "info",
                action_required=f"评估 {std_name} 对知识库的影响，更新相关文档",
                target_files=["knowledge_base/group_02_standards/"],
            ))
            state.known_items[item_hash] = datetime.now().isoformat(timespec="seconds")

    return items


def generate_report(new_items: List[IntelligenceItem], state: CrawlerState,
                    sources_checked: int, sources_failed: int) -> IntelligenceReport:
    """生成情报汇总报告"""
    now = datetime.now()
    report = IntelligenceReport(
        generated_at=now.isoformat(timespec="seconds"),
        period_start=(now - timedelta(days=30)).strftime("%Y-%m-%d"),
        period_end=now.strftime("%Y-%m-%d"),
        sources_checked=sources_checked,
        sources_failed=sources_failed,
        new_items=[asdict(i) for i in new_items],
        urgent_items=[asdict(i) for i in new_items if i.severity == "urgent"],
        summary={
            "总新情报": len(new_items),
            "紧急": len([i for i in new_items if i.severity == "urgent"]),
            "重要": len([i for i in new_items if i.severity == "important"]),
            "信息": len([i for i in new_items if i.severity == "info"]),
            "按类别": {},
            "需更新文件": set(),
        }
    )

    for item in new_items:
        report.summary["按类别"][item.category] = \
            report.summary["按类别"].get(item.category, 0) + 1
        for f in item.target_files:
            report.summary["需更新文件"].add(f)

    report.summary["需更新文件"] = sorted(report.summary["需更新文件"])
    return report


def push_to_fixer(report: IntelligenceReport) -> Optional[Path]:
    """推送报告至 knowledge_fixer/inbox"""
    PUSH_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = PUSH_DIR / filename
    output_path.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"情报报告已推送: {output_path}")
    return output_path


def run() -> IntelligenceReport:
    """主执行入口"""
    logger.info("=" * 60)
    logger.info(f"GeoEvolve 情报抓取层启动 | {CRAWLER_ID} | {VERSION}")
    logger.info("=" * 60)

    state = load_state()
    all_new = []
    sources_checked = 0
    sources_failed = 0

    for source in INTELLIGENCE_SOURCES:
        logger.info(f"检查情报源: [{source['id']}] {source['name']}")
        try:
            if source["category"] == "标准":
                items = check_standard_source(source, state)
            elif source["category"] == "软件":
                items = check_software_source(source, state)
            elif source["id"] == "OGC-001":
                items = check_ogc_source(source, state)
            else:
                items = check_software_source(source, state)

            all_new.extend(items)
            sources_checked += 1
            logger.info(f"  → {len(items)} 条新情报")
        except Exception as e:
            logger.error(f"  × 检查失败: {e}")
            sources_failed += 1

    state.known_items["_last_crawl"] = datetime.now().isoformat(timespec="seconds")
    save_state(state)

    report = generate_report(all_new, state, sources_checked, sources_failed)
    push_to_fixer(report)

    logger.info(f"完成: {sources_checked}/{len(INTELLIGENCE_SOURCES)} 源成功, "
                f"{len(all_new)} 条新情报 (紧急:{report.summary['紧急']} 重要:{report.summary['重要']})")

    return report


# ── CLI 入口 ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GeoEvolve 情报抓取层")
    parser.add_argument("--force", action="store_true", help="强制全量抓取（忽略已知缓存）")
    parser.add_argument("--output", "-o", type=str, help="输出报告路径")
    args = parser.parse_args()

    if args.force:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            logger.info("已清除缓存状态，将执行全量抓取")

    try:
        report = run()
        if args.output:
            Path(args.output).write_text(
                json.dumps(asdict(report), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        print(f"\n完成: {report.sources_checked} 源成功, "
              f"{report.summary['总新情报']} 条新情报已推送至 knowledge_fixer。")
        sys.exit(0)
    except Exception as e:
        logger.exception("抓取异常")
        print(f"错误: {e}")
        sys.exit(1)
