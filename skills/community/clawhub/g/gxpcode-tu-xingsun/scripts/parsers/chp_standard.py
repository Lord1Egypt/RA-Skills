# GxpCode Skill — Parser: CHP 药典委员会标准公示（Quasar SPA + hash 路由）
# 适用: www.chp.org.cn/#/business/standard
# 5 个 tab: 中药 / 化学药 / 生物制品 / 通则辅料包材 / 中药配方颗粒
# 通过 extract.tab 指定要抓取的 tab，一次调用只抓一个 tab 的当前页
# DOM: <TABLE class="q-mt-md"> → <TR><TD>分类</TD><TD><A>标题</A></TD><TD>处室</TD><TD>公示时间</TD><TD>截止时间</TD><TD>状态</TD></TR>
# Tab: <DIV class="item-cont"><SPAN>tab名</SPAN></DIV>

import re
import time
from urllib.parse import urljoin

BASE_URL = "https://www.chp.org.cn"


def parse(page, source_name: str, jurisdiction: str, extract: dict = None):
    tab_name = extract.get("tab", "") if extract else ""
    if not tab_name:
        return []

    # 等待 SPA 渲染
    time.sleep(2)
    try:
        page.wait_for_selector("table.q-mt-md tr", timeout=20000)
    except Exception:
        pass

    # 点击目标 tab（DIV.item-cont 包含匹配文本）
    clicked = False
    for el in page.query_selector_all("div.item-cont"):
        text = el.inner_text().strip()
        if text == tab_name:
            try:
                el.click()
                time.sleep(2)
                clicked = True
            except Exception:
                pass
            break

    if not clicked:
        # fallback: 尝试 span/div 中精确文本匹配
        for el in page.query_selector_all("span, div"):
            text = el.inner_text().strip() if el.inner_text() else ""
            if text == tab_name:
                try:
                    el.click()
                    time.sleep(2)
                    clicked = True
                except Exception:
                    pass
                break

    # 解析表格行（跳过 header 和空行）
    entries = []
    rows = page.query_selector_all("table.q-mt-md tr")
    for row in rows:
        cells = row.query_selector_all("td")
        if len(cells) < 4:
            continue

        # 列: TD[0]=分类 | TD[1]=<A>标题 | TD[2]=处室 | TD[3]=公示时间 | TD[4]=截止时间 | TD[5]=状态
        cat = cells[0].inner_text().strip()
        title_cell = cells[1]
        date_text = cells[3].inner_text().strip()

        a_el = title_cell.query_selector("a")
        title_text = a_el.inner_text().strip() if a_el else title_cell.inner_text().strip()
        href = a_el.get_attribute("href") if a_el else ""

        # URL 可能是 hash 路由的相对链接
        if href:
            if href.startswith("/") or href.startswith("#"):
                url = urljoin(BASE_URL, href)
            else:
                url = href
        else:
            url = f"{BASE_URL}/#/business/standard"

        if not title_text:
            continue

        # 过滤：只保留当前 tab 分类的条目
        if tab_name not in cat:
            continue

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
        date = date_match.group(1) if date_match else date_text

        entries.append({
            "title": title_text,
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
