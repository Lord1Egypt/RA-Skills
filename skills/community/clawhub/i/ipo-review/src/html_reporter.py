from __future__ import annotations

import html
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from .models import DocumentInfo, Evidence, FinancialFact, Issue, to_dict


def write_outputs(output_dir: str | Path, docs: list[DocumentInfo], evidence: list[Evidence],
                  facts: list[FinancialFact], issues: list[Issue], log_lines: list[str], diagnostics: dict | None = None) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    _write_json(out / "document_inventory.json", [to_dict(d) for d in docs])
    _write_json(out / "evidence_index.json", [to_dict(e) for e in evidence])
    _write_json(out / "issues.json", [to_dict(i) for i in issues])
    _write_csv(out / "financial_facts.csv", [to_dict(f) for f in facts])
    _write_csv(out / "nonfinancial_facts.csv", [])
    (out / "run_log.txt").write_text("\n".join(log_lines), encoding="utf-8")
    (out / "IPO问询回复复核分析报告.html").write_text(render_html(docs, facts, issues, diagnostics or {}), encoding="utf-8")


def render_html(docs: list[DocumentInfo], facts: list[FinancialFact], issues: list[Issue], diagnostics: dict | None = None) -> str:
    diagnostics = diagnostics or {}
    key_issues = [i for i in issues if i.review_priority == "key" and getattr(i, "display_default", True)]
    normal_issues = [i for i in issues if i.review_priority == "normal" and i.need_manual_review]
    tech_issues = [i for i in issues if i.category in {"期间表述提示", "格式及文字问题"}]
    noise_count = sum(1 for i in issues if i.review_priority == "noise")
    manual_count = len(key_issues) + len(normal_issues)
    tech_count = len(tech_issues)
    category_counts = Counter(i.category for i in key_issues)
    focus = "、".join(f"{k}{v}项" for k, v in category_counts.items()) or "无高优先级事项"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key_rows = "\n".join(_issue_card(i) for i in key_issues) or "<p class='empty'>本次未识别到高优先级待人工复核事项。</p>"
    normal_rows = "\n".join(_issue_card(i) for i in normal_issues) or "<p class='empty'>暂无一般复核事项。</p>"
    tech_rows = "\n".join(_issue_card(i) for i in tech_issues) or "<p class='empty'>暂无期间或格式类技术提示。</p>"
    doc_rows = "\n".join(
        f"<tr><td>{html.escape(d.filename)}</td><td>{html.escape(d.role_name)}</td><td>{html.escape(d.parse_status)}</td></tr>"
        for d in docs
    ) or "<tr><td colspan='3'>input目录下暂无可解析文件。</td></tr>"
    diag_rows = _diagnostic_rows(facts, diagnostics, noise_count)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IPO问询回复复核报告</title>
