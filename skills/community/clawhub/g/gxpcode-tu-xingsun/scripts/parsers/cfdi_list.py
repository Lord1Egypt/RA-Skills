# GxpCode Skill — Parser: CFDI 通知公告列表页
# 适用: www.cfdi.org.cn 所有模块页面（module=A001, A002 等）
# 特征: <ul><li><a.title> 内含 <p.content>标题 + <p.datatime>日期
# 分页: form POST + gotopage(N) JS 函数
# 渲染: 首页服务端渲染，翻页需 JS

import re


def parse(page, source_name: str, jurisdiction: str) -> list:
    """
    从 CFDI 列表页提取条目。
    DOM 结构:
      <ul>
        <li>
          <a class="title" href="...">
            <p class="content">标题文本</p>
            <p class="datatime">YYYY-MM-DD</p>
          </a>
        </li>
      </ul>
    """
    entries = []
    for a_el in page.query_selector_all("a.title"):
        url = a_el.evaluate("el => el.href")
        content_el = a_el.query_selector("p.content")
        date_el = a_el.query_selector("p.datatime")
        title = content_el.inner_text().strip() if content_el else ""
        date = date_el.inner_text().strip() if date_el else ""

        if not title or not url:
            continue

        entries.append({
            "title": title,
            "url": url,
            "date": date,
        })

    return _build_items(entries, source_name, jurisdiction)


def _build_items(entries: list, source_name: str, jurisdiction: str) -> list:
    items = []
    for e in entries:
        items.append({
            "source": source_name,
            "jurisdiction": jurisdiction,
            "title": e["title"],
            "url": e["url"],
            "date": e.get("date", ""),
            "summary": "",
            "source_type": "web",
            "confidence": "high",
        })
    return items
