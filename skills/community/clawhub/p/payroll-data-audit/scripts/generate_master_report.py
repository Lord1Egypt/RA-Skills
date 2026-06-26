#!/usr/bin/env python3
"""
生成总审核报告（Master Report）
将数据扫描、审核结果、判定过程、问题清单、抽样校验等聚合为一份完整的 HTML 报告。
"""
import json
import sys
from pathlib import Path
from datetime import datetime


def generate_master_report(audit_result_path: str, scan_path: str,
                           issue_path: str, sampling_path: str,
                           output_path: str) -> dict:
    """生成总审核报告。"""
    # 读取所有输入
    with open(audit_result_path) as f:
        audit = json.load(f)
    scan = {}
    if Path(scan_path).exists():
        with open(scan_path) as f:
            scan = json.load(f)
    issues = []
    if Path(issue_path).exists():
        with open(issue_path) as f:
            content = f.read()
            # 简单解析问题清单
            for line in content.split('\n'):
                if line.startswith('| ') and '员工' in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 5:
                        issues.append({
                            'severity': parts[1],
                            'rule': parts[2],
                            'detail': parts[3],
                            'suggestion': parts[4],
                        })

    sampling = {}
    if Path(sampling_path).exists():
        with open(sampling_path) as f:
            sampling = json.load(f)

    summary = audit.get('summary', {})

    # 计算各线触发人数
    red_count = sum(r.get('triggered', 0) for r in audit.get('red_lines', {}).get('rule_results', []))
    yellow_count = sum(r.get('triggered', 0) for r in audit.get('yellow_lines', {}).get('rule_results', []))
    blue_count = sum(r.get('triggered', 0) for r in audit.get('blue_lines', {}).get('rule_results', []))
    total = audit.get('total_records', 0)

    # 判定结论
    overall = "✅ 审核通过" if red_count == 0 else "🔴 存在红线异常，禁止出报告"

    html = _build_html(audit, scan, issues, sampling, total, red_count, yellow_count, blue_count, overall)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return {
        'output_path': str(output_path),
        'total_records': total,
        'red_count': red_count,
        'yellow_count': yellow_count,
        'overall': overall,
    }


