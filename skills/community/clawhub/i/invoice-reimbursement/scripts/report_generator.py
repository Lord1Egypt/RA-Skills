#!/usr/bin/env python3
"""
发票报销报告生成器 — 生成交互式HTML可视化报告
"""
import json
import os
import sys
import argparse
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from invoice_manager import get_db, list_invoices, get_summary, get_invoice

CATEGORY_COLORS = {
    "餐饮": "#FF6B6B", "交通": "#4ECDC4", "住宿": "#45B7D1",
    "办公": "#96CEB4", "通讯": "#FFEAA7", "培训": "#DDA0DD",
    "差旅": "#98D8C8", "医疗": "#F7DC6F", "租赁": "#BB8FCE",
    "维修": "#85C1E9", "其他": "#B0BEC5",
}

CATEGORY_ICONS = {
    "餐饮": "🍽️", "交通": "🚗", "住宿": "🏨", "办公": "💼",
    "通讯": "📞", "培训": "📚", "差旅": "✈️", "医疗": "💊",
    "租赁": "🏠", "维修": "🔧", "其他": "📋",
}

STATUS_LABELS = {
    "pending": "待报销", "approved": "已审批",
    "rejected": "已驳回", "reimbursed": "已报销"
}

STATUS_COLORS = {
    "pending": "#FFA726", "approved": "#66BB6A",
    "rejected": "#EF5350", "reimbursed": "#42A5F5"
}

