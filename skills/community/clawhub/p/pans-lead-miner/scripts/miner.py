#!/usr/bin/env python3
"""
pans-lead-miner — AI算力销售线索挖掘器

输入行业关键词，自动搜索筛选潜在客户，识别算力需求信号。
通过 SearXNG 聚合多数据源，按融资和算力需求排序。
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
import urllib.error
import re
from datetime import datetime
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEARXNG_URL = "http://127.0.0.1:8888/search"

DEFAULT_CATEGORIES = ["crunchbase", "github", "linkedin", "news"]

SIGNAL_KEYWORDS = [
    # 融资信号
    "funding", "raised", "series a", "series b", "series c", "seed round",
    "valuation", "invested", "financing",
    # 算力需求信号
    "gpu", "training", "inference", "data center", "datacenter",
    "compute", "cloud infrastructure", "hpc", "supercomputer",
    "model training", "deep learning", "large language model", "llm",
    "foundation model", "ai chip", "accelerator",
    # 招聘信号
    "hiring gpu", "ml engineer", "infra engineer", "cuda",
]

STAGE_ORDER = {
    "seed": 1,
    "pre-seed": 0,
    "series-a": 2,
    "series b": 3,
    "series-b": 3,
    "series c": 4,
    "series-c": 4,
    "later": 5,
    "ipo": 6,
}

REGION_MAP = {
    "us": ["united states", "usa", "us", "silicon valley", "san francisco", "new york", "seattle"],
    "cn": ["china", "chinese", "beijing", "shanghai", "shenzhen", "hangzhou", "中国", "北京", "上海", "深圳"],
    "eu": ["europe", "european", "london", "berlin", "paris", "amsterdam", "uk", "germany", "france"],
    "global": [],
}

SIZE_MAP = {
    "startup": (1, 50),
    "small": (51, 200),
    "medium": (201, 1000),
    "large": (1001, 10000),
    "enterprise": (10001, None),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_get(url: str, timeout: int = 15) -> dict | None:
    """HTTP GET with JSON response, returns None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "pans-lead-miner/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as exc:
        print(f"[warn] SearXNG request failed: {exc}", file=sys.stderr)
        return None


def _extract_company(title: str) -> str:
    """Try to extract company name from a search result title."""
    # Common patterns: "Company raises $X" / "Company — Crunchbase" / "Company | ..."
    for sep in [" — ", " | ", " - "]:
        if sep in title:
            return title.split(sep)[0].strip()
    return title.strip()


def _extract_stage(text: str) -> str | None:
    """Extract funding stage from text."""
    text_lower = text.lower()
    for stage in ["series c", "series b", "series a", "seed", "pre-seed"]:
        if stage in text_lower:
            return stage
    if "ipo" in text_lower:
        return "ipo"
    return None


