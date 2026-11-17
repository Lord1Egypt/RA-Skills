#!/usr/bin/env python3
"""Create a persistent synthetic chart-led PDF for visual acceptance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_INFO = json.loads((ROOT / "version-info.json").read_text(encoding="utf-8"))
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from generate_pdf_report import generate  # type: ignore  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def package() -> dict[str, object]:
    participants = []
    roster = [
        ("omni-ecom-team-lead", "沐风", "全域经营操盘总监", []),
        ("data-analyst", "沈数清", "电商数据分析专家", ["agent-demo-data"]),
        ("platform-ops", "梁运通", "平台运营专家", ["agent-demo-platform"]),
        ("content-live-growth", "洪涨声", "内容与直播增长专家", ["agent-demo-content"]),
        ("ad-profit-optimizer", "罗效盈", "投流与利润优化专家", ["agent-demo-profit"]),
        ("delivery-review", "韦交达", "项目交付与复盘专家", []),
    ]
    for agent_id, name, profession, task_ids in roster:
        participants.append({
            "agent_id": agent_id,
            "display_name": name,
            "profession": profession,
            "participation_status": "contributed" if agent_id != "delivery-review" else "pending_review",
            "agent_task_ids": task_ids,
        })
    return {
        "schema_version": "1.0",
        "team_id": "omni-ecom",
        "team_version": VERSION_INFO["team_version"],
        "team_previous_version": VERSION_INFO["previous_version"],
        "report_revision": "R1",
        "task_type": "weekly_report",
        "task_profile": {"display_name": "经营周报"},
        "title": "脱敏演示店铺周度经营分析报告",
        "period": "2026-W32",
        "gate_status": "WARN",
        "expert_participation": participants,
        "metrics": [
            {
                "period": "上一周",
                "inputs": {"gmv": 15550, "visitors": 5496, "buyers": 65, "orders": 68, "refund_amount": 2600},
                "metrics": {"conversion_rate": 0.0118, "aov": 239.23, "refund_rate_amount": 0.1672},
            },
            {
                "period": "本周",
                "inputs": {"gmv": 10348, "visitors": 5619, "buyers": 45, "orders": 47, "refund_amount": 2300},
                "metrics": {"conversion_rate": 0.0080, "aov": 229.96, "refund_rate_amount": 0.2223},
            },
        ],
        "facts": [
            {"claim": "本周访客保持稳定，但支付买家减少，成交效率弱于上一周。"},
            {"claim": "核心规模指标已通过访客、买家与销售额勾稽。"},
        ],
        "judgments": [
            {"claim": "当前主要矛盾在成交转化，而不是简单的流量不足。", "confidence": "medium"},
        ],
        "hypotheses": [
            {"claim": "部分流量来源与商品承接不匹配。", "verification_method": "按来源拆分访客、加购和支付买家连续观察 7 天。"},
        ],
        "actions": [
            {"priority": "P0", "action": "复核低转化来源的落地商品与首屏卖点", "owner": "运营", "acceptance": "重点来源支付转化率连续7天改善"},
            {"priority": "P0", "action": "对高退款商品补充规格与价格预期说明", "owner": "商品", "acceptance": "下单错误与价格原因退款占比下降"},
            {"priority": "P1", "action": "对老客池执行分层回访测试", "owner": "会员", "acceptance": "回访人群支付买家数达到设定样本门槛"},
            {"priority": "P2", "action": "补齐投放花费和毛利数据", "owner": "运营/财务", "acceptance": "可复算净ROAS与贡献利润"},
        ],
        "missing_data": ["分计划投放花费", "商品毛利与履约成本"],
        "risks": ["样例数据仅用于版式验收，不代表真实客户经营结果"],
        "sources": [{"type": "synthetic_fixture", "source": "pdf_smoke.py", "status": "verified"}],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    report_json = output_dir / "report.json"
    write_json(report_json, package())
    try:
        receipt = generate(
            report_json,
            output_dir / "report.pdf",
            output_dir / "pdf-delivery.json",
            output_dir / ".pdf_qa",
        )
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 1
    ok = receipt.get("status") == "pdf_render_verified" and int(receipt.get("chart_count", 0)) >= 3
    print(json.dumps({"status": "PASS" if ok else "FAIL", **receipt}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
