#!/usr/bin/env python3
"""
HuggingFace Papers Fetcher
获取 HuggingFace Papers 热门论文

Usage:
    python get_papers.py --period daily          # 今日热门
    python get_papers.py --period weekly         # 本周热门
    python get_papers.py --period monthly        # 本月热门
    python get_papers.py --period daily --date 2026-04-29   # 指定日期
    python get_papers.py --period weekly --limit 10
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional


def get_hf_papers_url(period: str, custom_date: Optional[str] = None) -> str:
    """根据时间范围和可选的自定义日期生成 HuggingFace Papers URL"""
    if custom_date:
        # 使用自定义日期
        if period == "daily":
            return f"https://huggingface.co/papers/date/{custom_date}"
        elif period == "weekly":
            d = datetime.strptime(custom_date, "%Y-%m-%d")
            week_number = d.isocalendar()[1]
            return f"https://huggingface.co/papers/week/{d.strftime('%Y')}-W{week_number:02d}"
        elif period == "monthly":
            d = datetime.strptime(custom_date, "%Y-%m-%d")
            return f"https://huggingface.co/papers/month/{d.strftime('%Y-%m')}"
    
    today = datetime.now()
    if period == "daily":
        return f"https://huggingface.co/papers/date/{today.strftime('%Y-%m-%d')}" 
    elif period == "weekly":
        week_number = today.isocalendar()[1]
        return f"https://huggingface.co/papers/week/{today.strftime('%Y')}-W{week_number:02d}"
    elif period == "monthly":
        return f"https://huggingface.co/papers/month/{today.strftime('%Y-%m')}"
    else:
        return f"https://huggingface.co/papers/date/{today.strftime('%Y-%m-%d')}"


def fetch_html(url: str, timeout: int = 15) -> str:
    """获取 HTML 内容"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise Exception(f"网络错误：无法访问 {url} - {e.reason}")
    except TimeoutError:
        raise Exception(f"请求超时：{timeout}秒内未响应")


def decode_html_entities(html: str) -> str:
    """解码 HTML 实体和转义字符"""
    result = html
    result = result.replace('&quot;', '"')
    result = result.replace('&amp;', '&')
    result = result.replace('\\&quot;', '"')
    result = result.replace('\\n', ' ')
    return result


def parse_papers(html: str, limit: int = 10) -> List[Dict]:
    """解析页面获取论文列表"""
    decoded = decode_html_entities(html)
    papers = []
    seen_ids = set()
    
    # 提取所有 paper id
    id_pattern = r'"id":"(\d{4}\.\d{4,5})","authors"'
    ids = re.findall(id_pattern, decoded)
    
    for pid in ids:
        if pid in seen_ids:
            continue
        seen_ids.add(pid)
        
        # 找到这个 id 的位置
        id_pos = decoded.find(f'"id":"{pid}"')
        if id_pos < 0:
            continue
        
        # 扩大搜索范围以包含所有字段
        search_range = 15000
        search_block = decoded[id_pos:id_pos+search_range]
        
        # 提取 title
        title_match = re.search(r'"title":"(.+?)"', search_block)
        title = title_match.group(1) if title_match else f"arXiv:{pid}"
        
        # 提取 summary
        summary_match = re.search(r'"summary":"(.+?)(?:","|"\})', search_block)
        summary = summary_match.group(1) if summary_match else ""
        
        # 提取 upvotes
        upvotes_match = re.search(r'"upvotes":(\d+)', search_block)
        upvotes = int(upvotes_match.group(1)) if upvotes_match else 0
        
        papers.append({
            "paper_id": pid,
            "title": title,
            "abstract": summary,
            "upvotes": upvotes,
            "url": f"https://huggingface.co/papers/{pid}"
        })
        
        if len(papers) >= limit:
            break
    
    return papers


def get_papers(period: str = "weekly", limit: int = 10, custom_date: Optional[str] = None) -> List[Dict]:
    """获取热门论文列表"""
    url = get_hf_papers_url(period, custom_date)
    html = fetch_html(url)
    return parse_papers(html, limit)


def format_markdown(papers: List[Dict], period: str) -> str:
    """格式化为 Markdown（英文原文）"""
    period_names = {
        "daily": "今日热门",
        "weekly": "本周热门",
        "monthly": "本月热门"
    }
    
    lines = [
        f"# 📄 HuggingFace Papers {period_names.get(period, period)}",
        "",
        f"**获取时间:** {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} (GMT+8)",
        "",
        "---",
        ""
    ]
    
    for i, paper in enumerate(papers, 1):
        fire = " 🔥" if paper["upvotes"] >= 50 else ""
        lines.append(f'{i}. **{paper["title"]}**{fire}')
        lines.append(f'   - 👍 {paper["upvotes"]:,} upvotes')
        if paper.get("abstract"):
            lines.append(f'   - 📝 {paper["abstract"]}')
        lines.append(f'   - 🔗 {paper["url"]}')
        lines.append("")
    
    lines.extend([
        "---",
        "",
        "*由 🤖 生成*"
    ])
    
    return "\n".join(lines)


def format_json(papers: List[Dict]) -> str:
    """格式化为 JSON"""
    return json.dumps(papers, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="获取 HuggingFace Papers 热门论文")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"], default="daily",
                        help="时间范围: daily/weekly/monthly")
    parser.add_argument("--limit", type=int, default=10,
                        help="返回论文数量 (默认: 10)")
    parser.add_argument("--format", choices=["md", "json"], default="md",
                        help="输出格式: md/json")
    parser.add_argument("--output", type=str, default=None,
                        help="输出文件路径 (可选)")
    parser.add_argument("--date", type=str, default=None,
                        help="自定义日期 (YYYY-MM-DD)，覆盖自动计算的日期")
    
    args = parser.parse_args()
    
    try:
        papers = get_papers(args.period, args.limit, args.date)
        
        if args.format == "json":
            output = format_json(papers)
        else:
            output = format_markdown(papers, args.period)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ 已保存到: {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
