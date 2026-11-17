#!/usr/bin/env python3
"""Generate the default chart-led PDF delivery from report.json.

This module does not derive new business claims. It visualizes only metrics,
facts, judgments, actions and collaboration evidence already present in the
validated report package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import tempfile
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
PDF_SKILL = ROOT / "skills" / "ecom-report-pdf-layout" / "scripts"
if str(PDF_SKILL) not in sys.path:
    sys.path.insert(0, str(PDF_SKILL))

from pdf_layout_kit import (  # type: ignore  # noqa: E402
    CONTENT_W,
    KeepTogether,
    Paragraph,
    Spacer,
    body_left,
    build_doc,
    chart,
    cm,
    finding,
    judge,
    make_table,
    section_title,
    setup_matplotlib_cn,
    small,
    styles,
)


METRICS: list[tuple[str, str, str, bool]] = [
    ("gmv", "销售额", "money", False),
    ("net_gmv_reference", "净销售参考", "money", False),
    ("visitors", "访客数", "number", False),
    ("buyers", "支付买家", "number", False),
    ("orders", "订单量", "number", False),
    ("aov", "客单价", "money", False),
    ("uv_value", "访客价值", "per_visitor", False),
    ("conversion_rate", "支付转化率", "rate", False),
    ("refund_rate_amount", "金额退款率", "rate", True),
    ("roas", "ROAS", "ratio", False),
    ("net_roas", "扣退款 ROAS（非利润）", "ratio", False),
    ("contribution_roas", "扣匹配变动成本 ROAS（非净利润）", "ratio", False),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("report_json_invalid")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def num(value: Any) -> float | None:
    if isinstance(value,bool):
        raise ValueError('report_metric_boolean_not_number')
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def metric_value(row: dict[str, Any], key: str) -> float | None:
    from report_metric_guard import metric_value as checked_value
    value=checked_value(row,key)
    if value is None: return None
    converted=float(value)
    if not math.isfinite(converted) or (converted==0 and value!=0):
        raise ValueError('report_metric_not_renderable')
    return converted


def fmt(value: float | None, kind: str) -> str:
    if value is None:
        return "数据不足"
    if kind == "money":
        return f"{value:,.2f}元"
    if kind == "per_visitor":
        return f"{value:,.2f}元/人"
    if kind == "rate":
        return f"{value * 100:.2f}%"
    if kind == "ratio":
        return f"{value:.2f}倍"
    return f"{value:,.0f}"


def change(current: float | None, previous: float | None, kind: str) -> str:
    if current is None or previous is None:
        return "-"
    if kind == "rate":
        delta = (current - previous) * 100
        return f"{'↑' if delta > 0 else '↓' if delta < 0 else '—'}{abs(delta):.2f}个百分点" if delta else "—"
    if previous==0:
        return '基期为0，不计算相对变化'
    delta = (current - previous) / abs(previous) * 100
    return f"{'↑' if delta > 0 else '↓' if delta < 0 else '—'}{abs(delta):.2f}%" if delta else "—"


def clean(value: Any, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return escape(text[:limit])


def complete(value: Any) -> str:
    """Full business text, unlike explicitly abbreviated navigation/summary."""
    from report_text_fields import text
    return escape(re.sub(r'\s+', ' ', text(value)).strip())


def strip_tag(text: str) -> str:
    """Drop a leading 【...】 tag so callers can prefix without doubling it."""
    return re.sub(r"^【[^】]*】\s*", "", str(text or "").strip())


def chart_sales(rows: list[dict[str, Any]], out: Path) -> bool:
    values = [(str(row.get("period", f"期间{i + 1}")), metric_value(row, "gmv")) for i, row in enumerate(rows)]
    values = [(label, value) for label, value in values if value is not None]
    if not values:
        return False
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    labels, data = zip(*values)
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    bars = ax.bar(labels, data, color="#2E5AAC", width=0.55)
    ax.set_title("销售额趋势（元）", loc="left")
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in data], padding=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def chart_returns(rows: list[dict[str, Any]], out: Path) -> bool:
    values=[]
    for row in rows:
        for key,label,color in (('roas','ROAS','#2E5AAC'),('net_roas','扣退款 ROAS','#6B8FD6'),
                                ('contribution_roas','扣匹配变动成本 ROAS','#8A6BBE')):
            value=metric_value(row,key)
            if value is not None:
                values.append((str(row['period'])+'\n'+label,value,color))
    if not values: return False
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,3.4),dpi=160)
    bars=ax.bar([v[0] for v in values],[v[1] for v in values],color=[v[2] for v in values],width=0.55)
    ax.set_title('投放回报（倍；非利润）',loc='left')
    if min(v[1] for v in values)>=0: ax.set_ylim(bottom=0)
    else: ax.axhline(0,color='#555555',linewidth=0.8)
    ax.grid(axis='y',alpha=0.18)
    ax.spines[['top','right']].set_visible(False)
    ax.bar_label(bars,labels=[f'{v[1]:.2f}倍' for v in values],padding=3,fontsize=9)
    fig.tight_layout(); fig.savefig(out,facecolor='white'); plt.close(fig)
    return True


def chart_traffic(rows: list[dict[str, Any]], out: Path) -> bool:
    current = rows[-1] if rows else {}
    values = [("访客", metric_value(current, "visitors")), ("支付买家", metric_value(current, "buyers")), ("订单", metric_value(current, "orders"))]
    values = [(label, value) for label, value in values if value is not None]
    if len(values) < 2:
        return False
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    labels, data = zip(*values)
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    bars = ax.barh(labels, data, color=["#6B8FD6", "#2E5AAC", "#8AA4D6"][: len(data)])
    logarithmic = min(data)>0 and max(data)/min(data)>30
    ax.set_title("流量到成交规模（横轴为对数刻度）" if logarithmic else "流量到成交规模（线性刻度）", loc="left")
    ax.set_xscale("log" if logarithmic else "linear")
    ax.grid(axis="x", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in data], padding=4, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def chart_rates(rows: list[dict[str, Any]], out: Path) -> bool:
    current = rows[-1] if rows else {}
    previous = rows[-2] if len(rows) > 1 else None
    keys = [("支付转化率", "conversion_rate"), ("金额退款率", "refund_rate_amount")]
    labels: list[str] = []
    now_values: list[float] = []
    previous_values: list[float] = []
    previous_positions: list[int] = []
    for label, key in keys:
        value = metric_value(current, key)
        if value is not None:
            labels.append(label)
            now_values.append(value * 100)
            prior=metric_value(previous,key) if previous else None
            if prior is not None:
                previous_positions.append(len(labels)-1)
                previous_values.append(prior*100)
            elif previous:
                labels[-1]+='\n对比期缺数'
    if not labels:
        return False
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.arange(len(labels))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    if previous:
        if previous_positions:
            prior_bars=ax.bar(x[previous_positions] - width / 2, previous_values, width, label="上一期", color="#B8C8E6")
            ax.bar_label(prior_bars,labels=[f"{v:.2f}%" for v in previous_values],padding=3,fontsize=9)
        bars = ax.bar(x + width / 2, now_values, width, label="本期", color="#2E5AAC")
        ax.legend(frameon=False)
    else:
        bars = ax.bar(x, now_values, width=0.5, color="#2E5AAC")
    ax.set_title("关键比率（%）", loc="left")
    ax.set_xticks(x, labels)
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[f"{v:.2f}%" for v in now_values], padding=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def chart_actions(package: dict[str, Any], out: Path) -> bool:
    counts = Counter(str(item.get("priority") or "未分级") for item in package.get("actions", []) if isinstance(item, dict))
    if not counts:
        counts["已列行动"] = 0
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    labels = list(counts)
    values = [counts[label] for label in labels]
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    bars = ax.bar(labels, values, color="#6B8FD6")
    ax.set_title("行动优先级分布", loc="left")
    ax.set_ylabel("行动数")
    ax.set_ylim(0, max(values) + 1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[str(v) for v in values], padding=3)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def chart_data_gate(package: dict[str, Any], out: Path) -> bool:
    from report_metric_guard import period_key
    periods={period_key(row.get('period')) for row in package.get('metrics',[])}
    checked_sources={(item['source']['file'],item['source']['sha256']) for item in
                     package.get('claim_ledger',{}).get('source_checks',[]) if 'source' in item}
    values = [
        len(periods),
        len(checked_sources),
        len(package.get("missing_data", [])),
        len(package.get("risks", [])),
    ]
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    labels = ["不同指标期间", "复算来源文件", "缺失项", "风险项"]
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    bars = ax.bar(labels, values, color=["#2E5AAC", "#6B8FD6", "#E6A23C", "#FF6B6B"])
    ax.set_title("数据闸门概况", loc="left")
    ax.set_ylim(0, max(values + [1]) + 1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[str(v) for v in values], padding=3)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def chart_participation(package: dict[str, Any], out: Path) -> bool:
    counts = Counter(
        "已贡献" if item.get("participation_status") == "contributed" else "待复核/未调用"
        for item in package.get("expert_participation", [])
        if isinstance(item, dict)
    )
    if not counts:
        return False
    setup_matplotlib_cn()
    import matplotlib.pyplot as plt
    labels = list(counts)
    values = [counts[label] for label in labels]
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=160)
    bars = ax.bar(labels, values, color=["#2E5AAC", "#B8C8E6"][: len(values)])
    ax.set_title("专家协作参与状态", loc="left")
    ax.set_ylabel("岗位数")
    ax.set_ylim(0, max(values) + 1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[str(v) for v in values], padding=3)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return True


def render_charts(package: dict[str, Any], chart_dir: Path) -> list[tuple[Path, str]]:
    chart_dir.mkdir(parents=True, exist_ok=True)
    from report_metric_guard import metric_groups
    groups=metric_groups(package)
    specs=[]
    for index,(label,rows) in enumerate(groups,1):
        suffix='' if len(groups)==1 else ' · '+escape(label)
        prefix='' if len(groups)==1 else f'g{index}-'
        specs.extend([
            (chart_sales, (rows,chart_dir/(prefix+'01-sales.png')), '销售额趋势'+suffix),
            (chart_traffic, (rows,chart_dir/(prefix+'02-traffic.png')), '流量到成交规模'+suffix),
            (chart_rates, (rows,chart_dir/(prefix+'03-rates.png')), '转化与退款关键比率'+suffix),
            (chart_returns, (rows,chart_dir/(prefix+'03-returns.png')), '投放回报（非利润）'+suffix)])
    specs.extend([
        (chart_actions, (package, chart_dir / "04-actions.png"), "图4 行动优先级分布"),
        (chart_data_gate, (package, chart_dir / "05-data-gate.png"), "图5 数据闸门概况"),
        (chart_participation, (package, chart_dir / "06-participation.png"), "图6 专家协作参与状态"),
    ])
    result: list[tuple[Path, str]] = []
    for fn, args, caption in specs:
        if fn(*args):
            result.append((args[-1], f'图{len(result)+1} '+re.sub(r'^图\d+\s*','',caption)))
    if len(result) < 3:
        raise ValueError("pdf_chart_minimum_not_met")
    return result


def page_decorator(canvas: Any, doc: Any, candidate: bool = False) -> None:
    canvas.saveState()
    canvas.setFont("YaHei", 8)
    canvas.setFillColorRGB(0.42, 0.42, 0.42)
    canvas.drawString(2.5 * cm, 1.05 * cm, "候选验收 - 未正式交付" if candidate else "标准经营报告 - 以 completion-receipt.json 为正式完成依据")
    canvas.drawRightString(18.5 * cm, 1.05 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


def build_story(package: dict[str, Any], charts: list[tuple[Path, str]]) -> list[Any]:
    from report_metric_guard import metric_groups
    from report_presentation import view, action_order
    presentation=view(package)
    groups=metric_groups(package)
    story: list[Any] = [
        Paragraph(clean(package.get("title") or "电商经营分析报告"), styles["DocTitle"]),
        Paragraph(
            f"报告期：{clean(package.get('period'))} ｜ 任务：{clean(package.get('task_profile', {}).get('display_name'))} ｜ 专家团版本：{clean(package.get('team_version'))} ｜ 上一版本：{clean(package.get('team_previous_version'))} ｜ 报告修订：{clean(package.get('report_revision'))} ｜ 数据闸门：{clean(package.get('gate_status'))}",
            styles["DocMeta"],
        ),
    ]
    version_changes = [str(item) for item in (package.get("team_version_changes") or []) if str(item).strip()]
    if package.get('acceptance_only'):
        story.append(finding(clean(package['acceptance_notice'], 400)))
    if version_changes:
        excerpt = "；".join(clean(item, 90) for item in version_changes[:3])
        story.append(
            small(
                f"版本差异（{clean(package.get('team_previous_version'))} → {clean(package.get('team_version'))}，共 {len(version_changes)} 条，节选前 3 条）：{excerpt}"
            )
        )
    summary = next((item.get("claim") for item in package.get("judgments", []) if isinstance(item, dict) and item.get("claim")), None)
    if not summary:
        summary = next((item.get("claim") for item in package.get("facts", []) if isinstance(item, dict) and item.get("claim")), "当前仅形成数据质量结论。")
    story += [finding(clean(summary, 260)) if package.get('acceptance_only') else judge(clean(summary, 260)), Spacer(1, 8)]
    story.append(small('本次重点：'+'；'.join(presentation['focus'])))
    story.append(small('比较要求：'+clean(presentation['comparison_expectation'] or '仅使用已提供的同口径资料',500)))
    for action in action_order(package.get('actions',[]))[:3]:
        story.append(small('优先动作：'+clean(action.get('action'),500)+'；负责人：'+clean(action.get('owner') or '待指定',100)))
    if package.get('task_type')=='weekly_report':
        from previous_action_review import feedback_lines
        story.append(small('上次行动回验：'))
        story.extend(small(complete(line)) for line in feedback_lines(package.get('previous_action_review')))
    if package.get('team_maintenance_revision'):
        story.append(small('专家团维护批次：'+complete(package['team_maintenance_revision'])))
    appendix_story=[]

    if package.get("stage0", {}).get("status") == "stage0_complete":
        story.append(small(f"资料覆盖：共 {len(package.get('report_inventory',{}).get('reports',[]))} 份报表；完整清单、归类和章节映射见证据附录。"))
        appendix_story += [section_title("附录", "数据概览与覆盖")]
        inventory_rows = [["报表", "文件", "类型", "期间", "状态"]]
        for item in package.get("report_inventory", {}).get("reports", []):
            scope = item.get("time_scope", {})
            period = scope.get("note") or f"{scope.get('start') or ''}~{scope.get('end') or ''}"
            inventory_rows.append([clean(item.get("report_id"), 12), clean(item.get("file_name"), 30), clean(item.get("report_type_label") or item.get("report_type"), 28), clean(period, 18), clean(item.get("verdict"), 14)])
        appendix_story.append(make_table(inventory_rows, [1.6*cm, 3.5*cm, 4.6*cm, 3.0*cm, 2.4*cm], first_col_left=True))
        cluster_rows = [["归类", "业务域", "名称", "包含报表", "状态"]]
        for item in package.get("report_clusters", {}).get("clusters", []):
            cluster_rows.append([clean(item.get("cluster_id"), 12), clean(item.get("domain"), 18), clean(item.get("label"), 26), clean(", ".join(item.get("members", [])), 24), clean(item.get("sufficiency"), 14)])
        appendix_story.append(make_table(cluster_rows, [1.6*cm, 2.6*cm, 4.7*cm, 3.5*cm, 2.7*cm], first_col_left=True))
        chapter_rows = [["章节", "标题", "负责人", "来源报表"]]
        for item in package.get("chapter_plan", {}).get("chapters", []):
            chapter_rows.append([clean(item.get("chapter_id"), 12), clean(item.get("title"), 32), clean(item.get("owner_agent"), 24), clean(", ".join(item.get("source_report_ids", [])) or "无直接报表", 24)])
        appendix_story.append(make_table(chapter_rows, [1.8*cm, 6.0*cm, 4.0*cm, 3.3*cm], first_col_left=True))

    story += [section_title("一", "核心指标速览")]
    shown=False
    for scope_label,rows in groups:
        current=rows[-1]; previous=rows[-2] if len(rows)>1 else None
        metric_rows = [["指标", "本期", "对比期", "变化"]]
        for key, label, kind, _inverse in METRICS:
            cur = metric_value(current, key)
            prev = metric_value(previous, key) if previous else None
            if cur is not None:
                metric_rows.append([label, fmt(cur, kind), fmt(prev, kind), change(cur, prev, kind)])
        if len(metric_rows)>1:
            shown=True
            description=f"{scope_label}；本期 {current['period']}；对比期 {previous['period'] if previous else '无'}"
            story.append(small(escape(description)))
            story.append(make_table(metric_rows,[4.0*cm]*4,first_col_left=True))
    if not shown:
        story += [finding("当前数据闸门未提供可视化经营指标；以下只展示数据完整性和待补项。")]

    story += [section_title("二", "关键图表")]
    for path, caption in charts:
        label = caption + '（透明固定测试源，非客户经营表现）' if package.get('acceptance_only') else caption
        story.append(KeepTogether(chart(str(path), caption=label)))

    story += [section_title("三", "事实、判断与限制")]
    shown_items=set()
    sections=[(str(c.get('title') or c.get('chapter_id')),c['items']) for c in presentation['chapters'] if c['items']]
    sections.append(('跨章节汇总',presentation['unassigned_findings']))
    for heading,items in sections:
        if not items:continue
        story.append(body_left('<b>'+clean(heading,300)+'</b>'))
        for item in items:
            identity=item['presentation_key']
            if identity in shown_items:continue
            shown_items.add(identity)
            label={'facts':'事实','judgments':'判断','hypotheses':'待验证'}[item['kind']]
            claim=str(item.get('claim') or '')
            story.append(body_left('【'+label+'】'+strip_tag(clean(claim,max(240,len(claim))))))
            if item['kind']=='hypotheses':
                story.append(small('验证：'+complete(item.get('verification_method'))))
            if item['kind']=='judgments':
                story.append(small('置信度：'+clean(item.get('confidence') or '待定',100)))
            if item.get('counter_conditions'):
                story.append(small('反证条件：'+complete('；'.join(item['counter_conditions']))))
            story.append(small('证据：'+complete(', '.join(item.get('evidence_ids',[])))))
    for item in ([] if package.get('acceptance_only') else package.get("missing_data", [])):
        from report_text_fields import gap_lines
        story.extend(small('待补数据：'+complete(line)) for line in gap_lines(item))
    if package.get('risks'):
        story.append(body_left('<b>风险与限制</b>'))
        story.extend(small(complete(item)) for item in package['risks'])

    story += [section_title("四", "优先行动")]
    action_items = action_order(package.get("actions", []))
    if action_items:
        for index, item in enumerate(action_items, 1):
            block = [
                Paragraph(
                    f"<b>行动 {index}</b>：{clean(item.get('action_id') or '未编号', 60)} ｜ 优先级 {clean(item.get('priority') or '未分级', 20)}",
                    styles["Judge"],
                ),
                body_left(f"<b>动作：</b>{complete(item.get('action'))}"),
                body_left(f"<b>负责人：</b>{clean(item.get('owner') or '待指定', 200)} ｜ <b>到期：</b>{clean(item.get('due') or '待指定', 40)}"),
                body_left(f"<b>验收指标：</b>{complete(item.get('acceptance') or '待补充')}"),
                body_left(
                    f"<b>审批：</b>{clean(item.get('approval_state') or '待确认', 40)} ｜ <b>状态：</b>{clean(item.get('status') or '待确认', 40)} ｜ <b>停止条件：</b>{complete(item.get('stop_condition') or '待补充')}"
                ),
                Spacer(1, 6),
            ]
            if sum(len(str(item.get(k) or '')) for k in ('action','acceptance','stop_condition'))<=1200:
                story.append(KeepTogether(block))
            else:
                story.extend(block)
    else:
        story.append(body_left("当前没有通过治理闸门的行动项。"))

    from decision_display import sections as decision_sections
    decisions=decision_sections(package)
    if decisions:
        for index,(title,paragraphs) in enumerate(decisions):
            block=([section_title("裁决", "专家分歧与总监结论")] if index==0 else [])
            block.append(body_left('<b>'+escape(title)+'</b>'))
            for paragraph in paragraphs:
                block.append(body_left(escape(paragraph)))
            block.append(Spacer(1,6))
            if sum(len(p) for p in paragraphs)<=1200 and len(paragraphs)<=10:
                story.append(KeepTogether(block))
            else:
                story.extend(block)
    story.extend(appendix_story)
    story += [section_title("附录", "专家协作与版本凭证")]
    quality = package.get("collaboration_quality", {})
    if quality:
        story.append(body_left(f"共享基线 SHA256：{clean(quality.get('baseline_sha256'), 80)}"))
        depth_rows = [["专家", "达到", "要求", "数据闸门", "深度状态"]]
        for item in quality.get("agent_depth", []):
            depth_rows.append([clean(item.get("agent_id"), 24), clean(item.get("reached_level"), 8), clean(item.get("required_level"), 8), clean(item.get("gate_status"), 12), clean(item.get("status"), 14)])
        story.append(make_table(depth_rows, [4.5*cm, 1.8*cm, 1.8*cm, 3.0*cm, 3.0*cm], first_col_left=True))
        story.append(small(f"冲突扫描：{clean(quality.get('conflict_scan_status'), 30)}；hard={quality.get('hard_conflict_count', 0)}，soft={quality.get('soft_conflict_count', 0)}；质疑轮={quality.get('challenge_round_status', '')}；团长复算={quality.get('lead_recomputation_status', '')}，裁决条目={quality.get('adjudication_count', 0)}"))
    participation_rows = [["专家", "岗位", "状态", "Agent 子任务"]]
    for item in package.get("expert_participation", []):
        if isinstance(item, dict):
            agent_id = clean(item.get("agent_id"), 40)
            raw_status = clean(item.get("participation_status"), 24)
            if agent_id == "delivery-review" and raw_status in {"not_invoked", "pending_review"}:
                display_status = "交付前独立复核"
                display_task = "最终状态见放行凭证"
            else:
                display_status = raw_status
                display_task = clean(", ".join(item.get("agent_task_ids", [])) or "主任务", 70)
            participation_rows.append([
                clean(item.get("display_name") or item.get("agent_id"), 30),
                clean(item.get("profession"), 50),
                display_status,
                display_task,
            ])
    if len(participation_rows) > 1:
        story.append(make_table(participation_rows, [2.8 * cm, 4.8 * cm, 3.0 * cm, 5.4 * cm], first_col_left=True))
    for item in package.get("expert_participation", []):
        if isinstance(item, dict) and item.get("agent_id") != "delivery-review":
            summary = clean(item.get("contribution_summary") or "未提供贡献摘要", 900)
            story.append(small(f"{clean(item.get('display_name') or item.get('agent_id'), 30)}贡献：{summary}"))
    for item in package.get('mechanism_findings', []):
        story.append(body_left('<b>'+clean(item['agent_id'])+' 的独立机制核查（岗位闸门 '+clean(item['gate_status'])+'）</b>'))
        for fact in item['facts']:
            story.append(body_left(complete(fact.get('claim'))))
            story.append(small('证据编号：'+clean(', '.join(fact.get('evidence_ids', [])))))
        for missing in item.get('missing_data', []):
            from report_text_fields import gap_lines
            story.extend(small('未验证范围：'+complete(line)) for line in gap_lines(missing))
    story += [section_title("六", "数字来源与复算索引")]
    story.append(small("以下逐项列出原表定位或计算依据；缺数不补为 0。复算只验证本地来源一致性，不代表平台认证或完整业务口径已经通过。"))
    for item in package.get('claim_ledger',{}).get('claims',[]):
        claim_start=len(story)
        status=item['status']
        label={'verified':'原表复算','derived':'公式复算','unknown':'缺数，未复算'}[status]
        value='未知' if status=='unknown' else str(item['value'])
        heading=f"{item['claim_id']} ｜ {item['metric']} ｜ {value} {item.get('unit','')} ｜ {label}"
        story.append(body_left('<b>'+escape(heading)+'</b>'))
        from report_metric_guard import scope_key
        platform,store,dimensions=scope_key(package,item)
        scope_parts=[f'平台：{platform}' if platform else '',f'店铺：{store}' if store else '']
        detail_dimensions=json.loads(dimensions)
        if detail_dimensions: scope_parts.append('细分：'+'，'.join(f'{k}={v}' for k,v in detail_dimensions.items()))
        if any(scope_parts): story.append(small(escape('；'.join(part for part in scope_parts if part))))
        source=item['source_ref']
        if status=='verified':
            location_keys=('sheet','range') if Path(source['source_file']).suffix.lower() in ('.xlsx','.xls') else ('pointer',) if Path(source['source_file']).suffix.lower()=='.json' else ('range',)
            location='；'.join(str(source[key]) for key in location_keys if source.get(key))
            aggregation={'value':'单格取值','sum':'求和','mean':'平均'}[source.get('aggregation','value')]
            detail=f"来源：{source['source_file']}；字段：{source['field']}；位置：{location}；汇总方式：{aggregation}"
            story.append(small(escape(detail)))
        elif status=='derived':
            formula=item['formula']
            story.append(small(escape(f"公式：{formula['expression']}；输入编号：{', '.join(item['inputs'])}")))
            if formula.get('bindings'):
                story.append(small(escape('变量对应：'+json.dumps(formula['bindings'],ensure_ascii=False))))
        else:
            story.append(small(escape('缺口说明：'+str(item.get('missing_reason') or source.get('field') or '待补原始数据'))))
        if item.get('decimal_places') is not None:
            story.append(small(escape(f"显示四舍五入到 {item['decimal_places']} 位小数；期间：{item['period']}")))
        else:
            story.append(small(escape('期间：'+str(item['period']))))
        story.append(Spacer(1,5))
        if len(json.dumps(item,ensure_ascii=False))<=2500:
            story[claim_start:]=[KeepTogether(story[claim_start:])]
    if package.get('acceptance_only'):
        story += [section_title('七', '验收缺口与限制（CH05）')]
        story.append(small(clean(package['chapter_plan_enrichment']['note'], 500)))
        for gap in package.get('missing_data', []):
            story.append(body_left(complete(gap['gap_id']+' '+gap['owner_agent']+'：'+gap['item'])))
            story.append(small('对结论的影响：'+complete(gap['impact'])))
            story.append(small('补数要求：'+complete(gap['required_source'])))
    story += [
        Spacer(1, 8),
        small(f"专家团版本：{clean(package.get('team_version'))}；上一版本：{clean(package.get('team_previous_version'))}；本次报告修订：{clean(package.get('report_revision'))}。"),
        small("候选版本仅可记录 candidate_pipeline_complete，以 candidate-acceptance-receipt.json 为依据；不构成正式交付。" if '-candidate.' in str(package.get('team_version')) else "本 PDF 为待冻结和独立复核的候选稿。只有独立交付复核、公域隔离和最终完成闸门全部通过，且 completion-receipt.json 状态为 formal_delivery_complete 后，才构成正式交付。"),
    ]
    return story


def inspect_pdf(pdf_path: Path, render_dir: Path, page_limit: int = 17) -> dict[str, Any]:
    try:
        import pymupdf as fitz
    except ImportError as exc:
        raise ValueError("pdf_render_dependency_missing") from exc
    render_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    pages: list[dict[str, Any]] = []
    blank_pages: list[int] = []
    for index, page in enumerate(doc, 1):
        text = page.get_text().strip()
        images = len(page.get_images(full=True))
        if len(text) < 30 and images == 0:
            blank_pages.append(index)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25), alpha=False)
        image_path = render_dir / f"page-{index:02d}.png"
        pix.save(image_path)
        pages.append({"page": index, "text_chars": len(text), "embedded_images": images, "render": image_path.name})
    page_count = doc.page_count
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    if page_count > page_limit or blank_pages or not re.search(r"[\u4e00-\u9fff]", text):
        raise ValueError("pdf_render_quality_failed")
    return {"page_count": page_count, "blank_pages": blank_pages, "pages": pages, "text_chars": len(text)}


def generate(report_json: Path, output: Path, qa_output: Path, render_dir: Path) -> dict[str, Any]:
    report_json,output,qa_output,render_dir=[Path(p).resolve() for p in (report_json,output,qa_output,render_dir)]
    report_original=sha256(report_json)
    package = read_json(report_json)
    from report_metric_guard import validate_delivery_metrics as validate_report_metrics
    validate_report_metrics(package)
    required = ("team_version", "report_revision", "title", "gate_status", "expert_participation")
    if any(not package.get(key) for key in required):
        raise ValueError("report_package_missing_pdf_fields")
    from claim_source_guard import validate_report_sources
    markdown=report_json.parent/'report.md'
    markdown_original=sha256(markdown)
    claim_check=validate_report_sources(package,report_json.parent,markdown.read_text(encoding='utf-8-sig'))
    inputs={str(report_json):report_original,str(markdown):markdown_original}
    inputs.update({str((report_json.parent/item['file']).resolve()):item['sha256'] for item in claim_check['inputs']})
    chart_dir=(output.parent/'.report_charts').resolve()
    if (output==qa_output or any(str(path) in inputs for path in (output,qa_output)) or
        any(Path(path).is_relative_to(folder) for path in inputs for folder in (render_dir,chart_dir)) or
        any(path.is_relative_to(folder) for path in (output,qa_output) for folder in (render_dir,chart_dir))):
        raise ValueError('pdf_output_overlaps_inputs')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='omni-pdf-',dir=output.parent) as temporary:
        stage=Path(temporary)
        charts=render_charts(package,stage/'charts')
        staged_pdf=stage/'report.pdf'
        doc=build_doc(str(staged_pdf),title=str(package.get('title') or '电商经营分析报告'))
        from functools import partial
        decorator = partial(page_decorator, candidate='-candidate.' in package['team_version'])
        doc.build(build_story(package,charts),onFirstPage=decorator,onLaterPages=decorator)
        from pdf_layout_policy import page_limit
        maximum_pages=page_limit(package)
        inspection=inspect_pdf(staged_pdf,stage/'pages',page_limit=maximum_pages)
        if any(sha256(Path(path))!=digest for path,digest in inputs.items()):
            raise ValueError('pdf_inputs_changed_during_render')
        # Do not replace an existing delivery with a failed or unverified render.
        chart_dir.mkdir(parents=True,exist_ok=True)
        render_dir.mkdir(parents=True,exist_ok=True)
        for path,_caption in charts: shutil.copy2(path,chart_dir/path.name)
        for page in inspection['pages']:
            shutil.copy2(stage/'pages'/page['render'],render_dir/page['render'])
        staged_pdf.replace(output)
    from artifact_contract import native_receipt_identity
    receipt = {
        **native_receipt_identity("pdf_delivery", package["team_version"]),
        "status": "pdf_render_verified",
        "run_id": package['run_id'],
        "client_scope": package['client_scope'],
        "input_fingerprints": {str(Path(path).relative_to(report_json.parent)):digest for path,digest in inputs.items()},
        "claim_source_gate": claim_check,
        "team_version": package["team_version"],
        "report_revision": package["report_revision"],
        "report_file": output.name,
        "report_sha256": sha256(output),
        "report_bytes": output.stat().st_size,
        "chart_count": len(charts),
        "chart_files": [path.name for path, _caption in charts],
        "page_count": inspection["page_count"],
        "page_limit": maximum_pages,
        "blank_pages": inspection["blank_pages"],
        "text_chars": inspection["text_chars"],
        "rendered_pages": inspection["pages"],
        "render_directory": str(render_dir.relative_to(output.parent)) if render_dir.is_relative_to(output.parent) else None,
        "verified_at": utc_now(),
    }
    write_json(qa_output, receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate chart-led PDF from a report package")
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa-output", required=True)
    parser.add_argument("--render-dir", required=True)
    args = parser.parse_args()
    try:
        result = generate(
            Path(args.report_json).resolve(),
            Path(args.output).resolve(),
            Path(args.qa_output).resolve(),
            Path(args.render_dir).resolve(),
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError, ArithmeticError, ImportError, RecursionError) as exc:
        print(json.dumps({"status": "pdf_generation_failed", "reason": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
