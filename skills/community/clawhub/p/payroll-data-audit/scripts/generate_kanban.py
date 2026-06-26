#!/usr/bin/env python3
"""
Payroll Audit Kanban Generator - 审核清单看板生成器 v5.3

输入: rules_engine.py 输出的 audit_result.json + rules.json
输出: HTML 审核清单看板 / Markdown 审核清单看板

看板特性:
- 展开 rules.json 所有审核条目为完整清单
- 每条绑定审核结果 + 数据依据
- 颜色标识: ✅通过 / 🟠异常 / 🔴阻断
- 支持飞书文档导入

用法:
    python3 scripts/generate_kanban.py --input /tmp/audit_result.json --format html --output kanban.html
    python3 scripts/generate_kanban.py --input /tmp/audit_result.json --format markdown --output kanban.md
    python3 scripts/generate_kanban.py --input /tmp/audit_result.json --format both
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Data Loading & Normalization
# ---------------------------------------------------------------------------

def load_rules(rules_path=None):
    """加载 rules.json"""
    if rules_path is None:
        rules_dir = Path(__file__).parent
        if (rules_dir / "rules.json").exists():
            rules_path = rules_dir / "rules.json"
        else:
            rules_path = rules_dir.parent / "references" / "rules.json"
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_audit_result(input_path):
    """加载审核结果 JSON"""
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_kanban_items(rules, audit, link_template=None):
    """
    构建完整的审核清单看板条目列表。
    每条包含：类别、规则ID、审核条目、审核结果、检查数、通过数、异常数、通过率、数据依据、处理建议。
    """
    items = []
    total_records = audit.get("total_records", 0)

    # 1. 字段完整性
    field_check = audit.get("field_check", {})
    items.append({
        "category": "字段完整性",
        "rule_id": "FC-001",
        "name": "必填字段检查",
        "description": f"检查 {field_check.get('total_fields_checked', 0)} 个必填字段的完整性和格式",
        "status": "pass" if field_check.get("passed") else "fail",
        "checked": total_records,
        "passed": total_records if field_check.get("passed") else 0,
        "failed": 0 if field_check.get("passed") else len(field_check.get("missing", {})),
        "rate": "100%" if field_check.get("passed") else f"{(1 - len(field_check.get('missing', {})) / max(field_check.get('total_fields_checked', 1), 1)) * 100:.1f}%",
        "evidence": f"检查 {field_check.get('total_fields_checked', 0)} 个字段，" +
                    (f"全部完整且格式正确" if field_check.get("passed") else
                     f"缺失字段: {', '.join(field_check.get('missing', {}).keys())}"),
        "action": "补充缺失字段后重新审核" if not field_check.get("passed") else "无需操作",
    })

    # 2. 公式校验
    formula_check = audit.get("formula_check", {})
    for fr in formula_check.get("formula_results", []):
        passed = fr.get("passed", True)
        violations = fr.get("violation_count", 0)
        items.append({
            "category": "公式校验",
            "rule_id": fr.get("rule_id", ""),
            "name": fr.get("rule_name", ""),
            "description": fr.get("rule_name", ""),
            "status": "pass" if passed else "warning",
            "checked": fr.get("total_checked", total_records),
            "passed": fr.get("total_checked", total_records) - violations,
            "failed": violations,
            "rate": f"{((fr.get('total_checked', 1) - violations) / max(fr.get('total_checked', 1), 1)) * 100:.1f}%",
            "evidence": f"{fr.get('total_checked', 0)}条记录中" +
                        (f"全部通过，容差0.01元" if passed else
                         f"{violations}条公式计算偏差超出容差"),
            "action": _format_violation_action(fr.get("violations", []), link_template=link_template) if not passed else "无需操作",
        })

    # 3. 业务规则
    business_check = audit.get("business_check", {})
    for br in business_check.get("rule_results", []):
        passed = br.get("passed", True)
        triggered = br.get("triggered", 0)
        items.append({
            "category": "业务规则",
            "rule_id": br.get("rule_id", ""),
            "name": br.get("rule_name", ""),
            "description": br.get("rule_name", ""),
            "status": "pass" if passed else "warning",
            "checked": br.get("total_checked", total_records),
            "passed": br.get("total_checked", total_records) - triggered,
            "failed": triggered,
            "rate": f"{((br.get('total_checked', 1) - triggered) / max(br.get('total_checked', 1), 1)) * 100:.1f}%",
            "evidence": f"{br.get('total_checked', 0)}条记录中" +
                        (f"全部符合业务规则" if passed else
                         f"{triggered}条触发业务规则异常"),
            "action": _format_violation_action(br.get("details", []), link_template=link_template) if not passed else "无需操作",
        })

    # 4. 红线
    red_check = audit.get("red_lines", {})
    for rl in red_check.get("rule_results", []):
        triggered = rl.get("triggered", 0)
        passed = triggered == 0
        items.append({
            "category": "红线",
            "rule_id": rl.get("rule_id", ""),
            "name": rl.get("name", ""),
            "description": rl.get("name", ""),
            "status": "pass" if passed else "block",
            "checked": rl.get("total_checked", total_records),
            "passed": rl.get("total_checked", total_records) - triggered,
            "failed": triggered,
            "rate": f"{((rl.get('total_checked', 1) - triggered) / max(rl.get('total_checked', 1), 1)) * 100:.1f}%",
            "evidence": f"{rl.get('total_checked', 0)}条记录中" +
                        (f"全部通过红线校验" if passed else
                         f"{triggered}条触发红线（严重违规）"),
            "action": _format_violation_action(rl.get("details", []), is_red=True, link_template=link_template) if not passed else "无需操作",
        })

    # 5. 黄线
    yellow_check = audit.get("yellow_lines", {})
    for yl in yellow_check.get("rule_results", []):
        triggered = yl.get("triggered", 0)
        passed = triggered == 0
        items.append({
            "category": "黄线",
            "rule_id": yl.get("rule_id", ""),
            "name": yl.get("name", ""),
            "description": yl.get("name", ""),
            "status": "pass" if passed else "warning",
            "checked": yl.get("total_checked", total_records),
            "passed": yl.get("total_checked", total_records) - triggered,
            "failed": triggered,
            "rate": f"{((yl.get('total_checked', 1) - triggered) / max(yl.get('total_checked', 1), 1)) * 100:.1f}%",
            "evidence": f"{yl.get('total_checked', 0)}条记录中" +
                        (f"全部正常" if passed else
                         f"{triggered}条需核实"),
            "action": f"核实以下人员: {_format_violation_action(yl.get('details', []), link_template=link_template)}" if not passed else "无需操作",
        })

    # 6. 蓝线
    blue_check = audit.get("blue_lines", {})
    for bl in blue_check.get("rule_results", []):
        triggered = bl.get("triggered", 0)
        passed = triggered == 0
        items.append({
            "category": "蓝线",
            "rule_id": bl.get("rule_id", ""),
            "name": bl.get("name", ""),
            "description": bl.get("name", ""),
            "status": "pass" if passed else "note",
            "checked": bl.get("total_checked", total_records),
            "passed": bl.get("total_checked", total_records) - triggered,
            "failed": triggered,
            "rate": f"{((bl.get('total_checked', 1) - triggered) / max(bl.get('total_checked', 1), 1)) * 100:.1f}%",
            "evidence": f"{bl.get('total_checked', 0)}条记录中" +
                        (f"无异常波动" if passed else
                         f"{triggered}条有波动趋势（正常范围）"),
            "action": "关注趋势变化" if not passed else "无需操作",
        })

    # 7. 政策校验
    policy_check = audit.get("policy_check", {})
    for pol in policy_check.get("rule_results", []):
        triggered = pol.get("triggered", 0)
        total_checked = pol.get("total_checked", total_records)
        passed = triggered == 0
        items.append({
            "category": "政策校验",
            "rule_id": pol.get("rule_id", ""),
            "name": pol.get("name", ""),
            "description": pol.get("name", ""),
            "status": "pass" if passed else "warning",
            "checked": total_checked,
            "passed": total_checked - triggered,
            "failed": triggered,
            "rate": f"{((total_checked - triggered) / max(total_checked, 1)) * 100:.1f}%",
            "evidence": f"{total_checked}条记录中" +
                        (f"全部符合政策规定" if passed else
                         f"{triggered}条不符合豁免政策"),
            "action": f"核实以下人员: {_format_violation_action(pol.get('details', []), link_template=link_template)}" if not passed else "无需操作",
        })

    return items


def _format_violation_action(details, is_red=False, max_show=5, link_template=None):
    """格式化违规明细为行动建议，支持超链接复核"""
    if not details:
        return "无需操作"
    if isinstance(details, list) and len(details) > 0 and isinstance(details[0], dict):
        items = []
        for d in details[:max_show]:
            name = d.get("姓名代号", "")
            emp_id = d.get("工号", "")
            val = d.get("value", d.get("diff", ""))
            label = f"{name}({emp_id})" if name and emp_id else (name or emp_id or "未知")
            if val:
                label += f"={val}"

            # 超链接
            if link_template and emp_id:
                link = link_template.replace("{emp_id}", emp_id).replace("{emp_name}", name).replace("{row_index}", str(d.get("index", "")))
                items.append(f'<a href="{link}" target="_blank">{label}</a>')
            else:
                items.append(label)
        suffix = f" 等{len(details)}人" if len(details) > max_show else ""
        action_text = f"{'立即核实并修正' if is_red else '核实'}: {'; '.join(items)}{suffix}"
        return action_text
    return str(details)[:200]


# ---------------------------------------------------------------------------
# HTML Kanban Generator
# ---------------------------------------------------------------------------

def generate_html_kanban(items, audit, output_path=None):
    """生成 HTML 审核清单看板"""
    total = len(items)
    passed = sum(1 for i in items if i["status"] == "pass")
    warnings = sum(1 for i in items if i["status"] == "warning")
    blocks = sum(1 for i in items if i["status"] == "block")
    notes = sum(1 for i in items if i["status"] == "note")

    total_checked = sum(i["checked"] for i in items)
    total_failed = sum(i["failed"] for i in items)
    overall_rate = f"{((total_checked - total_failed) / max(total_checked, 1)) * 100:.1f}%"

    # Color mapping
    status_colors = {
        "pass": "#22c55e",
        "warning": "#f59e0b",
        "block": "#ef4444",
        "note": "#6366f1",
    }
    status_labels = {
        "pass": "✅ 通过",
        "warning": "🟠 异常",
        "block": "🔴 阻断",
        "note": "🔵 提示",
    }
    category_colors = {
        "字段完整性": "#3b82f6",
        "公式校验": "#8b5cf6",
        "业务规则": "#06b6d4",
        "红线": "#ef4444",
        "黄线": "#f59e0b",
        "蓝线": "#6366f1",
        "政策校验": "#10b981",
    }

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工资审核清单看板 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f8fafc; color: #1e293b; padding: 24px; }}
  .header {{ background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 32px; border-radius: 16px; margin-bottom: 24px; }}
  .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
  .header .meta {{ font-size: 14px; opacity: 0.85; }}
  .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); text-align: center; }}
  .card .number {{ font-size: 36px; font-weight: 700; margin-bottom: 4px; }}
  .card .label {{ font-size: 13px; color: #64748b; }}
  .card.pass .number {{ color: #22c55e; }}
  .card.warning .number {{ color: #f59e0b; }}
  .card.block .number {{ color: #ef4444; }}
  .card.note .number {{ color: #6366f1; }}
  .card.total .number {{ color: #1e40af; }}
  .card.rate .number {{ color: #059669; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px; }}
  th {{ background: #f1f5f9; padding: 12px 16px; text-align: left; font-size: 13px; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0; }}
  td {{ padding: 12px 16px; font-size: 13px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f8fafc; }}
  .status-badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; color: white; }}
  .status-pass {{ background: #22c55e; }}
  .status-warning {{ background: #f59e0b; }}
  .status-block {{ background: #ef4444; }}
  .status-note {{ background: #6366f1; }}
  .category-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; color: white; }}
  .rule-id {{ font-family: monospace; font-size: 12px; color: #94a3b8; }}
  .evidence {{ color: #475569; max-width: 300px; word-break: break-word; }}
  .action {{ color: #dc2626; font-weight: 500; max-width: 250px; word-break: break-word; }}
  .action-normal {{ color: #22c55e; }}
  .rate-bar {{ display: inline-block; width: 60px; height: 6px; background: #e2e8f0; border-radius: 3px; vertical-align: middle; margin-left: 6px; }}
  .rate-bar-fill {{ height: 100%; border-radius: 3px; }}
  .footer {{ text-align: center; padding: 16px; color: #94a3b8; font-size: 12px; }}
  @media (max-width: 768px) {{ table {{ font-size: 11px; }} td, th {{ padding: 8px 10px; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>📋 工资审核清单看板</h1>
  <div class="meta">
    审核时间: {audit.get('audit_time', datetime.now().isoformat())} |
    检查记录: {audit.get('total_records', 0)} 条 |
    版本: {audit.get('version', 'v5.3')}
  </div>
</div>

<div class="summary-cards">
  <div class="card total"><div class="number">{total}</div><div class="label">审核条目总数</div></div>
  <div class="card pass"><div class="number">{passed}</div><div class="label">✅ 通过</div></div>
  <div class="card warning"><div class="number">{warnings}</div><div class="label">🟠 异常</div></div>
  <div class="card block"><div class="number">{blocks}</div><div class="label">🔴 阻断</div></div>
  <div class="card note"><div class="number">{notes}</div><div class="label">🔵 提示</div></div>
  <div class="card rate"><div class="number">{overall_rate}</div><div class="label">综合通过率</div></div>
</div>

<table>
  <thead>
    <tr>
      <th style="width:40px">#</th>
      <th style="width:80px">类别</th>
      <th style="width:60px">规则ID</th>
      <th style="width:160px">审核条目</th>
      <th style="width:80px">审核结果</th>
      <th style="width:50px">检查数</th>
      <th style="width:50px">通过</th>
      <th style="width:50px">异常</th>
      <th style="width:90px">通过率</th>
      <th style="width:250px">数据依据</th>
      <th style="width:200px">处理建议</th>
    </tr>
  </thead>
  <tbody>
"""

    for idx, item in enumerate(items, 1):
        cat_color = category_colors.get(item["category"], "#64748b")
        status_class = f"status-{item['status']}"
        status_label = status_labels.get(item["status"], item["status"])
        rate_val = float(item["rate"].replace("%", ""))
        bar_color = "#22c55e" if rate_val >= 98 else ("#f59e0b" if rate_val >= 90 else "#ef4444")
        action_class = "" if item["status"] != "pass" else "action-normal"

        html += f"""    <tr>
      <td>{idx}</td>
      <td><span class="category-tag" style="background:{cat_color}">{item['category']}</span></td>
      <td><span class="rule-id">{item['rule_id']}</span></td>
      <td><strong>{item['name']}</strong><br><span style="color:#94a3b8;font-size:11px">{item.get('description', '')[:60]}</span></td>
      <td><span class="status-badge {status_class}">{status_label}</span></td>
      <td style="text-align:center">{item['checked']}</td>
      <td style="text-align:center;color:#22c55e">{item['passed']}</td>
      <td style="text-align:center;color:#ef4444;font-weight:600">{item['failed']}</td>
      <td>
        {item['rate']}
        <span class="rate-bar"><span class="rate-bar-fill" style="width:{rate_val}%;background:{bar_color}"></span></span>
      </td>
      <td class="evidence">{item['evidence']}</td>
      <td class="action {action_class}">{item['action']}</td>
    </tr>
"""

    html += """  </tbody>
</table>
<div class="footer">
  工资审核清单看板 v5.3 | 基于确定性规则引擎生成 | 每个审核结论均有数据依据
</div>
</body>
</html>"""

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
    return html


