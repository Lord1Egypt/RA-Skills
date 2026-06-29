# GxpCode Skill — Parser 公共工具
import re
import time


def _parse_body(body: str, date_mode: str) -> list:
    """解析 innerText，按日期模式提取 title + date"""
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    entries = []

    if date_mode == "行模式":
        _parse_block_mode(lines, entries)
    elif date_mode == "括号内":
        _parse_bracket_mode(lines, entries)

    return entries


def _parse_block_mode(lines: list, entries: list):
    """行模式: 日期和日可能在同一行（2026.06 01）或跨行"""
    i = 0
    while i < len(lines):
        # 标准格式: 2026.06 01 或 (2026-06-01)
        m = re.match(r"^(?:\d{4}\.\d{2} \d{2}|\(\d{4}-\d{2}-\d{2}\))$", lines[i])
        if m and i + 1 < len(lines):
            entries.append({
                "date": lines[i].strip("()").replace(" ", "-"),
                "title": lines[i + 1].replace(">", "").strip(),
            })
            i += 2
        else:
            i += 1


def _parse_bracket_mode(lines: list, entries: list):
    """括号内模式: 标题 (YYYY-MM-DD)"""
    for line in lines:
        m = re.search(r"(.+) \((\d{4}-\d{2}-\d{2})\)$", line)
        if m:
            entries.append({"title": m.group(1), "date": m.group(2)})


def _pair_links(entries: list, page, link_key: str, text_match_mode: bool = False) -> list:
    """把标题和链接配对。

    当 text_match_mode=True 时，link_key 为链接的固定文本（如【查看详情】）。
    当 text_match_mode=False 时，link_key 为 title（标题本身即链接）。
    """
    if text_match_mode:
        link_list = []
        for a in page.query_selector_all("a"):
            if a.inner_text().strip() == link_key:
                link_list.append(a.evaluate("el => el.href"))
        for i, e in enumerate(entries):
            e["url"] = link_list[i] if i < len(link_list) else ""
    else:
        all_links = {}
        for a in page.query_selector_all("a[href]"):
            text = a.inner_text().strip()
            url = a.evaluate("el => el.href")
            if len(text) >= 10 and url:
                all_links[text] = url
        for e in entries:
            t = e["title"]
            if t in all_links:
                e["url"] = all_links[t]
            else:
                best = ""
                for k, v in all_links.items():
                    if len(k) >= 15 and (k[:20] in t or t[:20] in k):
                        best = v
                        break
                e["url"] = best

    return entries


def _parse_data_order(page) -> list:
    """data-order 模式: PIC/S publications 表格"""
    entries = []
    for td in page.query_selector_all("td[data-order]"):
        do = td.get_attribute("data-order") or ""
        m = re.match(r"(\d{4}-\d{2}-\d{2})", do)
        if not m:
            continue
        date = m.group(1)
        a = td.query_selector("a[href]")
        if not a:
            continue
        title = a.inner_text().strip()
        url = a.evaluate("el => el.href")
        if not title or not url:
            continue
        entries.append({"title": title, "url": url, "date": date})
    return entries


def _parse_onclick(page, source_url: str) -> list:
    """onclick 模式: JSCDI JS 渲染列表"""
    from urllib.parse import urljoin

    entries = []
    for a_el in page.query_selector_all("a"):
        onclick = a_el.get_attribute("onclick") or ""
        if "openArticle" not in onclick and "SiteMain" not in onclick:
            continue

        m = re.search(r"['\"](\d+)['\"]\s*,\s*['\"]([^'\"]+)['\"]", onclick)
        if not m:
            m = re.search(r"openArticle\s*\((\d+),\s*['\"]([^'\"]+)['\"]", onclick)
        if not m:
            continue
        art_type = m.group(1)
        art_url = m.group(2)

        if art_type == "3" or art_url.startswith("http"):
            url = art_url
        else:
            prefix = None
            for seg in ["/hczx/web", "/web"]:
                idx = source_url.find(seg)
                if idx > 0:
                    prefix = source_url[:idx + len(seg)]
                    break
            if prefix:
                url = prefix + art_url
            else:
                url = urljoin(source_url, art_url)

        title = a_el.inner_text().strip() if a_el else ""
        if not title or not url:
            continue
        entries.append({"title": title, "url": url, "date": ""})
    return entries
