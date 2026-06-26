#!/usr/bin/env python3
"""
Dynamic Kanban Generator v6.0 - 审核清单看板（动态交互式）

不再是纯静态 HTML。生成独立 HTML 文件 + 内嵌原生 JavaScript（零依赖）：
- 筛选：按类别/状态/通过率区间
- 排序：点击列头排序
- 搜索：输入规则ID、人员工号、规则名即时过滤
- 展开明细：点击异常行展开详细人员列表
- 导出：一键导出当前筛选结果为 CSV
- 深色模式：一键切换
- 锚定链接：URL 参数支持 ?filter=red&rule=RL-001 直接定位

输入: data_index.json（由 generate_data_index.py 生成）
输出: kanban_v6.html

用法:
    python3 scripts/generate_kanban_v6.py --input data_index.json --output kanban_v6.html
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_dynamic_kanban(index, review_link_template=None):
    """生成动态 HTML 看板，包含内嵌 JavaScript"""

    rules = index.get("rule_index", {})
    summary = index.get("summary", {})
    total_records = index.get("total_records", 0)
    audit_id = index.get("audit_id", "")
    timestamp = index.get("timestamp", "")
    version = index.get("version", "")

    # Build JSON data for JS
    import json as json_mod
    rules_json = json_mod.dumps(rules, ensure_ascii=False)
    summary_json = json_mod.dumps(summary, ensure_ascii=False)

    # Category colors for JS
    category_colors = {
        "字段完整性": "#3b82f6",
        "公式校验": "#8b5cf6",
        "业务规则": "#06b6d4",
        "红线": "#ef4444",
        "黄线": "#f59e0b",
        "蓝线": "#6366f1",
        "政策校验": "#10b981",
        "红线阻断": "#ef4444",
        "黄线异常": "#f59e0b",
        "蓝线提示": "#6366f1",
    }

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工资审核清单看板 v6 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
<style>
  :root {{
    --bg: #f1f5f9;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --header-bg: linear-gradient(135deg, #1e40af, #3b82f6);
    --header-text: #ffffff;
    --row-hover: #f8fafc;
    --input-bg: #ffffff;
    --input-border: #cbd5e1;
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
    --badge-pass-bg: #dcfce7;
    --badge-pass-text: #16a34a;
    --badge-warning-bg: #fef3c7;
    --badge-warning-text: #d97706;
    --badge-block-bg: #fecaca;
    --badge-block-text: #dc2626;
    --badge-note-bg: #e0e7ff;
    --badge-note-text: #4f46e5;
  }}
  .dark {{
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --header-bg: linear-gradient(135deg, #1e3a8a, #1d4ed8);
    --header-text: #f1f5f9;
    --row-hover: #334155;
    --input-bg: #1e293b;
    --input-border: #475569;
    --shadow: 0 1px 3px rgba(0,0,0,0.3);
    --badge-pass-bg: #14532d;
    --badge-pass-text: #86efac;
    --badge-warning-bg: #78350f;
    --badge-warning-text: #fbbf24;
    --badge-block-bg: #7f1d1d;
    --badge-block-text: #fca5a5;
    --badge-note-bg: #312e81;
    --badge-note-text: #a5b4fc;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); padding: 24px; transition: background 0.2s, color 0.2s; }}
  .header {{ background: var(--header-bg); color: var(--header-text); padding: 28px; border-radius: 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
  .header h1 {{ font-size: 24px; }}
  .header .meta {{ font-size: 13px; opacity: 0.85; }}
  .header-actions {{ display: flex; gap: 8px; align-items: center; }}
  .btn {{ padding: 6px 14px; border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; background: rgba(255,255,255,0.15); color: white; cursor: pointer; font-size: 13px; transition: background 0.2s; }}
  .btn:hover {{ background: rgba(255,255,255,0.3); }}
  .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 16px; }}
  .card {{ background: var(--card-bg); border-radius: 12px; padding: 16px; box-shadow: var(--shadow); text-align: center; }}
  .card .number {{ font-size: 28px; font-weight: 700; }}
  .card .label {{ font-size: 12px; color: var(--text-secondary); margin-top: 2px; }}
  .card.pass .number {{ color: #22c55e; }}
  .card.warning .number {{ color: #f59e0b; }}
  .card.block .number {{ color: #ef4444; }}
  .card.note .number {{ color: #6366f1; }}
  .card.total .number {{ color: #3b82f6; }}
  .card.rate .number {{ color: #059669; }}
  .controls {{ background: var(--card-bg); border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: var(--shadow); display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
  .controls label {{ font-size: 13px; color: var(--text-secondary); font-weight: 500; }}
  .controls select, .controls input {{ padding: 6px 10px; border: 1px solid var(--input-border); border-radius: 6px; font-size: 13px; background: var(--input-bg); color: var(--text); }}
  .controls input[type="text"] {{ width: 200px; }}
  .controls .search-box {{ flex: 1; min-width: 180px; }}
  .controls .result-count {{ margin-left: auto; font-size: 13px; color: var(--text-secondary); }}
  .table-container {{ background: var(--card-bg); border-radius: 12px; box-shadow: var(--shadow); overflow: hidden; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: var(--card-bg); padding: 10px 12px; text-align: left; color: var(--text-secondary); font-weight: 600; border-bottom: 2px solid var(--border); white-space: nowrap; cursor: pointer; user-select: none; position: sticky; top: 0; z-index: 1; }}
  th:hover {{ color: var(--text); }}
  th .sort-icon {{ font-size: 10px; margin-left: 4px; opacity: 0.4; }}
  th.sorted .sort-icon {{ opacity: 1; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  tr {{ background: var(--card-bg); }}
  tr:hover td {{ background: var(--row-hover); }}
  tr.expanded td {{ background: var(--row-hover); }}
  .category-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; color: white; }}
  .status-badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
  .status-pass {{ background: var(--badge-pass-bg); color: var(--badge-pass-text); }}
  .status-warning {{ background: var(--badge-warning-bg); color: var(--badge-warning-text); }}
  .status-block {{ background: var(--badge-block-bg); color: var(--badge-block-text); }}
  .status-note {{ background: var(--badge-note-bg); color: var(--badge-note-text); }}
  .rule-id {{ font-family: monospace; font-size: 11px; color: var(--text-secondary); }}
  .rate-bar {{ display: inline-block; width: 50px; height: 5px; background: var(--border); border-radius: 3px; vertical-align: middle; margin-left: 4px; }}
  .rate-bar-fill {{ height: 100%; border-radius: 3px; transition: width 0.3s; }}
  .detail-row {{ display: none; }}
  .detail-row.show {{ display: table-row; }}
  .detail-row td {{ background: var(--row-hover); padding: 12px; }}
  .detail-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  .detail-table th {{ font-size: 11px; padding: 6px 8px; border-bottom: 1px solid var(--border); }}
  .detail-table td {{ padding: 4px 8px; border-bottom: 1px solid var(--border); }}
  .person-tag {{ display: inline-block; padding: 1px 6px; background: #fef2f2; color: #dc2626; border-radius: 3px; font-size: 11px; margin: 1px; }}
  .person-tag.yellow {{ background: #fffbeb; color: #d97706; }}
  .expand-btn {{ cursor: pointer; color: #3b82f6; font-size: 12px; text-decoration: none; }}
  .expand-btn:hover {{ text-decoration: underline; }}
  .footer {{ text-align: center; padding: 16px; color: var(--text-secondary); font-size: 12px; }}
  .hidden {{ display: none !important; }}
  @media (max-width: 768px) {{ table {{ font-size: 11px; }} td, th {{ padding: 6px 8px; }} .controls {{ flex-direction: column; }} .controls .search-box {{ width: 100%; }} }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>📋 工资审核清单看板 v6.0</h1>
    <div class="meta">
      审核ID: {audit_id} | 时间: {timestamp[:19].replace('T', ' ')} |
      记录: {total_records} 条 | 版本: {version}
    </div>
  </div>
  <div class="header-actions">
    <button class="btn" onclick="toggleDark()">🌗 深色</button>
    <button class="btn" onclick="exportCSV()">📥 导出CSV</button>
    <a href="audit_report_v6.html" class="btn" target="_blank">📄 报告</a>
  </div>
</div>

<div class="summary-cards">
  <div class="card total"><div class="number">{summary.get('total_rules', 0)}</div><div class="label">审核条目</div></div>
  <div class="card pass"><div class="number">{summary.get('passed_rules', 0)}</div><div class="label">✅ 通过</div></div>
  <div class="card warning"><div class="number">{summary.get('total_rules', 0) - summary.get('passed_rules', 0)}</div><div class="label">🟠 异常</div></div>
  <div class="card block"><div class="number">{summary.get('red_count', 0)}</div><div class="label">🔴 红线</div></div>
  <div class="card note"><div class="number">{summary.get('blue_count', 0)}</div><div class="label">🔵 蓝线</div></div>
</div>

<div class="controls">
  <label>类别:</label>
  <select id="filterCategory" onchange="applyFilters()">
    <option value="all">全部</option>
    <option value="字段完整性">字段完整性</option>
    <option value="公式校验">公式校验</option>
    <option value="业务规则">业务规则</option>
    <option value="红线">红线</option>
    <option value="黄线">黄线</option>
    <option value="蓝线">蓝线</option>
    <option value="政策校验">政策校验</option>
  </select>

  <label>状态:</label>
  <select id="filterStatus" onchange="applyFilters()">
    <option value="all">全部</option>
    <option value="pass">✅ 通过</option>
    <option value="warning">🟠 异常</option>
    <option value="block">🔴 阻断</option>
    <option value="note">🔵 提示</option>
  </select>

  <label>搜索:</label>
  <input type="text" id="searchInput" class="search-box" placeholder="规则ID、规则名、工号..." oninput="applyFilters()">

  <div class="result-count" id="resultCount">加载中...</div>
</div>

<div class="table-container">
  <table id="kanbanTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">#<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(1)">类别<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(2)">规则ID<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(3)">审核条目<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(4)">结果<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(5)">检查数<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(6)">通过<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(7)">异常<span class="sort-icon">▼</span></th>
        <th onclick="sortTable(8)">通过率<span class="sort-icon">▼</span></th>
        <th>数据依据</th>
        <th>处理建议</th>
      </tr>
    </thead>
    <tbody id="kanbanBody">
    </tbody>
  </table>
</div>

<div class="footer">
  工资审核清单看板 v6.0 | 动态交互式 | 数据来源: data_index.json | 关联: audit_report_v6.html
</div>

<script>
// Data
const RULES_DATA = {rules_json};
const SUMMARY_DATA = {summary_json};
const CATEGORY_COLORS = {json.dumps(category_colors)};

let allRules = [];
let filteredRules = [];
let sortCol = -1;
let sortAsc = true;

// Status labels
const STATUS_LABELS = {{
  "pass": "✅ 通过",
  "warning": "🟠 异常",
  "block": "🔴 阻断",
  "note": "🔵 提示",
}};

// Initialize
function init() {{
  // Convert object to sorted array
  allRules = Object.entries(RULES_DATA).map(([id, r]) => ({{ id, ...r }}));

  // Check URL params
  const params = new URLSearchParams(window.location.search);
  const filterRule = params.get('rule');
  const filterCat = params.get('filter');

  if (filterRule) {{
    document.getElementById('searchInput').value = filterRule;
  }}
  if (filterCat) {{
    document.getElementById('filterCategory').value = filterCat;
  }}

  applyFilters();
}}

// Apply filters
function applyFilters() {{
  const cat = document.getElementById('filterCategory').value;
  const status = document.getElementById('filterStatus').value;
  const search = document.getElementById('searchInput').value.trim().toLowerCase();

  filteredRules = allRules.filter(r => {{
    if (cat !== 'all' && r.category !== cat) return false;
    if (status !== 'all' && r.status !== status) return false;
    if (search) {{
      const haystack = `${{r.id}} ${{r.name}} ${{r.category}}`.toLowerCase();
      // Also search in details
      const detailText = (r.details || []).map(d => JSON.stringify(d)).join(' ').toLowerCase();
      if (!haystack.includes(search) && !detailText.includes(search)) return false;
    }}
    return true;
  }});

  if (sortCol >= 0) {{
    doSort(sortCol, sortAsc);
  }}

  renderTable();
}}

// Sort
function sortTable(colIndex) {{
  if (sortCol === colIndex) {{
    sortAsc = !sortAsc;
  }} else {{
    sortCol = colIndex;
    sortAsc = true;
  }}
  doSort(colIndex, sortAsc);
  renderTable();
}}

function doSort(colIndex, asc) {{
  const keyMap = [null, 'category', 'id', 'name', 'status', 'checked', 'passed', 'failed', 'rate'];
  const key = keyMap[colIndex];
  if (!key) return;

  filteredRules.sort((a, b) => {{
    let va = a[key], vb = b[key];
    if (typeof va === 'number' && typeof vb === 'number') return asc ? va - vb : vb - va;
    // For rate, parse percentage
    if (key === 'rate') {{
      va = parseFloat(String(va).replace('%', '')) || 0;
      vb = parseFloat(String(vb).replace('%', '')) || 0;
      return asc ? va - vb : vb - va;
    }}
    return asc ? String(va).localeCompare(String(vb), 'zh') : String(vb).localeCompare(String(va), 'zh');
  }});
}}

// Render
function renderTable() {{
  const tbody = document.getElementById('kanbanBody');
  const countEl = document.getElementById('resultCount');
  countEl.textContent = `显示 ${{filteredRules.length}} / ${{allRules.length}} 条`;

  let html = '';
  filteredRules.forEach((r, idx) => {{
    const catColor = CATEGORY_COLORS[r.category] || '#64748b';
    const statusClass = `status-${{r.status}}`;
    const statusLabel = STATUS_LABELS[r.status] || r.status;
    const rateVal = parseFloat(String(r.rate).replace('%', '')) || 0;
    const barColor = rateVal >= 98 ? '#22c55e' : (rateVal >= 90 ? '#f59e0b' : '#ef4444');
    const detailCount = r.detail_count || (r.details || []).length;
    const hasDetails = detailCount > 0 && r.status !== 'pass';

    html += `<tr id="row-${{r.id}}" data-id="${{r.id}}">`;
    html += `<td>${{idx + 1}}</td>`;
    html += `<td><span class="category-tag" style="background:${{catColor}}">${{r.category}}</span></td>`;
    html += `<td><span class="rule-id">${{r.id}}</span></td>`;
    html += `<td><strong>${{r.name}}</strong></td>`;
    html += `<td><span class="status-badge ${{statusClass}}">${{statusLabel}}</span></td>`;
    html += `<td style="text-align:center">${{r.checked.toLocaleString()}}</td>`;
    html += `<td style="text-align:center;color:#22c55e">${{r.passed.toLocaleString()}}</td>`;
    html += `<td style="text-align:center;color:#ef4444;font-weight:600">${{r.failed.toLocaleString()}}</td>`;
    html += `<td>${{r.rate}}<span class="rate-bar"><span class="rate-bar-fill" style="width:${{rateVal}}%;background:${{barColor}}"></span></span></td>`;

    // Evidence
    const evidence = `${{r.checked}}条记录中，${{r.passed}}条通过，${{r.failed}}条异常`;
    html += `<td style="max-width:200px;font-size:12px;color:var(--text-secondary)">${{evidence}}</td>`;

    // Action
    let actionHtml = r.action || '无需操作';
    if (hasDetails) {{
      actionHtml += `<br><a class="expand-btn" href="#" onclick="toggleDetail('${{r.id}}'); return false;">📋 展开 ${{detailCount}} 条明细</a>`;
    }}
    html += `<td style="max-width:180px;font-size:12px">${{actionHtml}}</td>`;
    html += `</tr>`;

    // Detail row
    if (hasDetails && r.details && r.details.length > 0) {{
      html += `<tr class="detail-row" id="detail-${{r.id}}">`;
      html += `<td colspan="11">`;
      html += `<div style="max-height:300px;overflow-y:auto;">`;
      html += `<table class="detail-table">`;
      html += `<thead><tr><th>工号</th><th>姓名</th><th>异常值</th><th>预期值</th><th>说明</th></tr></thead>`;
      html += `<tbody>`;
      r.details.forEach(d => {{
        const empId = d['工号'] || d['emp_id'] || '';
        const empName = d['姓名代号'] || d['name'] || '';
        const val = d['value'] || d['diff'] || '';
        const expected = d['expected'] || '';
        const note = d['note'] || d['reason'] || '';
        html += `<tr><td>${{empId}}</td><td><span class="person-tag ${{r.status === 'warning' ? 'yellow' : ''}}">${{empName}}</span></td><td>${{val}}</td><td>${{expected}}</td><td style="font-size:11px;color:var(--text-secondary)">${{note}}</td></tr>`;
      }});
      html += `</tbody></table></div></td></tr>`;
    }}
  }});

  tbody.innerHTML = html;

  // Highlight URL-matched rule
  const params = new URLSearchParams(window.location.search);
  const targetRule = params.get('rule');
  if (targetRule) {{
    const row = document.getElementById(`row-${{targetRule}}`);
    if (row) {{
      row.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      row.style.background = '#fef3c7';
      setTimeout(() => {{ row.style.background = ''; }}, 3000);
    }}
  }}
}}

// Toggle detail
function toggleDetail(ruleId) {{
  const detailRow = document.getElementById(`detail-${{ruleId}}`);
  if (!detailRow) return;
  detailRow.classList.toggle('show');
  const row = document.getElementById(`row-${{ruleId}}`);
  if (row) row.classList.toggle('expanded');
}}

// Dark mode
function toggleDark() {{
  document.body.classList.toggle('dark');
  const isDark = document.body.classList.contains('dark');
  localStorage.setItem('kanban-dark', isDark ? '1' : '0');
}}

// CSV export
function exportCSV() {{
  const headers = ['#', '类别', '规则ID', '审核条目', '结果', '检查数', '通过', '异常', '通过率', '数据依据', '处理建议'];
  const rows = [headers.join(',')];

  filteredRules.forEach((r, idx) => {{
    const statusLabel = STATUS_LABELS[r.status] || r.status;
    const evidence = `${{r.checked}}条记录中，${{r.passed}}条通过，${{r.failed}}条异常`;
    rows.push([
      idx + 1,
      `"${{r.category}}"`,
      `"${{r.id}}"`,
      `"${{r.name}}"`,
      `"${{statusLabel}}"`,
      r.checked,
      r.passed,
      r.failed,
      `"${{r.rate}}"`,
      `"${{evidence}}"`,
      `"${{r.action || '无需操作'}}"`
    ].join(','));
  }});

  const csvContent = '\\uFEFF' + rows.join('\\n');  // BOM for Excel
  const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `kanban_${{new Date().toISOString().slice(0, 10)}}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}}

// Init
document.addEventListener('DOMContentLoaded', () => {{
  init();
  // Restore dark mode
  if (localStorage.getItem('kanban-dark') === '1') {{
    document.body.classList.add('dark');
  }}
}});
</script>

</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="动态审核清单看板生成器 v6.0")
    parser.add_argument("--input", help="data_index.json 路径")
    parser.add_argument("--audit-result", help="audit_result.json 路径（备选，自动生成索引）")
    parser.add_argument("--output", default="kanban_v6.html", help="输出文件路径")
    args = parser.parse_args()

    if args.audit_result:
        from generate_data_index import generate_index
        with open(args.audit_result, encoding="utf-8") as f:
            audit_result = json.load(f)
        index = generate_index(audit_result)
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            index = json.load(f)
    else:
        parser.error("需要 --input data_index.json 或 --audit-result audit_result.json")

    html = generate_dynamic_kanban(index)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 动态看板 v6 已生成: {args.output} ({len(html):,} bytes)")
    print(f"   规则数: {len(index.get('rule_index', {{}}))}")


if __name__ == "__main__":
    main()