<style>
:root {{ --bg:#f7f8fa; --paper:#fff; --text:#202833; --muted:#667085; --line:#d7dce3; --blue:#1f4e79; --orange:#9a4b00; --red:#9f1d1d; --soft:#f2f5f9; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:"Microsoft YaHei",Arial,sans-serif; line-height:1.65; }}
header {{ background:#243447; color:#fff; padding:24px 32px; border-bottom:4px solid #d98c2b; }}
h1 {{ margin:0 0 4px; font-size:26px; font-weight:700; }}
h2 {{ margin:26px 0 12px; font-size:20px; color:#1f3447; }}
h3 {{ margin:0 0 10px; font-size:18px; color:#1f3447; }}
main {{ max-width:1160px; margin:0 auto; padding:22px; }}
.summary-text,.issue,.appendix,details.panel {{ background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:16px; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:14px 0; }}
.card {{ background:#fff; border:1px solid var(--line); border-left:4px solid var(--blue); border-radius:6px; padding:12px 14px; }}
.card span {{ display:block; color:var(--muted); font-size:13px; }}
.card strong {{ display:block; font-size:28px; color:#1f3447; }}
.toolbar {{ position:sticky; top:0; z-index:5; background:rgba(247,248,250,.96); border-bottom:1px solid var(--line); padding:10px 0; display:flex; gap:10px; flex-wrap:wrap; }}
select,input {{ border:1px solid var(--line); border-radius:5px; padding:8px 10px; min-width:190px; background:#fff; }}
.section-note {{ color:var(--muted); margin-top:-6px; }}
.issue {{ margin:12px 0; border-left:4px solid var(--blue); }}
.issue.normal {{ border-left-color:#6b7280; }}
.issue.tech {{ border-left-color:#9a4b00; }}
.meta {{ display:flex; gap:8px; flex-wrap:wrap; color:var(--muted); font-size:13px; margin-bottom:8px; }}
.tag {{ border:1px solid var(--line); border-radius:999px; padding:1px 8px; background:#f8fafc; }}
.priority {{ color:#fff; background:var(--blue); border-color:var(--blue); }}
table {{ width:100%; border-collapse:collapse; background:#fff; margin:10px 0; }}
th,td {{ border:1px solid var(--line); padding:7px 9px; vertical-align:top; }}
th {{ background:var(--soft); text-align:left; color:#344054; }}
.num {{ text-align:right; white-space:nowrap; }}
.diff {{ color:var(--red); font-weight:600; }}
.evidence-list {{ margin:6px 0 10px; padding-left:20px; }}
details {{ margin-top:10px; }}
details summary {{ cursor:pointer; color:var(--blue); font-weight:600; }}
pre {{ white-space:pre-wrap; background:#f8fafc; border:1px solid var(--line); border-radius:5px; padding:10px; max-height:220px; overflow:auto; }}
.empty {{ color:var(--muted); }}
.appendix ul {{ margin-top:6px; }}
@media (max-width:760px) {{ main {{ padding:14px; }} .toolbar {{ position:static; }} select,input {{ width:100%; }} }}
</style>
</head>
<body>
<header>
  <h1>IPO问询回复复核报告</h1>
  <div>项目组待人工复核清单｜生成时间：{generated_at}</div>
</header>
<main>
  <section>
    <h2>一、复核结论摘要</h2>
    <div class="summary-text">
      本次共识别需人工复核事项 <strong>{manual_count}</strong> 项，其中高优先级 <strong>{len(key_issues)}</strong> 项，一般复核 <strong>{len(normal_issues)}</strong> 项。
      重点包括：{html.escape(focus)}。建议项目组优先核对高优先级事项。
    </div>
    <div class="cards">
      <div class="card"><span>需人工复核</span><strong>{manual_count}</strong></div>
      <div class="card"><span>高优先级</span><strong>{len(key_issues)}</strong></div>
      <div class="card"><span>一般复核</span><strong>{len(normal_issues)}</strong></div>
      <div class="card"><span>技术提示</span><strong>{tech_count}</strong></div>
    </div>
  </section>

  <section>
    <h2>二、待人工复核清单</h2>
    <p class="section-note">默认仅展示高优先级事项：表文数据不一致、截止日口径不一致、正式财务差异及高价值数学勾稽。</p>
    <div class="toolbar">
      <select id="scope">
        <option value="key">只看重点复核</option>
        <option value="manual">查看全部人工复核</option>
        <option value="tech">查看技术提示</option>
      </select>
      <select id="type">
        <option value="">全部问题类型</option>
        <option value="表文数据不一致">表文数据不一致</option>
        <option value="截止日口径不一致">截止日口径不一致</option>
        <option value="财务">财务数据差异</option>
        <option value="数学勾稽">数学勾稽</option>
        <option value="格式">格式文字</option>
      </select>
      <input id="keyword" placeholder="搜索文件、位置、指标">
    </div>
    <div id="issues">{key_rows}{normal_rows}{tech_rows}</div>
  </section>

  <details class="panel">
    <summary>三、一般复核事项（默认折叠）</summary>
    {normal_rows}
  </details>

  <details class="panel">
    <summary>四、口径不同提示（默认折叠）</summary>
    <p>调整口径、预测测算、孰低/孰高等事项已保留在 <code>caliber_notes.csv</code> 和 <code>comparison_exclusions.csv</code>，不计入待人工复核异常。</p>
    <table><thead><tr><th>文件</th><th>说明</th></tr></thead><tbody><tr><td>caliber_notes.csv</td><td>业务型口径排除事项清单</td></tr><tr><td>comparison_exclusions.csv</td><td>全部不可比或被排除事实</td></tr></tbody></table>
  </details>

  <details class="appendix">
    <summary>五、技术诊断附录（默认折叠）</summary>
    <table><thead><tr><th>项目</th><th>数量</th></tr></thead><tbody>{diag_rows}</tbody></table>
    <h3>文件清单</h3>
    <table><thead><tr><th>文件</th><th>角色</th><th>解析状态</th></tr></thead><tbody>{doc_rows}</tbody></table>
    <p>详细数据请查看：</p>
    <ul>
      <li>issues.json</li><li>financial_facts.csv</li><li>comparison_exclusions.csv</li><li>caliber_notes.csv</li>
      <li>arithmetic_skips.csv</li><li>parse_errors.csv</li><li>evidence_index.json</li><li>run_log.txt</li>
    </ul>
  </details>
</main>
<script>
const scope = document.getElementById('scope');
const type = document.getElementById('type');
const keyword = document.getElementById('keyword');
function applyFilter() {{
  const sc = scope.value;
  const ty = type.value;
  const kw = keyword.value.trim().toLowerCase();
  document.querySelectorAll('.issue').forEach(card => {{
    const okScope = sc === 'manual' ? card.dataset.scope !== 'tech' : card.dataset.scope === sc;
    const okType = !ty || card.dataset.category.includes(ty) || (ty === '财务' && card.dataset.category.includes('财务'));
    const okKw = !kw || card.textContent.toLowerCase().includes(kw);
    card.style.display = okScope && okType && okKw ? '' : 'none';
  }});
}}
scope.addEventListener('change', applyFilter);
type.addEventListener('change', applyFilter);
keyword.addEventListener('input', applyFilter);
applyFilter();
</script>
</body>
</html>"""


def _issue_card(issue: Issue) -> str:
    scope = "key" if issue.review_priority == "key" else ("tech" if issue.category in {"期间表述提示", "格式及文字问题"} else "manual")
    priority_label = "高优先级" if scope == "key" else ("技术提示" if scope == "tech" else "一般复核")
    title = _business_title(issue)
    detail = _detail_table(issue)
    evidence = _evidence_list(issue)
    suggestion = _business_suggestion(issue)
    excerpts = _excerpts(issue)
    tech = _technical_info(issue)
    css = "issue" + (" normal" if scope == "manual" else " tech" if scope == "tech" else "")
    return f"""<article class="{css}" data-scope="{scope}" data-category="{html.escape(issue.category)}">
  <div class="meta"><span class="tag priority">{priority_label}</span><span class="tag">{html.escape(issue.category)}</span></div>
  <h3>{html.escape(title)}</h3>
  <p><strong>复核结论：</strong>{html.escape(_business_conclusion(issue))}</p>
  {detail}
  <p><strong>证据位置：</strong></p>{evidence}
  <p><strong>建议处理：</strong>{html.escape(suggestion)}</p>
  {excerpts}
  {tech}
</article>"""


def _business_title(issue: Issue) -> str:
    if issue.category == "表文数据不一致":
        return f"【表文数据不一致】{issue.item}：正文与表格披露不一致"
    if issue.category == "截止日口径不一致":
        metric = issue.item.replace("|", "")
        return f"【截止日口径不一致】{metric}：统计截止日不一致"
    if issue.category == "数学勾稽错误":
        parts = issue.item.split("/")
        table = parts[0] if parts else "表格"
        item = parts[1] if len(parts) > 1 else issue.item
        return f"【数学勾稽】{table} {item}：合计与明细不一致"
    if "财务" in issue.category or "跨文件" in issue.category:
        metric = issue.item.split("|")[1] if "|" in issue.item and len(issue.item.split("|")) > 1 else issue.item
        return f"【财务数据差异】{metric}：不同文件披露金额不一致"
    if issue.category == "格式及文字问题":
        return "【格式文字】文本格式或表述需要核对"
    return f"【{issue.category}】{issue.item}"


def _business_conclusion(issue: Issue) -> str:
    if issue.category == "表文数据不一致":
        years = "、".join(re.findall(r"(20\d{2})年度", issue.caliber_analysis))
        return f"正文披露的{years or '相关年度'}{issue.item}与紧邻表格披露值不一致。"
    if issue.category == "截止日口径不一致":
        dates = "、".join(re.findall(r"20\d{2}-\d{2}(?:-\d{2})?", issue.caliber_analysis))
        return f"同一主题“{issue.item}”使用了不同统计截止日：{dates}。"
    if issue.category == "数学勾稽错误":
        return _math_sentence(issue)
    return issue.conclusion


def _detail_table(issue: Issue) -> str:
    if issue.category == "表文数据不一致":
        rows = []
        pattern = re.compile(r"(20\d{2})年度：正文(-?\d+(?:\.\d+)?)%，表格(-?\d+(?:\.\d+)?)%，差异(-?\d+(?:\.\d+)?)个百分点")
        for year, text_v, table_v, diff in pattern.findall(issue.caliber_analysis):
            rows.append(f"<tr><td>{year}年度</td><td class='num'>{float(text_v):.2f}%</td><td class='num'>{float(table_v):.2f}%</td><td class='num diff'>{float(diff):.2f}个百分点</td></tr>")
        return "<table><thead><tr><th>年度</th><th>正文披露</th><th>表格披露</th><th>差异</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>" if rows else ""
    if issue.category == "截止日口径不一致":
        return _cutoff_table(issue)
    if issue.category == "数学勾稽错误":
        return _math_table(issue)
    if "财务" in issue.category or "跨文件" in issue.category:
        return _financial_table(issue)
    return ""


def _cutoff_table(issue: Issue) -> str:
    rows = []
    for source, text in [(issue.source_1, issue.source_1_text), (issue.source_2, issue.source_2_text)]:
        match = re.match(r"(.+?)\s+(\S+)：截至(20\d{2}-\d{2}(?:-\d{2})?)", source)
        if match:
            file, pos, date = match.groups()
        else:
            file, pos, date = source, "", ""
        excerpt = _trim(text.split("｜", 1)[-1] if "｜" in text else text)
        rows.append(f"<tr><td>{html.escape(file)}</td><td>{html.escape(pos)}</td><td>{html.escape(date)}</td><td>{html.escape(excerpt)}</td></tr>")
    return "<table><thead><tr><th>来源文件</th><th>位置</th><th>截止日</th><th>原文摘要</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def _math_table(issue: Issue) -> str:
    detail = _number_after(issue.source_1, "明细求和=")
    total = _number_after(issue.source_2, "披露合计=")
    diff = issue.diff_amount if issue.diff_amount is not None else (total - detail if detail is not None and total is not None else None)
    ratio = f"{issue.diff_ratio:.2%}" if issue.diff_ratio is not None else ""
    parts = issue.item.split("/")
    table = parts[0] if parts else ""
    item = parts[1] if len(parts) > 1 else issue.item
    judgement = "简单合计表，超过披露精度尾差" if issue.arithmetic_rule_type == "simple_sum" else "需结合表格结构人工判断"
    return (
        "<table><thead><tr><th>表格</th><th>项目</th><th>明细合计</th><th>披露合计</th><th>差异</th><th>偏离率</th><th>判断</th></tr></thead><tbody>"
        f"<tr><td>{html.escape(table)}</td><td>{html.escape(item)}</td><td class='num'>{_fmt_num(detail)}</td><td class='num'>{_fmt_num(total)}</td><td class='num diff'>{_fmt_num(diff)}</td><td class='num'>{ratio}</td><td>{html.escape(judgement)}</td></tr>"
        "</tbody></table>"
    )


def _financial_table(issue: Issue) -> str:
    parts = issue.item.split("|")
    metric = parts[1] if len(parts) > 1 else issue.item
    period = parts[2] if len(parts) > 2 else ""
    return (
        "<table><thead><tr><th>指标</th><th>期间</th><th>来源1</th><th>来源2</th><th>差异</th></tr></thead><tbody>"
        f"<tr><td>{html.escape(metric)}</td><td>{html.escape(period)}</td><td>{html.escape(issue.source_1)}</td><td>{html.escape(issue.source_2)}</td><td class='diff'>{_fmt_num(issue.diff_amount)}</td></tr>"
        "</tbody></table>"
    )


def _evidence_list(issue: Issue) -> str:
    items = []
    for page in issue.evidence_pages:
        if " " in page:
            file, pos = page.rsplit(" ", 1)
            items.append(f"<li>{html.escape(file)}：{html.escape(pos)}</li>")
        else:
            items.append(f"<li>{html.escape(page)}</li>")
    return "<ul class='evidence-list'>" + "".join(items) + "</ul>"


def _business_suggestion(issue: Issue) -> str:
    if issue.category == "表文数据不一致":
        return "建议核对正文与表格的数据来源。如表格为最新数据，应同步修改正文描述；如正文正确，应调整表格对应年度数据。"
    if issue.category == "截止日口径不一致":
        return "建议统一期后回款统计截止日。若不同文件因统计范围不同确需使用不同截止日，应在相关位置补充说明原因。"
    if issue.category == "数学勾稽错误":
        return "建议核对合计行对应的明细范围，确认是否存在遗漏项目、小计行、跨页项目或单位不一致。"
    if "财务" in issue.category or "跨文件" in issue.category:
        return "建议核对两处披露是否为同一主体、同一期间、同一口径。如为同一口径，应统一披露金额；如口径不同，应补充说明。"
    return issue.suggestion or "请结合原文证据进行人工核对。"


def _excerpts(issue: Issue) -> str:
    parts = []
    for text in [issue.source_1_text, issue.source_2_text]:
        if text:
            parts.append(f"<pre>{html.escape(_trim(text, 300))}</pre>")
    if not parts:
        return ""
    return "<details><summary>展开原文</summary>" + "".join(parts) + "</details>"


def _technical_info(issue: Issue) -> str:
    body = (
        f"issue_id：{html.escape(issue.issue_id)}\n"
        f"evidence_ids：{html.escape(', '.join(issue.evidence_ids))}\n"
        f"rule_type：{html.escape(issue.arithmetic_rule_type or issue.category)}\n"
        f"skip_reason：{html.escape(issue.arithmetic_skip_reason or getattr(issue, 'noise_reason', '') or '')}"
    )
    return f"<details><summary>开发诊断信息</summary><pre>{body}</pre></details>"


def _diagnostic_rows(facts: list[FinancialFact], diagnostics: dict, noise_count: int) -> str:
    rows = [
        ("财务事实", len(facts)),
        ("确认一致事项", diagnostics.get("确认一致事项", "")),
        ("正常舍入事项", diagnostics.get("正常舍入事项", "")),
        ("comparison_exclusions", diagnostics.get("comparison_exclusions.csv", "")),
        ("caliber_notes", diagnostics.get("caliber_notes.csv", "")),
        ("arithmetic_skips", diagnostics.get("arithmetic_skips.csv", "")),
        ("噪声参考", diagnostics.get("噪声参考", noise_count)),
        ("parse_errors", diagnostics.get("parse_errors.csv", "")),
    ]
    return "".join(f"<tr><td>{html.escape(str(k))}</td><td class='num'>{html.escape(str(v))}</td></tr>" for k, v in rows)


def _math_sentence(issue: Issue) -> str:
    detail = _number_after(issue.source_1, "明细求和=")
    total = _number_after(issue.source_2, "披露合计=")
    diff = total - detail if detail is not None and total is not None else issue.diff_amount
    item = issue.item.split("/")[1] if "/" in issue.item and len(issue.item.split("/")) > 1 else issue.item
    return f"表格中“{item}”明细合计为{_fmt_num(detail)}，披露合计为{_fmt_num(total)}，存在{_fmt_num(diff)}差异。"


def _number_after(text: str, prefix: str) -> float | None:
    if prefix not in text:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text.split(prefix, 1)[1].replace(",", ""))
    return float(match.group(0)) if match else None


def _fmt_num(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _trim(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit] + "..."


def _write_json(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    import csv
    keys = sorted({k for row in rows for k in row}) if rows else ["empty"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