# ---------------------------------------------------------------------------
# Markdown Kanban Generator
# ---------------------------------------------------------------------------

def generate_markdown_kanban(items, audit):
    """生成 Markdown 审核清单看板（飞书文档友好）"""
    total = len(items)
    passed = sum(1 for i in items if i["status"] == "pass")
    warnings = sum(1 for i in items if i["status"] == "warning")
    blocks = sum(1 for i in items if i["status"] == "block")
    notes = sum(1 for i in items if i["status"] == "note")

    total_checked = sum(i["checked"] for i in items)
    total_failed = sum(i["failed"] for i in items)
    overall_rate = f"{((total_checked - total_failed) / max(total_checked, 1)) * 100:.1f}%"

    lines = []
    lines.append(f"# 📋 工资审核清单看板\n")
    lines.append(f"**审核时间**: {audit.get('audit_time', datetime.now().isoformat())}  ")
    lines.append(f"**检查记录**: {audit.get('total_records', 0)} 条  ")
    lines.append(f"**版本**: {audit.get('version', 'v5.3')}  ")
    lines.append("")

    # Summary
    lines.append("## 📊 审核概览\n")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 审核条目总数 | {total} |")
    lines.append(f"| ✅ 通过 | {passed} |")
    lines.append(f"| 🟠 异常 | {warnings} |")
    lines.append(f"| 🔴 阻断 | {blocks} |")
    lines.append(f"| 🔵 提示 | {notes} |")
    lines.append(f"| 综合通过率 | {overall_rate} |")
    lines.append("")

    # Detail table
    lines.append("## 📋 审核清单明细\n")
    lines.append("| # | 类别 | 规则ID | 审核条目 | 结果 | 检查数 | 通过 | 异常 | 通过率 | 数据依据 | 处理建议 |")
    lines.append("|---|------|--------|---------|------|--------|------|------|--------|---------|---------|")

    status_map = {
        "pass": "✅ 通过",
        "warning": "🟠 异常",
        "block": "🔴 阻断",
        "note": "🔵 提示",
    }

    for idx, item in enumerate(items, 1):
        status_label = status_map.get(item["status"], item["status"])
        evidence = item["evidence"][:120] + "..." if len(item["evidence"]) > 120 else item["evidence"]
        action = item["action"][:80] + "..." if len(item["action"]) > 80 else item["action"]
        lines.append(
            f"| {idx} | {item['category']} | {item['rule_id']} | {item['name']} | {status_label} | "
            f"{item['checked']} | {item['passed']} | {item['failed']} | {item['rate']} | "
            f"{evidence} | {action} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("*工资审核清单看板 v5.3 | 基于确定性规则引擎生成 | 每个审核结论均有数据依据*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="工资审核清单看板生成器 v5.3")
    parser.add_argument("--input", required=True, help="audit_result.json 文件路径")
    parser.add_argument("--format", choices=["html", "markdown", "both"], default="both", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（默认自动命名）")
    parser.add_argument("--review-link", help="异常项人工复核超链接模板 (支持 {emp_id}, {emp_name}, {row_index} 占位符)")

    args = parser.parse_args()

    # Load data
    audit = load_audit_result(args.input)
    rules = load_rules()

    # Build kanban items
        # 解析复核链接模板
    link_template = getattr(args, 'review_link', None)
    items = build_kanban_items(rules, audit, link_template=link_template)
    print(f"✅ 构建了 {len(items)} 条审核清单条目")

    # Generate outputs
    fmt = args.format
    if fmt in ("html", "both"):
        output_path = args.output if args.output and fmt == "html" else "kanban.html"
        generate_html_kanban(items, audit, output_path)
        print(f"✅ HTML 看板已生成: {output_path}")

    if fmt in ("markdown", "both"):
        output_path = args.output if args.output and fmt == "markdown" else "kanban.md"
        md = generate_markdown_kanban(items, audit)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Markdown 看板已生成: {output_path}")


if __name__ == "__main__":
    main()
