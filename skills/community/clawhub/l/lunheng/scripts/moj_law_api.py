#!/usr/bin/env python3
"""
国家行政法规库 (xzfg.moj.gov.cn) 客户端
司法部维护，行政法规最权威来源（现行有效 612 部）

无 REST API，通过 HTTP 抓取 HTML 页面解析。
"""

import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from dataclasses import dataclass, field
from typing import Optional

BASE_URL = "https://xzfg.moj.gov.cn"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


@dataclass
class MojLaw:
    """行政法规元数据"""
    law_id: str = ""
    title: str = ""
    publish_date: str = ""      # 公布日期
    implement_date: str = ""    # 施行日期
    status: str = "现行有效"     # 行政法规库仅收录现行有效
    detail_url: str = ""
    download_word: str = ""
    download_pdf: str = ""


def _fetch(url: str, timeout: int = 15) -> str:
    """发起 HTTP GET 请求，返回响应文本"""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            # 尝试多种编码
            for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
                try:
                    return data.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return data.decode("utf-8", errors="replace")
    except Exception as e:
        return ""


def search_by_title(keyword: str, page: int = 1) -> list[MojLaw]:
    """
    标题检索行政法规。
    
    Args:
        keyword: 搜索关键词（法规名称片段）
        page: 页码（从1开始）
    
    Returns:
        list[MojLaw] — 匹配的法规列表
    """
    encoded = urllib.parse.quote(keyword)
    # QueryAll 格式: 关键词ZVING1（1=标题检索，2=正文检索）
    query_all = urllib.parse.quote(f"{keyword}ZVING1")
    url = f"{BASE_URL}/SearchTitleFront?SiteID=122&Query={encoded}&Type=1&QueryAll={query_all}"
    html = _fetch(url)
    if not html:
        return []
    return _parse_search_results(html)


def search_by_content(keyword: str, page: int = 1) -> list[MojLaw]:
    """
    正文检索行政法规。
    
    Args:
        keyword: 搜索关键词
        page: 页码
    
    Returns:
        list[MojLaw] — 匹配的法规列表
    """
    encoded = urllib.parse.quote(keyword)
    query_all = urllib.parse.quote(f"{keyword}ZVING2")
    url = f"{BASE_URL}/SearchFront?SiteID=122&Query={encoded}&Type=2&QueryAll={query_all}"
    html = _fetch(url)
    if not html:
        return []
    return _parse_search_results(html)


def advanced_search(
    title: str = "",
    content: str = "",
    publish_file_number: str = "",
    publish_time_start: str = "",
    publish_time_end: str = "",
    implement_date_start: str = "",
    implement_date_end: str = "",
    page: int = 1,
) -> list[MojLaw]:
    """
    高级检索行政法规。
    
    Args:
        title: 标题
        content: 正文关键词
        publish_file_number: 公布文号
        publish_time_start: 公布日期起 (YYYY-MM-DD)
        publish_time_end: 公布日期止
        implement_date_start: 施行日期起
        implement_date_end: 施行日期止
        page: 页码
    
    Returns:
        list[MojLaw]
    """
    params = {
        "title": title,
        "content": content,
        "timeliness": "1",  # 现行有效
        "publishFileNumber": publish_file_number,
        "publishTimeStart": publish_time_start,
        "publishTimeEnd": publish_time_end,
        "implementDateStart": implement_date_start,
        "implementDateEnd": implement_date_end,
        "pageNo": str(page),
    }
    # 过滤空值
    params = {k: v for k, v in params.items() if v}
    encoded = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/SearchAdvancedFront?{encoded}"
    html = _fetch(url)
    if not html:
        return []
    return _parse_search_results(html)