def _extract_amount(text: str) -> str | None:
    """Extract funding amount from text."""
    patterns = [
        r"\$[\d.]+\s*[BMK]\b",       # $100M, $1.5B
        r"\$[\d,]+(?:\.\d+)?\s*(?:million|billion)",  # $100 million
        r"[\d.]+\s*(?:million|billion)\s*(?:USD|dollars?)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return None


def _compute_signal_score(text: str) -> int:
    """Compute a heuristic signal score (0-100) based on keyword presence."""
    text_lower = text.lower()
    score = 0
    for kw in SIGNAL_KEYWORDS:
        if kw in text_lower:
            score += 5
    return min(score, 100)


def _infer_region(text: str) -> str:
    """Infer region from text content."""
    text_lower = text.lower()
    for region, keywords in REGION_MAP.items():
        if region == "global":
            continue
        for kw in keywords:
            if kw in text_lower:
                return region.upper()
    return "GLOBAL"


def _matches_region(text: str, region: str) -> bool:
    if region == "global":
        return True
    text_lower = text.lower()
    for kw in REGION_MAP.get(region, []):
        if kw in text_lower:
            return True
    return False


def _matches_stage(stage: str | None, filter_stage: str) -> bool:
    if filter_stage == "all":
        return True
    if stage is None:
        return False
    return stage.lower().replace(" ", "-") == filter_stage.lower().replace(" ", "-")


# ---------------------------------------------------------------------------
# Search logic
# ---------------------------------------------------------------------------

def search_searxng(keyword: str, source: str, region: str, limit: int) -> list[dict]:
    """Search via local SearXNG instance and return parsed results."""
    results = []

    # Build query categories
    categories = [source] if source != "all" else DEFAULT_CATEGORIES

    for cat in categories:
        params = {
            "q": keyword,
            "format": "json",
            "categories": cat,
        }
        if region and region != "global":
            params["language"] = region

        url = f"{SEARXNG_URL}?{urllib.parse.urlencode(params)}"
        data = _safe_get(url)
        if not data:
            continue

        for item in data.get("results", []):
            combined_text = f"{item.get('title', '')} {item.get('content', '')}"
            results.append({
                "company": _extract_company(item.get("title", "Unknown")),
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "source": cat,
                "stage": _extract_stage(combined_text),
                "amount": _extract_amount(combined_text),
                "signal_score": _compute_signal_score(combined_text),
                "region": _infer_region(combined_text),
            })

    return results


def generate_demo_leads(industry: str, region: str, size: str, limit: int) -> list[dict]:
    """Generate demo/sample leads when SearXNG is unavailable.

    These are illustrative companies based on the search criteria,
    designed to demonstrate the tool's output format and scoring logic.
    """
    demo_pool = [
        {
            "company": "NeuralScale AI",
            "stage": "series-b",
            "amount": "$120M",
            "signal_score": 85,
            "region": "US",
            "description": "Building distributed training platform for LLMs; hiring GPU infra engineers.",
        },
        {
            "company": "DeepCompute",
            "stage": "series-a",
            "amount": "$45M",
            "signal_score": 78,
            "region": "US",
            "description": "Cloud GPU marketplace for AI startups; recently expanded to 8 data centers.",
        },
        {
            "company": "InferEdge",
            "stage": "seed",
            "amount": "$8M",
            "signal_score": 65,
            "region": "US",
            "description": "Edge inference optimization; hiring CUDA kernel engineers.",
        },
        {
            "company": "智算科技",
            "stage": "series-a",
            "amount": "3亿元",
            "signal_score": 72,
            "region": "CN",
            "description": "国产AI算力调度平台；正在招聘GPU集群运维工程师。",
        },
        {
            "company": "ModelForge",
            "stage": "series-b",
            "amount": "$200M",
            "signal_score": 90,
            "region": "US",
            "description": "Foundation model training platform; 2000+ GPU cluster expansion announced.",
        },
        {
            "company": "QuantumBit Labs",
            "stage": "seed",
            "amount": "$5M",
            "signal_score": 55,
            "region": "EU",
            "description": "Research lab focusing on quantum-classical hybrid AI; seeking HPC partnerships.",
        },
        {
            "company": "CloudInfer",
            "stage": "series-a",
            "amount": "$60M",
            "signal_score": 75,
            "region": "US",
            "description": "Serverless GPU inference platform; scaling to 10K+ GPUs.",
        },
        {
            "company": "百川智能",
            "stage": "series-b",
            "amount": "50亿元",
            "signal_score": 88,
            "region": "CN",
            "description": "大模型厂商；采购数千张A100/H800用于模型训练。",
        },
        {
            "company": "TitanML",
            "stage": "seed",
            "amount": "$12M",
            "signal_score": 60,
            "region": "EU",
            "description": "LLM compression and deployment startup; hiring ML infra engineers.",
        },
        {
            "company": "AeroCompute",
            "stage": "later",
            "amount": "$350M",
            "signal_score": 70,
            "region": "US",
            "description": "AI cloud provider with global GPU fleet; expanding APAC data centers.",
        },
        {
            "company": "推理引擎科技",
            "stage": "series-a",
            "amount": "2亿元",
            "signal_score": 68,
            "region": "CN",
            "description": "大模型推理加速；自研推理框架，招聘CUDA工程师。",
        },
        {
            "company": "DeepStack AI",
            "stage": "series-c",
            "amount": "$500M",
            "signal_score": 82,
            "region": "US",
            "description": "Enterprise AI platform; deploying 5000+ GPU training cluster.",
        },
        {
            "company": "NeuralPath",
            "stage": "seed",
            "amount": "$6M",
            "signal_score": 50,
            "region": "EU",
            "description": "AutoML for edge devices; exploring cloud GPU partnerships.",
        },
        {
            "company": "银河算力",
            "stage": "series-b",
            "amount": "10亿元",
            "signal_score": 80,
            "region": "CN",
            "description": "AI算力云服务商；新建智算中心，需要大量GPU服务器。",
        },
        {
            "company": "FusionAI",
            "stage": "series-a",
            "amount": "$80M",
            "signal_score": 76,
            "region": "US",
            "description": "Multi-modal model training; hiring distributed systems engineers.",
        },
        {
            "company": "ScaleHPC",
            "stage": "later",
            "amount": "$250M",
            "signal_score": 73,
            "region": "US",
            "description": "HPC-as-a-Service for AI workloads; GPU fleet management platform.",
        },
        {
            "company": "CogniLab",
            "stage": "seed",
            "amount": "$4M",
            "signal_score": 45,
            "region": "EU",
            "description": "AI research lab; early-stage model training requiring GPU access.",
        },
        {
            "company": "月之暗面",
            "stage": "series-b",
            "amount": "20亿元",
            "signal_score": 92,
            "region": "CN",
            "description": "Kimi大模型开发商；大量采购GPU用于长上下文模型训练。",
        },
        {
            "company": "VectorScale",
            "stage": "series-a",
            "amount": "$30M",
            "signal_score": 62,
            "region": "US",
            "description": "Vector database for AI applications; expanding GPU-accelerated search.",
        },
        {
            "company": "推理云科技",
            "stage": "series-a",
            "amount": "5亿元",
            "signal_score": 77,
            "region": "CN",
            "description": "大模型推理云平台；需要大量推理GPU资源。",
        },
    ]

    # Filter by region
    filtered = demo_pool
    if region and region != "global":
        region_upper = region.upper()
        filtered = [d for d in filtered if d["region"] == region_upper]

    # Filter by stage (if industry keyword hints at stage)
    # For demo, we just use signal_score to sort
    filtered.sort(key=lambda x: x["signal_score"], reverse=True)

    # Limit
    filtered = filtered[:limit]

    # Format to match search results
    results = []
    for d in filtered:
        results.append({
            "company": d["company"],
            "title": f"{d['company']} — {d.get('stage', 'N/A').upper()} {d.get('amount', '')}",
            "url": "",
            "snippet": d["description"],
            "source": "demo",
            "stage": d.get("stage"),
            "amount": d.get("amount"),
            "signal_score": d["signal_score"],
            "region": d["region"],
        })

    return results


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_markdown(leads: list[dict]) -> str:
    """Format leads as a Markdown table."""
    if not leads:
        return "No leads found matching criteria.\n"

    lines = [
        f"# 🔍 Lead Mining Results",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Total leads:** {len(leads)}",
        f"",
        f"| # | Company | Stage | Amount | Region | Signal | Source |",
        f"|---|---------|-------|--------|--------|--------|--------|",
    ]

    for i, lead in enumerate(leads, 1):
        stage = lead.get("stage") or "N/A"
        amount = lead.get("amount") or "-"
        region = lead.get("region", "GLOBAL")
        score = lead.get("signal_score", 0)
        source = lead.get("source", "N/A")
        lines.append(
            f"| {i} | {lead['company']} | {stage} | {amount} | {region} | {score} | {source} |"
        )

    lines.append("")
    lines.append("## Details")
    lines.append("")

    for i, lead in enumerate(leads, 1):
        lines.append(f"### {i}. {lead['company']}")
        lines.append(f"- **Stage:** {lead.get('stage') or 'N/A'}")
        lines.append(f"- **Amount:** {lead.get('amount') or 'N/A'}")
        lines.append(f"- **Region:** {lead.get('region', 'GLOBAL')}")
        lines.append(f"- **Signal Score:** {lead.get('signal_score', 0)}/100")
        lines.append(f"- **Source:** {lead.get('source', 'N/A')}")
        if lead.get("url"):
            lines.append(f"- **URL:** {lead['url']}")
        if lead.get("snippet"):
            lines.append(f"- **Snippet:** {lead['snippet']}")
        lines.append("")

    return "\n".join(lines)


def format_json(leads: list[dict]) -> str:
    """Format leads as JSON."""
    return json.dumps(leads, indent=2, ensure_ascii=False)


def format_csv(leads: list[dict]) -> str:
    """Format leads as CSV."""
    if not leads:
        return ""

    import io
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["company", "stage", "amount", "region", "signal_score", "source", "url", "snippet"],
    )
    writer.writeheader()
    for lead in leads:
        writer.writerow({
            "company": lead.get("company", ""),
            "stage": lead.get("stage", ""),
            "amount": lead.get("amount", ""),
            "region": lead.get("region", ""),
            "signal_score": lead.get("signal_score", 0),
            "source": lead.get("source", ""),
            "url": lead.get("url", ""),
            "snippet": lead.get("snippet", ""),
        })
    return output.getvalue()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="miner.py",
        description="AI算力销售线索挖掘器 — 搜索筛选潜在客户，识别算力需求信号",
        epilog="示例: python3 miner.py --industry 'AI infrastructure' --region us --limit 10",
    )

    parser.add_argument(
        "--industry", "-k",
        required=True,
        help="搜索关键词/行业（如 'AI infrastructure', 'LLM startup'）",
    )
    parser.add_argument(
        "--region",
        default="global",
        choices=["us", "cn", "eu", "global"],
        help="目标地区 (default: global)",
    )
    parser.add_argument(
        "--size",
        default=None,
        choices=["startup", "small", "medium", "large", "enterprise"],
        help="公司规模筛选",
    )
    parser.add_argument(
        "--source",
        default="all",
        choices=["crunchbase", "github", "linkedin", "news", "all"],
        help="数据源 (default: all)",
    )
    parser.add_argument(
        "--stage",
        default="all",
        choices=["seed", "series-a", "series-b", "later", "all"],
        help="融资阶段筛选 (default: all)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        default="markdown",
        choices=["json", "markdown", "csv"],
        help="输出格式 (default: markdown)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="最大结果数 (default: 20)",
    )
    parser.add_argument(
        "--export",
        default=None,
        help="导出文件路径（自动根据扩展名选择格式: .json/.csv/.md）",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="使用 demo 模式（无需 SearXNG，返回示例数据）",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    keyword = args.industry
    region = args.region
    source = args.source
    stage = args.stage
    limit = args.limit

    # Try SearXNG first, fall back to demo data
    leads: list[dict] = []

    # Fetch a larger pool so post-filters still have enough results
    fetch_limit = max(limit * 5, 50)

    if not args.demo:
        print(f"🔍 Searching for '{keyword}' via SearXNG...", file=sys.stderr)
        leads = search_searxng(keyword, source, region, fetch_limit)

        if not leads:
            print("⚠️  SearXNG unavailable, using demo data.", file=sys.stderr)
            leads = generate_demo_leads(keyword, region, args.size, fetch_limit)
    else:
        print("📋 Demo mode enabled.", file=sys.stderr)
        leads = generate_demo_leads(keyword, region, args.size, fetch_limit)

    # Filter by region — check both text content and explicit region field
    if region != "global":
        region_upper = region.upper()
        leads = [
            l for l in leads
            if l.get("region", "").upper() == region_upper
            or _matches_region(
                f"{l.get('snippet', '')} {l.get('title', '')}", region
            )
        ]

    # Filter by stage
    if stage != "all":
        leads = [l for l in leads if _matches_stage(l.get("stage"), stage)]

    # Sort by signal score descending
    leads.sort(key=lambda x: x.get("signal_score", 0), reverse=True)

    # Apply limit
    leads = leads[:limit]

    # Determine output format
    output_format = args.output_format

    # If --export is given, infer format from extension
    if args.export:
        ext = args.export.rsplit(".", 1)[-1].lower() if "." in args.export else ""
        if ext == "json":
            output_format = "json"
        elif ext == "csv":
            output_format = "csv"
        elif ext in ("md", "markdown"):
            output_format = "markdown"
        # else keep --format value

    # Format output
    if output_format == "json":
        output = format_json(leads)
    elif output_format == "csv":
        output = format_csv(leads)
    else:
        output = format_markdown(leads)

    # Write to file or stdout
    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Exported {len(leads)} leads to {args.export}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