# HTML模板 (使用 __PLACEHOLDER__ 避免 f-string 与 JS ${} 冲突)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; color: #333; }
.container { max-width: 1400px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 16px; margin-bottom: 24px; }
.header h1 { font-size: 28px; margin-bottom: 8px; }
.header .subtitle { opacity: 0.9; font-size: 14px; }
.header .stats { display: flex; gap: 40px; margin-top: 20px; }
.header .stat-item { text-align: center; }
.header .stat-value { font-size: 32px; font-weight: bold; }
.header .stat-label { font-size: 12px; opacity: 0.8; margin-top: 4px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
.card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.card h3 { font-size: 16px; margin-bottom: 16px; color: #555; display: flex; align-items: center; gap: 8px; }
.card h3 .icon { font-size: 20px; }
.chart-container { position: relative; height: 280px; }
.full-width { grid-column: 1/-1; }
.toolbar { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; align-items: center; }
.toolbar button { padding: 8px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.toolbar button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.btn-generate { background: #667eea; color: white; }
.btn-export { background: #4CAF50; color: white; }
.btn-select-all { background: #f0f0f0; color: #555; }
.btn-approve { background: #FF9800; color: white; }
.btn-delete { background: #ef5350; color: white; }
.filter-select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; }
.search-box { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; width: 200px; }
.summary-bar { background: white; border-radius: 12px; padding: 16px 24px; margin-bottom: 16px; display: flex; gap: 30px; align-items: center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.summary-bar .total { font-size: 24px; font-weight: bold; color: #667eea; }
.summary-bar .count { font-size: 14px; color: #888; }
table { width: 100%; border-collapse: collapse; }
th { background: #f8f9fc; padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #666; border-bottom: 2px solid #e8e8e8; }
td { padding: 12px; font-size: 14px; border-bottom: 1px solid #f0f0f0; }
tr:hover { background: #f8f9ff; }
.amount { font-weight: 600; color: #333; font-family: 'SF Mono', 'Consolas', monospace; }
.status-badge { color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
.invoice-check { width: 18px; height: 18px; cursor: pointer; }
.reimburse-panel { display: none; background: white; border-radius: 12px; padding: 24px; margin-top: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.reimburse-panel.show { display: block; }
.reimburse-panel h3 { margin-bottom: 16px; }
.reimburse-items { max-height: 300px; overflow-y: auto; margin-bottom: 20px; }
.reimburse-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.reimburse-total { font-size: 20px; font-weight: bold; color: #667eea; text-align: right; padding: 16px 0; border-top: 2px solid #667eea; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 13px; color: #666; margin-bottom: 4px; }
.form-group input, .form-group textarea { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; }
.form-group textarea { height: 80px; resize: vertical; }
.toast { position: fixed; top: 20px; right: 20px; padding: 12px 24px; border-radius: 8px; color: white; font-weight: 500; z-index: 1000; animation: slideIn 0.3s; }
.toast.success { background: #4CAF50; }
.toast.error { background: #ef5350; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@media (max-width: 768px) {
    .grid { grid-template-columns: 1fr; }
    .header .stats { flex-wrap: wrap; gap: 20px; }
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🧾 __TITLE__</h1>
        <div class="subtitle">生成时间: __GEN_TIME__ | 数据来源: 本地数据库</div>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">__TOTAL_COUNT__</div>
                <div class="stat-label">发票总数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">¥__TOTAL_AMOUNT__</div>
                <div class="stat-label">总金额</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">__CAT_COUNT__</div>
                <div class="stat-label">费用类别</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">__PENDING_COUNT__</div>
                <div class="stat-label">待报销</div>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="card">
            <h3><span class="icon">📊</span>费用类别分布</h3>
            <div class="chart-container"><canvas id="categoryChart"></canvas></div>
        </div>
        <div class="card">
            <h3><span class="icon">📈</span>月度趋势</h3>
            <div class="chart-container"><canvas id="monthChart"></canvas></div>
        </div>
        <div class="card">
            <h3><span class="icon">🍩</span>类别占比</h3>
            <div class="chart-container"><canvas id="donutChart"></canvas></div>
        </div>
        <div class="card">
            <h3><span class="icon">📋</span>报销状态</h3>
            <div class="chart-container"><canvas id="statusChart"></canvas></div>
        </div>
    </div>
    <div class="card full-width">
        <h3><span class="icon">📝</span>发票清单</h3>
        <div class="summary-bar">
            <span class="count">选中: <strong id="selected-count">0</strong> 张</span>
            <span class="total">合计: <strong id="selected-total">¥0.00</strong></span>
        </div>
        <div class="toolbar">
            <button class="btn-select-all" onclick="toggleSelectAll()">☑️ 全选/取消</button>
            <button class="btn-generate" onclick="showReimbursePanel()">📋 生成报销单</button>
            <button class="btn-export" onclick="exportCSV()">📥 导出CSV</button>
            <button class="btn-approve" onclick="batchUpdateStatus('approved')">✅ 批量标记已审批</button>
            <select class="filter-select" onchange="filterByCategory(this.value)">
                <option value="">所有类别</option>
                __CAT_OPTIONS__
            </select>
            <select class="filter-select" onchange="filterByStatus(this.value)">
                <option value="">所有状态</option>
                <option value="pending">待报销</option>
                <option value="approved">已审批</option>
                <option value="reimbursed">已报销</option>
            </select>
            <input class="search-box" placeholder="🔍 搜索..." oninput="searchInvoices(this.value)">
        </div>
        <div style="overflow-x: auto;">
            <table>
                <thead><tr><th>选</th><th>ID</th><th>日期</th><th>类别</th><th>发票类型</th><th>金额</th><th>销售方</th><th>状态</th></tr></thead>
                <tbody id="invoice-tbody">
                    __TABLE_ROWS__
                </tbody>
            </table>
        </div>
    </div>
    <div class="reimburse-panel" id="reimburse-panel">
        <h3>📋 生成报销单</h3>
        <div class="reimburse-items" id="reimburse-items"></div>
        <div class="reimburse-total" id="reimburse-total">合计: ¥0.00</div>
        <div class="form-group">
            <label>报销事由</label>
            <input type="text" id="reimburse-reason" placeholder="如：6月差旅费报销">
        </div>
        <div class="form-group">
            <label>备注</label>
            <textarea id="reimburse-notes" placeholder="补充说明..."></textarea>
        </div>
        <div style="display: flex; gap: 12px;">
            <button class="btn-generate" onclick="generateReimburseDoc()">📄 生成报销单</button>
            <button class="btn-approve" onclick="markReimbursed()">💰 标记已报销</button>
            <button style="background:#888;color:white;padding:8px 20px;border:none;border-radius:8px;cursor:pointer;" onclick="hideReimbursePanel()">取消</button>
        </div>
    </div>
</div>
<script>
var invoices = __INVOICES_JSON__;
var catLabels = __CAT_LABELS__;
var catAmounts = __CAT_AMOUNTS__;
var catColorsData = __CAT_COLORS__;
var monthLabels = __MONTH_LABELS__;
var monthAmounts = __MONTH_AMOUNTS__;
var statusLabelsData = __STATUS_LABELS__;
var statusCounts = __STATUS_COUNTS__;
var statusColorsData = __STATUS_COLORS__;
var CATEGORY_ICONS = __CATEGORY_ICONS_JSON__;

new Chart(document.getElementById('categoryChart'), {
    type: 'bar',
    data: {
        labels: catLabels,
        datasets: [{
            label: '金额 (¥)',
            data: catAmounts,
            backgroundColor: catColorsData,
            borderRadius: 8, borderWidth: 0,
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { callback: function(v) { return '¥' + v.toLocaleString(); } } } }
    }
});

new Chart(document.getElementById('monthChart'), {
    type: 'line',
    data: {
        labels: monthLabels,
        datasets: [{
            label: '月度金额', data: monthAmounts,
            borderColor: '#667eea', backgroundColor: 'rgba(102,126,234,0.1)',
            fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#667eea',
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { callback: function(v) { return '¥' + v.toLocaleString(); } } } }
    }
});

new Chart(document.getElementById('donutChart'), {
    type: 'doughnut',
    data: {
        labels: catLabels,
        datasets: [{ data: catAmounts, backgroundColor: catColorsData, borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'right', labels: { padding: 15, usePointStyle: true } } }
    }
});

new Chart(document.getElementById('statusChart'), {
    type: 'pie',
    data: {
        labels: statusLabelsData,
        datasets: [{ data: statusCounts, backgroundColor: statusColorsData, borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'right', labels: { padding: 15, usePointStyle: true } } }
    }
});

function updateSelection() {
    var checks = document.querySelectorAll('.invoice-check:checked');
    var total = 0;
    checks.forEach(function(c) { total += parseFloat(c.dataset.amount); });
    document.getElementById('selected-count').textContent = checks.length;
    document.getElementById('selected-total').textContent = '¥' + total.toLocaleString('zh-CN', {minimumFractionDigits: 2});
}

document.querySelectorAll('.invoice-check').forEach(function(cb) {
    cb.addEventListener('change', updateSelection);
});

function toggleSelectAll() {
    var all = document.querySelectorAll('.invoice-check');
    var anyUnchecked = Array.from(all).some(function(c) { return !c.checked; });
    all.forEach(function(c) { c.checked = anyUnchecked; });
    updateSelection();
}

function filterByCategory(cat) {
    document.querySelectorAll('.invoice-row').forEach(function(row) {
        var inv = invoices.find(function(i) { return i.id == row.dataset.id; });
        row.style.display = (!cat || (inv && inv.category === cat)) ? '' : 'none';
    });
}

function filterByStatus(status) {
    document.querySelectorAll('.invoice-row').forEach(function(row) {
        row.style.display = (!status || row.dataset.status === status) ? '' : 'none';
    });
}

function searchInvoices(query) {
    var q = query.toLowerCase();
    document.querySelectorAll('.invoice-row').forEach(function(row) {
        var inv = invoices.find(function(i) { return i.id == row.dataset.id; });
        if (!inv) return;
        var match = inv.seller_name.toLowerCase().indexOf(q) >= 0 ||
                    inv.invoice_number.toLowerCase().indexOf(q) >= 0 ||
                    inv.category.toLowerCase().indexOf(q) >= 0 ||
                    inv.notes.toLowerCase().indexOf(q) >= 0;
        row.style.display = (!q || match) ? '' : 'none';
    });
}

function showReimbursePanel() {
    var checks = document.querySelectorAll('.invoice-check:checked');
    if (checks.length === 0) { showToast('请先勾选要报销的发票', 'error'); return; }
    var panel = document.getElementById('reimburse-panel');
    var itemsDiv = document.getElementById('reimburse-items');
    var total = 0;
    itemsDiv.innerHTML = '';
    checks.forEach(function(c) {
        var inv = invoices.find(function(i) { return i.id == parseInt(c.dataset.id); });
        if (!inv) return;
        total += inv.total_amount;
        var icon = CATEGORY_ICONS[inv.category] || '📋';
        itemsDiv.innerHTML += '<div class="reimburse-item">' +
            '<span>' + icon + ' ' + inv.invoice_date + ' | ' + inv.category + ' | ' + (inv.seller_name||'').substring(0,20) + '</span>' +
            '<span class="amount">¥' + inv.total_amount.toLocaleString('zh-CN', {minimumFractionDigits: 2}) + '</span></div>';
    });
    document.getElementById('reimburse-total').textContent = '合计: ¥' + total.toLocaleString('zh-CN', {minimumFractionDigits: 2});
    panel.classList.add('show');
}

function hideReimbursePanel() {
    document.getElementById('reimburse-panel').classList.remove('show');
}

function getSelectedIds() {
    return Array.from(document.querySelectorAll('.invoice-check:checked')).map(function(c) { return parseInt(c.dataset.id); });
}

function generateReimburseDoc() {
    var ids = getSelectedIds();
    var reason = document.getElementById('reimburse-reason').value || '费用报销';
    var notes = document.getElementById('reimburse-notes').value || '';
    var selectedInvoices = invoices.filter(function(i) { return ids.indexOf(i.id) >= 0; });
    var total = selectedInvoices.reduce(function(s,i) { return s + i.total_amount; }, 0);
    var itemsHtml = selectedInvoices.map(function(i) {
        var icon = CATEGORY_ICONS[i.category] || '📋';
        return '<tr><td>' + i.invoice_date + '</td><td>' + icon + ' ' + i.category +
               '</td><td>' + i.invoice_number + '</td><td>' + (i.seller_name||'') +
               '</td><td class="amount">¥' + i.total_amount.toFixed(2) + '</td></tr>';
    }).join('');
    var notesHtml = notes ? '<p style="font-size:14px;margin-top:16px;">备注: ' + notes + '</p>' : '';
    var doc = window.open('', '_blank', 'width=800,height=600');
    doc.document.write('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>报销单</title>' +
    '<style>body{font-family:SimSun,serif;padding:40px;max-width:800px;margin:0 auto;}h1{text-align:center;font-size:24px;margin-bottom:20px;}' +
    '.info{display:flex;justify-content:space-between;margin-bottom:16px;font-size:14px;}.info span{display:inline-block;min-width:200px;}' +
    'table{width:100%;border-collapse:collapse;margin:16px 0;}th,td{border:1px solid #333;padding:8px;font-size:14px;text-align:left;}' +
    'th{background:#f0f0f0;}.amount{text-align:right;}.total{text-align:right;font-size:16px;font-weight:bold;margin-top:8px;}' +
    '.sign{display:flex;justify-content:space-between;margin-top:60px;font-size:14px;}.sign div{text-align:center;}' +
    '@media print{body{padding:20px;}}</style></head><body>' +
    '<h1>费 用 报 销 单</h1>' +
    '<div class="info"><span>报销事由: ' + reason + '</span><span>日期: ' + new Date().toLocaleDateString('zh-CN') + '</span></div>' +
    '<table><thead><tr><th>日期</th><th>类别</th><th>发票号</th><th>销售方</th><th>金额</th></tr></thead><tbody>' +
    itemsHtml + '</tbody></table>' +
    '<div class="total">合计金额: ¥' + total.toFixed(2) + ' (共' + selectedInvoices.length + '张)</div>' +
    notesHtml +
    '<div class="sign"><div>报销人:<br><br></div><div>审批人:<br><br></div><div>财务:<br><br></div></div>' +
    '<script>setTimeout(function(){print();},300);</' + 'script></body></html>');
    doc.document.close();
    showToast('报销单已生成！合计 ¥' + total.toFixed(2), 'success');
}

function markReimbursed() {
    var ids = getSelectedIds();
    if (ids.length === 0) return;
    batchUpdateStatus('reimbursed');
    hideReimbursePanel();
}

function batchUpdateStatus(status) {
    var ids = getSelectedIds();
    if (ids.length === 0) { showToast('请先勾选发票', 'error'); return; }
    showToast('正在更新 ' + ids.length + ' 张发票状态...', 'success');
}

function exportCSV() {
    var ids = getSelectedIds();
    var selectedInvoices = ids.length > 0 ? invoices.filter(function(i) { return ids.indexOf(i.id) >= 0; }) : invoices;
    var csv = 'ID,发票代码,发票号码,日期,类型,类别,金额,税额,价税合计,销售方,状态\\n';
    selectedInvoices.forEach(function(i) {
        csv += i.id + ',' + i.invoice_code + ',' + i.invoice_number + ',' + i.invoice_date + ',' +
               i.invoice_type + ',' + i.category + ',' + i.amount + ',' + i.tax_amount + ',' +
               i.total_amount + ',"' + (i.seller_name||'') + '",' + i.status + '\\n';
    });
    var blob = new Blob(['\\ufeff' + csv], {type: 'text/csv;charset=utf-8;'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = '报销明细_' + new Date().toISOString().slice(0,10) + '.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast('CSV导出成功！', 'success');
}

function showToast(msg, type) {
    var toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 3000);
}

updateSelection();
</script>
</body>
</html>"""


def generate_html_report(month: str = None, output_path: str = None) -> str:
    """生成交互式HTML报销报告"""
    summary = get_summary(month)
    filters = {"limit": 500}
    if month:
        filters["month"] = month
    invoices = list_invoices(filters)

    title = f"发票报销报告 - {month}" if month else "发票报销报告 - 全部"

    cat_data = summary["by_category"]
    pending_count = len([i for i in invoices if i['status'] == 'pending'])

    # 表格行
    table_rows = ""
    for inv in invoices:
        cat_icon = CATEGORY_ICONS.get(inv["category"], "📋")
        status_label = STATUS_LABELS.get(inv["status"], inv["status"])
        status_color = STATUS_COLORS.get(inv["status"], "#B0BEC5")
        table_rows += f"""<tr class="invoice-row" data-id="{inv['id']}" data-status="{inv['status']}">
            <td><input type="checkbox" class="invoice-check" data-id="{inv['id']}" data-amount="{inv['total_amount']}"></td>
            <td>{inv['id']}</td><td>{inv['invoice_date']}</td>
            <td>{cat_icon} {inv['category']}</td><td>{inv['invoice_type'][:10]}</td>
            <td class="amount">¥{inv['total_amount']:,.2f}</td>
            <td>{inv['seller_name'][:15]}</td>
            <td><span class="status-badge" style="background:{status_color}">{status_label}</span></td>
        </tr>"""

    # 类别筛选选项
    cat_options = "".join(
        f'<option value="{c["category"]}">{CATEGORY_ICONS.get(c["category"],"")} {c["category"]} ({c["count"]})</option>'
        for c in cat_data
    )

    # 替换模板
    html = HTML_TEMPLATE
    replacements = {
        "__TITLE__": title,
        "__GEN_TIME__": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "__TOTAL_COUNT__": str(summary["total_count"]),
        "__TOTAL_AMOUNT__": f"{summary['total_amount']:,.2f}",
        "__CAT_COUNT__": str(len(cat_data)),
        "__PENDING_COUNT__": str(pending_count),
        "__TABLE_ROWS__": table_rows,
        "__CAT_OPTIONS__": cat_options,
        "__INVOICES_JSON__": json.dumps(invoices, ensure_ascii=False, default=str),
        "__CAT_LABELS__": json.dumps([c["category"] for c in cat_data], ensure_ascii=False),
        "__CAT_AMOUNTS__": json.dumps([c["total"] for c in cat_data]),
        "__CAT_COLORS__": json.dumps([CATEGORY_COLORS.get(c["category"], "#B0BEC5") for c in cat_data]),
        "__MONTH_LABELS__": json.dumps([m["month"] for m in summary["by_month"]], ensure_ascii=False),
        "__MONTH_AMOUNTS__": json.dumps([m["total"] for m in summary["by_month"]]),
        "__STATUS_LABELS__": json.dumps([STATUS_LABELS.get(s["status"], s["status"]) for s in summary["by_status"]], ensure_ascii=False),
        "__STATUS_COUNTS__": json.dumps([s["count"] for s in summary["by_status"]]),
        "__STATUS_COLORS__": json.dumps([STATUS_COLORS.get(s["status"], "#B0BEC5") for s in summary["by_status"]]),
        "__CATEGORY_ICONS_JSON__": json.dumps(CATEGORY_ICONS, ensure_ascii=False),
    }

    for key, value in replacements.items():
        html = html.replace(key, value)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    return html


def generate_simple_report(month: str = None) -> str:
    """生成纯文本报销摘要"""
    summary = get_summary(month)

    lines = [
        "=" * 60,
        f"  发票报销汇总 - {month if month else '全部记录'}",
        f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        f"  发票总数: {summary['total_count']} 张",
        f"  总金额:   ¥{summary['total_amount']:,.2f}",
        "",
        "  按类别统计:",
        "  " + "-" * 50,
    ]
    for cat in summary["by_category"]:
        icon = CATEGORY_ICONS.get(cat["category"], "📋")
        bar_len = min(int(cat["total"] / max(summary["total_amount"], 1) * 30), 30)
        bar = "█" * bar_len
        lines.append(f"  {icon} {cat['category']:4}  {cat['count']:3}张  ¥{cat['total']:>10,.2f}  {bar}")
    lines.extend(["", "  按月趋势:", "  " + "-" * 50])
    for m in summary["by_month"]:
        lines.append(f"  {m['month']}  {m['count']:3}张  ¥{m['total']:>10,.2f}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="发票报销报告生成器")
    parser.add_argument("--month", default="", help="指定月份 YYYY-MM")
    parser.add_argument("--output", default="", help="输出HTML文件路径")
    parser.add_argument("--text", action="store_true", help="输出纯文本摘要")

    args = parser.parse_args()
    month = args.month or None

    if args.text:
        print(generate_simple_report(month))
    else:
        output_path = args.output or None
        result = generate_html_report(month, output_path)
        if output_path:
            print(f"✅ 报告已生成: {output_path}")
        else:
            print(result)


if __name__ == "__main__":
    main()