def get_detail(law_id: str) -> Optional[dict]:
    """
    获取法规详情页（含正文和历史沿革）。
    
    Args:
        law_id: 法规ID（数字字符串）
    
    Returns:
        dict: {"title", "history": [{"date", "law_id", "title"}], "html_body"}
        None if not found
    """
    url = f"{BASE_URL}/front/law/detail?LawID={law_id}"
    html = _fetch(url)
    if not html:
        return None

    result = {"title": "", "history": [], "html_body": ""}

    # 提取标题
    m = re.search(r'<div class="text-title">(.*?)</div>', html, re.DOTALL)
    if m:
        result["title"] = _clean_html(m.group(1))

    # 提取历史沿革
    history_pattern = re.compile(
        r'<span class="month-title[^"]*"[^>]*>(\d{4}-\d{2}-\d{2})</span>'
    )
    record_pattern = re.compile(
        r'<div class="incident-record"[^>]*data-time="(\d{4}-\d{2}-\d{2})">\s*'
        r'<a[^>]*href="[^"]*LawID=(\d+)"[^>]*>(.*?)</a>'
    )
    dates = history_pattern.findall(html)
    records = record_pattern.findall(html)
    for date_str, law_id_val, title in records:
        result["history"].append({
            "date": date_str,
            "law_id": law_id_val,
            "title": _clean_html(title),
        })

    # 提取正文 HTML
    m = re.search(r'<div class="law-chapter">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
    if m:
        result["html_body"] = m.group(1)

    return result


def get_plain_text(law_id: str) -> str:
    """
    获取法规纯文本正文（去除HTML标签）。
    
    Args:
        law_id: 法规ID
    
    Returns:
        纯文本正文
    """
    detail = get_detail(law_id)
    if not detail or not detail["html_body"]:
        return ""
    return _clean_html(detail["html_body"])


def verify_law(name: str) -> dict:
    """
    验证行政法规名称是否存在于行政法规库。
    用于 law_checker.py Layer 集成。
    
    Args:
        name: 法规名称
    
    Returns:
        {
            "found": bool,
            "law_id": str,
            "title": str,
            "status": str,
            "publish_date": str,
            "implement_date": str,
            "source": "moj",
        }
        未找到返回空 dict
    """
    results = search_by_title(name)
    if not results:
        return {}

    # 精确匹配优先
    for law in results:
        if law.title == name or law.title.replace(" ", "") == name.replace(" ", ""):
            return {
                "found": True,
                "law_id": law.law_id,
                "title": law.title,
                "status": law.status,
                "publish_date": law.publish_date,
                "implement_date": law.implement_date,
                "source": "moj",
            }

    # 模糊匹配（标题包含关键词）
    for law in results:
        if name in law.title or law.title in name:
            return {
                "found": True,
                "law_id": law.law_id,
                "title": law.title,
                "status": law.status,
                "publish_date": law.publish_date,
                "implement_date": law.implement_date,
                "source": "moj",
            }

    return {}


# ─── HTML 解析工具 ──────────────────────────────────────

def _parse_search_results(html: str) -> list[MojLaw]:
    """从搜索结果页 HTML 中提取法规列表"""
    laws = []

    # 提取所有 LawID
    law_ids = re.findall(r'LawID=(\d+)', html)
    law_ids = list(dict.fromkeys(law_ids))  # 去重保序

    # 按 list-item 分块解析
    items = re.split(r'<li class="list-item">', html)
    for item in items[1:]:  # 跳过第一个（list-item 之前的内容）
        law = MojLaw()

        # 提取 LawID
        m = re.search(r'LawID=(\d+)', item)
        if m:
            law.law_id = m.group(1)

        # 提取标题
        m = re.search(r'<div class="title">\s*<a[^>]*>(.*?)</a>', item, re.DOTALL)
        if m:
            law.title = _clean_html(m.group(1))

        # 提取公布日期
        m = re.search(r'<li class="publish-date">\s*(.*?)\s*</li>', item, re.DOTALL)
        if m:
            date_text = _clean_html(m.group(1))
            # 提取 YYYY-MM-DD 格式
            dm = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if dm:
                law.publish_date = dm.group(1)

        # 提取施行日期
        m = re.search(r'<li class="implement-date">\s*(.*?)\s*</li>', item, re.DOTALL)
        if m:
            date_text = _clean_html(m.group(1))
            dm = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if dm:
                law.implement_date = dm.group(1)

        # 构造 URL
        if law.law_id:
            law.detail_url = f"{BASE_URL}/front/law/detail?LawID={law.law_id}"
            law.download_word = f"{BASE_URL}/law/download?LawID={law.law_id}"
            law.download_pdf = f"{BASE_URL}/law/download?LawID={law.law_id}&type=pdf"

        if law.law_id and law.title:
            laws.append(law)

    return laws


def _clean_html(text: str) -> str:
    """去除 HTML 标签，保留纯文本"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&#\d+;', '', text)
    return text.strip()


# ─── CLI 测试 ──────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 moj_law_api.py search <关键词>       # 标题检索")
        print("  python3 moj_law_api.py content <关键词>      # 正文检索")
        print("  python3 moj_law_api.py detail <LawID>         # 获取详情")
        print("  python3 moj_law_api.py verify <法规名称>      # 验证法规存在性")
        sys.exit(1)

    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "search":
        results = search_by_title(arg)
        print(f"找到 {len(results)} 条结果:")
        for i, law in enumerate(results, 1):
            print(f"  {i}. [{law.law_id}] {law.title}")
            print(f"     公布: {law.publish_date}  施行: {law.implement_date}")

    elif cmd == "content":
        results = search_by_content(arg)
        print(f"找到 {len(results)} 条结果:")
        for i, law in enumerate(results, 1):
            print(f"  {i}. [{law.law_id}] {law.title}")
            print(f"     公布: {law.publish_date}  施行: {law.implement_date}")

    elif cmd == "detail":
        detail = get_detail(arg)
        if detail:
            print(f"标题: {detail['title']}")
            print(f"历史沿革 ({len(detail['history'])} 个版本):")
            for h in detail["history"]:
                print(f"  {h['date']} — {h['title']} (LawID={h['law_id']})")
            if detail["html_body"]:
                text = _clean_html(detail["html_body"])
                print(f"\n正文 ({len(text)} 字):")
                print(text[:500] + "..." if len(text) > 500 else text)
        else:
            print("未找到该法规")

    elif cmd == "verify":
        result = verify_law(arg)
        if result:
            print(f"✅ 找到: {result['title']}")
            print(f"   状态: {result['status']}")
            print(f"   公布: {result['publish_date']}  施行: {result['implement_date']}")
            print(f"   LawID: {result['law_id']}")
        else:
            print(f"❌ 未找到: {arg}")

    else:
        print(f"未知命令: {cmd}")
