# GxpCode Skill — ⑤ 通知：模板驱动 Markdown 报告

import json
import os
import re
import yaml
import markdown
from datetime import datetime
from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(SKILL_DIR, "resources", "templates")


def _load_template(name: str) -> str:
    with open(os.path.join(TEMPLATE_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def _extract_number(title: str) -> str:
    m = re.search(r"(\d{4}年第\d+号)", title)
    return m.group(1) if m else "-"


def _load_s4(gxpcode: str) -> list:
    """读取 S4 数据，按 URL 去重（同一法规多源收录时仅保留首次出现）"""
    s4_dir = os.path.join(gxpcode, "s4")
    seen_urls = set()
    all_items = []
    for fname in sorted(os.listdir(s4_dir)):
        if fname.endswith(".json"):
            with open(os.path.join(s4_dir, fname), "r", encoding="utf-8") as f:
                for item in json.load(f):
                    url = item.get("url", "")
                    if url and url in seen_urls:
                        continue
                    if url:
                        seen_urls.add(url)
                    all_items.append(item)
    return all_items


def _load_config():
    config_path = os.path.join(SKILL_DIR, "resources", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _match_product_type(item: dict, rules: list) -> str:
    text = " ".join([item.get("title", ""), item.get("summary", "")])
    for rule in rules:
        for kw in rule.get("keywords", []):
            if kw in text:
                return rule.get("label", "通用")
    return "通用"


def _render_item(item: dict, index: int, product_types: str) -> str:
    tpl = _load_template("report_item.md")

    att = item.get("attachment", "")
    if att:
        attachment_rows = f"| 附件本地路径 | {att} |"
    else:
        attachment_rows = ""

    src_name = item.get("source", "")
    if src_name.startswith("CDE"):
        authority = "国家药监局药审中心"
    elif src_name.startswith("NMPA"):
        authority = "国家药监局"
    elif src_name.startswith("PIC"):
        authority = "PIC/S"
    else:
        authority = src_name

    return tpl.format(
        index=index,
        title=item.get("title", "无标题"),
        issuing_authority=authority,
        publish_date=item.get("date", "-"),
        document_number=_extract_number(item.get("title", "")),
        topics=", ".join(item.get("tags", [])) or "-",
        product_types=product_types,
        abstract=item.get("summary", "-"),
        url=item.get("url", "-"),
        attachment_rows=attachment_rows,
        source=item.get("source", "-"),
    )


def _build_report(items: list, product_rules: list) -> str:
    today = datetime.now().strftime("%Y-%m-%d")

    high = [d for d in items if d.get("applicability") == "high" and not d.get("needs_manual_review")]
    medium = [d for d in items if d.get("applicability") == "medium" and not d.get("needs_manual_review")]
    low = [d for d in items if d.get("applicability") == "low" and not d.get("needs_manual_review")]
    none = [d for d in items if d.get("applicability") == "none" and not d.get("needs_manual_review")]
    manual = [d for d in items if d.get("needs_manual_review")]

    manual_row = f"| ⚠️ 待人工复核 | {len(manual)} |" if manual else ""

    # 按 applicability 分组渲染
    groups_order = [
        ("🔴 直接适用", high),
        ("🟡 潜在相关", medium),
        ("🟢 仅供参考", low),
        ("⚪ 不适用", none),
        ("⚠️ 待人工复核", manual),
    ]

    groups_md = ""
    group_tpl = _load_template("report_group.md")
    for title, grp in groups_order:
        if not grp:
            continue
        items_md = "\n".join(_render_item(item, i, _match_product_type(item, product_rules)) for i, item in enumerate(grp, 1))
        groups_md += group_tpl.format(group_title=title, items=items_md)

    # 附录
    appendix_rows = "\n".join(
        f"| {i} | {item.get('title', '-')[:40]} | "
        f"{'CDE' if item.get('source','').startswith('CDE') else 'NMPA' if item.get('source','').startswith('NMPA') else item.get('source','')} | "
        f"{item.get('date', '-')} | "
        f"{item.get('applicability', '-')} |"
        for i, item in enumerate(items, 1)
    )

    return _load_template("report.md").format(
        date=today,
        total=len(items),
        directly_applicable=len(high),
        potentially_relevant=len(medium),
        informational=len(low),
        manual_row=manual_row,
        groups=groups_md,
        appendix_rows=appendix_rows,
    )


def _update_history(items: list, gxpcode: str):
    history_path = os.path.join(SKILL_DIR, "gxpcode_data", "history.json")
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = {}
    today = datetime.now().strftime("%Y-%m-%d")
    for item in items:
        src = item.get("source", "")
        history.setdefault(src, [])
        title = item.get("title", "")
        url = item.get("url", "")
        if not title or not url:
            continue
        exist = any(r.get("title") == title and r.get("url") == url for r in history[src])
        if exist:
            continue
        history[src].append({"title": title, "url": url, "date": item.get("date", today), "first_seen": today, "last_updated": today})
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in history.values())
    print(f"history.json: {total} records")


def run(gxpcode: str):
    items = _load_s4(gxpcode)
    if not items:
        print("S4 is empty, nothing to report")
        return
    config = _load_config()
    product_rules = config.get("product_types", [])
    md = _build_report(items, product_rules)
    today = datetime.now().strftime("%Y-%m-%d")
    # 报告输出到工作空间（第二参数），未指定则落在 gxpcode_data
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"s5_report_{today}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
    _update_history(items, gxpcode)
    high = sum(1 for d in items if d.get("applicability") == "high")
    print(f"s5_report_{today}.md: {len(items)} items, {high} high")

    # 生成 PDF
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei','SimHei',sans-serif;font-size:11pt;color:#1a1a2e;background:#fff;padding:30px 50px}}
h1{{font-size:24pt;color:#0f3460;border-bottom:3px solid #16213e;padding-bottom:12px;margin-bottom:8px}}
h2{{font-size:14pt;color:#fff;margin:30px 0 12px;padding:10px 16px;border-radius:6px}}
h3{{font-size:12pt;color:#0f3460;margin:16px 0 10px;padding:8px 12px;background:#f8f9fc;border-radius:4px;border-left:3px solid #0f3460}}
table{{width:100%;border-collapse:collapse;margin:6px 0 16px;font-size:9.5pt}}
th{{background:#16213e;color:#fff;padding:8px 10px;text-align:left}}
td{{border-bottom:1px solid #e8e8e8;padding:6px 10px;vertical-align:top}}
tr:nth-child(even) td{{background:#fafafa}}
td:first-child{{white-space:nowrap;color:#666;font-weight:bold}}
blockquote{{margin:8px 0;padding:0}}
p{{margin:4px 0}}
a{{color:#533483;word-break:break-all;font-size:9pt}}
pre,code{{font-family:'Consolas',monospace;font-size:9pt;background:#f0f0f0;padding:2px 6px;border-radius:3px}}
hr{{border:none;border-top:1px solid #eee;margin:16px 0}}
/* 适用性色彩 */
h2:nth-of-type(1){{background:#e94560}}  /* 高适用 */
h2:nth-of-type(6){{background:#f5a623}}  /* 中适用 */
h2:nth-of-type(7){{background:#27ae60}}  /* 低适用 */
</style></head><body>
{markdown.markdown(md, extensions=['tables','fenced_code'])}
</body></html>"""
    pdf_path = os.path.join(output_dir, f"s5_report_{today}.pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html)
        page.pdf(path=pdf_path, format="A4", print_background=False)
        browser.close()
    print(f"s5_report_{today}.pdf: generated")


if __name__ == "__main__":
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else "gxpcode_data")