def _build_html(audit, scan, issues, sampling, total, red_count, yellow_count, blue_count, overall):
    """构建 HTML 总报告。"""
    summary = audit.get('summary', {})

    html_parts = ["""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工资审核总报告</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f5f5; color: #1f2937; line-height: 1.6; padding: 20px; }
.container { max-width: 1200px; margin: 0 auto; }
.cover { background: linear-gradient(135deg, #1e3a5f, #2563eb); color: white; padding: 60px 40px; border-radius: 12px; margin-bottom: 24px; }
.cover h1 { font-size: 32px; margin-bottom: 8px; }
.cover .subtitle { font-size: 16px; opacity: 0.9; }
.cover .meta { margin-top: 20px; display: flex; gap: 40px; }
.cover .meta-item { font-size: 14px; }
.cover .meta-item span { opacity: 0.7; }
.section { background: white; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.section h2 { font-size: 20px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #e5e7eb; }
.section h3 { font-size: 16px; margin: 20px 0 12px; color: #374151; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { padding: 20px; border-radius: 8px; text-align: center; }
.stat-card.red { background: #fef2f2; border: 1px solid #fecaca; }
.stat-card.yellow { background: #fffbeb; border: 1px solid #fde68a; }
.stat-card.blue { background: #eff6ff; border: 1px solid #bfdbfe; }
.stat-card.green { background: #f0fdf4; border: 1px solid #bbf7d0; }
.stat-card .value { font-size: 36px; font-weight: 700; }
.stat-card .label { font-size: 13px; color: #6b7280; margin-top: 4px; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; font-size: 14px; }
th { background: #f9fafb; font-weight: 600; color: #374151; }
tr:hover { background: #f9fafb; }
.judgment-block { background: #f9fafb; border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 4px solid #e5e7eb; }
.judgment-block.red { border-left-color: #dc2626; }
.judgment-block.yellow { border-left-color: #f59e0b; }
.judgment-block.green { border-left-color: #22c55e; }
.judgment-block h4 { font-size: 15px; margin-bottom: 8px; }
.judgment-block .logic { font-size: 13px; color: #6b7280; margin-bottom: 8px; }
.judgment-block .stats { display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; }
.judgment-block .stats span { background: #e5e7eb; padding: 2px 8px; border-radius: 4px; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
.badge.red { background: #fecaca; color: #991b1b; }
.badge.yellow { background: #fde68a; color: #92400e; }
.badge.green { background: #bbf7d0; color: #166534; }
.overall-badge { display: inline-block; padding: 8px 20px; border-radius: 8px; font-size: 18px; font-weight: 700; margin: 16px 0; }
.overall-badge.pass { background: #f0fdf4; color: #166534; border: 2px solid #86efac; }
.overall-badge.fail { background: #fef2f2; color: #991b1b; border: 2px solid #fca5a5; }
.exclusion-list { display: flex; gap: 8px; flex-wrap: wrap; margin: 8px 0; }
.exclusion-item { background: #f3f4f6; padding: 4px 10px; border-radius: 6px; font-size: 12px; }
.toc { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; margin: 20px 0; }
.toc-item { padding: 16px; background: #f9fafb; border-radius: 8px; cursor: pointer; }
.toc-item:hover { background: #e5e7eb; }
.toc-item h4 { font-size: 14px; margin-bottom: 4px; }
.toc-item p { font-size: 12px; color: #6b7280; }
</style>
</head>
<body>
<div class="container">
"""]

    # ─── 封面 ───
    html_parts.append(f"""
<div class="cover">
<h1>📋 工资审核总报告</h1>
<div class="subtitle">payroll-data-audit v6.1.0</div>
<div class="meta">
<div class="meta-item"><span>审核时间：</span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
<div class="meta-item"><span>数据量：</span>{total} 人</div>
<div class="meta-item"><span>规则版本：</span>{summary.get('rules_version', 'N/A')}</div>
</div>
</div>
""")

    # ─── 目录 ───
    html_parts.append("""
<div class="section">
<h2>📑 目录</h2>
<div class="toc">
<div class="toc-item" onclick="document.getElementById('s1').scrollIntoView({behavior:'smooth'})">
<h4>1. 审核结论</h4>
<p>总体判定 + 核心指标</p>
</div>
<div class="toc-item" onclick="document.getElementById('s2').scrollIntoView({behavior:'smooth'})">
<h4>2. 数据扫描</h4>
<p>数据概览 + 本月变动</p>
</div>
<div class="toc-item" onclick="document.getElementById('s3').scrollIntoView({behavior:'smooth'})">
<h4>3. 审核汇总表</h4>
<p>全维度规则检查结果</p>
</div>
<div class="toc-item" onclick="document.getElementById('s4').scrollIntoView({behavior:'smooth'})">
<h4>4. 判定过程详解</h4>
<p>每条规则的逻辑、排除、判定</p>
</div>
<div class="toc-item" onclick="document.getElementById('s5').scrollIntoView({behavior:'smooth'})">
<h4>5. 问题清单</h4>
<p>需逐项核实的异常项</p>
</div>
<div class="toc-item" onclick="document.getElementById('s6').scrollIntoView({behavior:'smooth'})">
<h4>6. 抽样校验</h4>
<p>数据准确性验证</p>
</div>
</div>
</div>
""")

    # ─── 1. 审核结论 ───
    is_pass = red_count == 0
    badge_class = "pass" if is_pass else "fail"
    html_parts.append(f"""
<div class="section" id="s1">
<h2>1. 审核结论</h2>
<div class="overall-badge {badge_class}">{overall}</div>
<div class="stats-grid">
<div class="stat-card green">
<div class="value">{total}</div>
<div class="label">检查总人数</div>
</div>
<div class="stat-card red">
<div class="value">{red_count}</div>
<div class="label">红线阻断</div>
</div>
<div class="stat-card yellow">
<div class="value">{yellow_count}</div>
<div class="label">黄线预警</div>
</div>
<div class="stat-card blue">
<div class="value">{blue_count}</div>
<div class="label">蓝线提示</div>
</div>
</div>
</div>
""")

    # ─── 2. 数据扫描 ───
    html_parts.append(f"""
<div class="section" id="s2">
<h2>2. 数据扫描</h2>
<table>
<tr><th>项目</th><th>值</th></tr>
<tr><td>发薪月</td><td>{scan.get('pay_month', 'N/A')}</td></tr>
<tr><td>公司主体</td><td>{', '.join(str(x) for x in scan.get('entities', []))}</td></tr>
<tr><td>总记录数</td><td>{scan.get('total_records', total)}</td></tr>
<tr><td>本月入职</td><td>{scan.get('new_hires', 'N/A')} 人</td></tr>
<tr><td>本月离职</td><td>{scan.get('departures', 'N/A')} 人</td></tr>
</table>
</div>
""")

    # ─── 3. 审核汇总表 ───
    rows = []
    for cat in ['red_lines', 'yellow_lines', 'blue_lines']:
        for r in audit.get(cat, {}).get('rule_results', []):
            j = r.get('judgment', {})
            chk = j.get('actually_checked', r.get('total_checked', total))
            triggered = j.get('triggered', r.get('triggered', 0))
            passed = r.get('passed', triggered == 0)
            rate = j.get('pass_rate', f"{(chk - triggered) / max(chk, 1) * 100:.1f}%")
            if cat == 'red_lines':
                status = '🔴 阻断' if not passed else '✅ 通过'
            elif cat == 'yellow_lines':
                status = '🟠 异常' if not passed else '✅ 通过'
            else:
                status = '🔵 提示' if not passed else '✅ 通过'
            rows.append((r.get('rule_id', ''), r.get('rule_name', ''), chk, chk - triggered, triggered, rate, status))

    rows_html = '\n'.join(f'<tr><td>{rid}</td><td>{rname}</td><td>{chk}</td><td>{passed}</td><td>{triggered}</td><td>{rate}</td><td>{status}</td></tr>'
                          for rid, rname, chk, passed, triggered, rate, status in rows)

    html_parts.append(f"""
<div class="section" id="s3">
<h2>3. 审核汇总表</h2>
<table>
<tr><th>规则ID</th><th>规则名称</th><th>检查数</th><th>通过数</th><th>异常数</th><th>通过率</th><th>结论</th></tr>
{rows_html}
</table>
</div>
""")

    # ─── 4. 判定过程详解 ───
    html_parts.append('<div class="section" id="s4">\n<h2>4. 判定过程详解</h2>\n')

    for cat_name, cat_label, color_class in [('red_lines', '🔴 红线', 'red'), ('yellow_lines', '🟠 黄线', 'yellow'), ('blue_lines', '🔵 蓝线', 'green')]:
        cat = audit.get(cat_name, {})
        html_parts.append(f'<h3>{cat_label}</h3>\n')
        for r in cat.get('rule_results', []):
            j = r.get('judgment', {})
            passed = r.get('passed', True)
            triggered = j.get('triggered', 0)
            total_rec = j.get('total_records', 0)
            excluded = j.get('exclusion_count', 0)
            checked = j.get('actually_checked', total_rec)
            pass_rate = j.get('pass_rate', 'N/A')
            verdict = j.get('verdict', 'N/A')
            logic = j.get('rule_logic', '')

            ex = j.get('excluded_reasons', {})
            ex_html = ''
            if ex:
                ex_html = '<div class="exclusion-list">' + ''.join(
                    f'<span class="exclusion-item">{k}: {v}人</span>' for k, v in ex.items()
                ) + '</div>'

            details_html = ''
            if r.get('details'):
                names = ', '.join(d['姓名代号'] + '(' + d.get('工号', '') + ')' for d in r['details'][:10])
                details_html = f'<div style="margin-top:8px;font-size:13px;color:#6b7280;">触发人员: {names}</div>'

            block_class = 'green' if passed else color_class
            badge_cls = 'green' if passed else color_class
            status_text = '✅ 通过' if passed else f'{"🔴 阻断" if color_class == "red" else "🟠 异常"}'

            html_parts.append(f"""
<div class="judgment-block {block_class}">
<h4>{r['rule_id']} {r['rule_name']} <span class="badge {badge_cls}">{status_text}</span></h4>
<div class="logic">{logic}</div>
<div class="stats">
<span>总人数: {total_rec}</span>
<span>排除: {excluded}</span>
<span>实际检查: {checked}</span>
<span>触发: {triggered}</span>
<span>通过率: {pass_rate}</span>
<span>判定: {verdict}</span>
</div>
{ex_html}
{details_html}
</div>
""")

    html_parts.append('</div>\n')

    # ─── 5. 问题清单 ───
    issue_rows = ''
    for i, issue in enumerate(issues, 1):
        sev = issue.get('severity', '')
        rule = issue.get('rule', '')
        detail = issue.get('detail', '')
        suggestion = issue.get('suggestion', '')
        icon = '🔴' if 'P0' in sev else '🟠'
        issue_rows += f'<tr><td>{i}</td><td>{icon} {sev}</td><td>{rule}</td><td>{detail}</td><td>{suggestion}</td></tr>\n'

    html_parts.append(f"""
<div class="section" id="s5">
<h2>5. 问题清单（{len(issues)} 项）</h2>
<table>
<tr><th>序号</th><th>严重级别</th><th>问题</th><th>详情</th><th>建议行动</th></tr>
{issue_rows}
</table>
</div>
""")

    # ─── 6. 抽样校验 ───
    sample_size = sampling.get('sample_size', 'N/A')
    total_records = sampling.get('total_records', 'N/A')
    deviation = sampling.get('deviation_rate', 'N/A')
    status = sampling.get('status', 'N/A')

    html_parts.append(f"""
<div class="section" id="s6">
<h2>6. 抽样校验</h2>
<table>
<tr><th>项目</th><th>值</th></tr>
<tr><td>抽样数</td><td>{sample_size} / {total_records}</td></tr>
<tr><td>偏差率</td><td>{deviation}%</td></tr>
<tr><td>状态</td><td>{status}</td></tr>
</table>
</div>
""")

    html_parts.append('</div>\n</body>\n</html>')

    return '\n'.join(html_parts)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='生成总审核报告')
    parser.add_argument('--audit-result', required=True, help='audit_result.json 路径')
    parser.add_argument('--scan', default='', help='data_scan.json 路径')
    parser.add_argument('--issues', default='', help='issue_report.md 路径')
    parser.add_argument('--sampling', default='', help='sampling_verify.json 路径')
    parser.add_argument('--output', required=True, help='输出路径')
    args = parser.parse_args()

    result = generate_master_report(
        args.audit_result,
        args.scan,
        args.issues,
        args.sampling,
        args.output,
    )
    print(f"✅ 总审核报告已生成: {result['output_path']}")
    print(f"   总人数: {result['total_records']}, 红线: {result['red_count']}, 黄线: {result['yellow_count']}")
    print(f"   结论: {result['overall']}")
