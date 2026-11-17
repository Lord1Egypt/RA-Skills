from __future__ import annotations

"""Expert review report export for NOMOS decision records.

Layer-2 human-readable output. Every claim in the report is anchored onto
machine-readable audit artifacts (the record_hash chain, algorithm audit
event hashes, and the hub report hash) so a domain expert can re-verify the
report without trusting the report itself. The report is a local file and is
never sealed by the engine; it is a presentation layer, not an audit record.
"""

from datetime import datetime, timezone
from pathlib import Path

from .audit.ledger import verify_algorithm_audit
from .decision.integrity import verify_chain, verify_record
from .hub.integrity import verify_hub_report
from .models.hub import HubReport
from .models.schemas import DecisionRecord
from .version import VERSION

_PASS = "PASS"
_FAIL = "FAIL"


def _verdict(ok: bool) -> str:
    return _PASS if ok else _FAIL


def _decision_row(record: DecisionRecord) -> str:
    result = record.result
    leading = ", ".join(result.leading_candidate_ids) or "—"
    return (
        f"| {record.revision} | {result.decision_id} | {result.status.value} | "
        f"{result.audit_passed} | {leading} | {record.record_hash} |"
    )


def _audit_rows(record: DecisionRecord) -> list[str]:
    return [
        f"| {event.sequence} | {event.stage} | {event.rule_id} | {event.operation} | {event.event_hash} |"
        for event in record.result.algorithm_audit
    ]


def export_expert_report(
    *,
    records: list[DecisionRecord],
    hub_report: HubReport | None = None,
    out_path: Path | None = None,
    out_dir: Path = Path("reports"),
) -> Path:
    """Render an expert review report and write it to a local Markdown file.

    Returns the path of the written file.
    """
    if not records:
        raise ValueError("at least one decision record is required")

    chain_ok = verify_chain(records)
    per_record_ok = {record.result.decision_id: verify_record(record) for record in records}
    audit_ok = {
        record.result.decision_id: verify_algorithm_audit(
            record.result.algorithm_audit,
            record.result.algorithm_audit_root_hash,
        )
        for record in records
    }
    hub_ok = verify_hub_report(hub_report) if hub_report is not None else None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    scope = f"{len(records)} 条决策记录"
    if hub_report is not None:
        scope += "，1 份 Hub 报告"
    lines = []
    lines.append("# NOMOS 领域专家复核报告")
    lines.append("")
    lines.append(f"- 报告生成时间：{now}")
    lines.append(f"- 引擎版本：{VERSION}")
    lines.append(f"- 复核对象：{scope}")
    lines.append("")
    lines.append("## 1. 结论摘要")
    lines.append("")
    lines.append("| 校验项 | 结果 |")
    lines.append("|---|---|")
    lines.append(f"| 决策链完整性（revision 单调 + 父哈希衔接） | {_verdict(chain_ok)} |")
    for decision_id, ok in per_record_ok.items():
        lines.append(f"| 记录哈希自洽（{decision_id}） | {_verdict(ok)} |")
    for decision_id, ok in audit_ok.items():
        lines.append(f"| 算法审计账本校验（{decision_id}） | {_verdict(ok)} |")
    if hub_ok is not None:
        lines.append(f"| Hub 报告哈希 | {_verdict(hub_ok)} |")
    lines.append("")
    lines.append("## 2. 决策链")
    lines.append("")
    lines.append("| 修订 | 决策 ID | 状态 | 审计通过 | 领先候选 | record_hash |")
    lines.append("|---|---|---|---|---|---|")
    for record in records:
        lines.append(_decision_row(record))
    lines.append("")
    lines.append("## 3. 算法审计事件（证据定位）")
    lines.append("")
    lines.append("每条事件均为 SHA-256 链式哈希，`previous_event_hash` 衔接前序事件。")
    lines.append("")
    for record in records:
        lines.append(f"### {record.result.decision_id}")
        lines.append(f"`algorithm_audit_root_hash` = `{record.result.algorithm_audit_root_hash or '—'}`")
        lines.append("")
        if record.result.algorithm_audit:
            lines.append("| 序号 | 阶段 | 规则 | 操作 | event_hash |")
            lines.append("|---|---|---|---|---|")
            lines.extend(_audit_rows(record))
        else:
            lines.append("（无审计事件）")
        lines.append("")
    if hub_report is not None:
        lines.append("## 4. Hub 报告锚点")
        lines.append("")
        lines.append(f"- `hub_run_id` = `{hub_report.hub_run_id}`")
        lines.append(f"- `report_hash` = `{hub_report.report_hash}`")
        lines.append(f"- `algorithm_audit_verified` = `{hub_report.algorithm_audit_verified}`")
        lines.append("")
    lines.append("## 5. 专家复核指引")
    lines.append("")
    lines.append("不要信任本报告的结论，直接对底层哈希复算：")
    lines.append("")
    lines.append("```bash")
    lines.append("python - <<'EOF'")
    lines.append("from second_perspective.decision.integrity import verify_chain, verify_record")
    lines.append("from second_perspective.audit.ledger import verify_algorithm_audit")
    lines.append("from second_perspective.hub.integrity import verify_hub_report")
    lines.append("# records / hub_report 从你的决策对象反序列化后传入")
    lines.append("print('chain:', verify_chain(records))")
    lines.append("print('record:', [verify_record(r) for r in records])")
    lines.append("print('audit:', [verify_algorithm_audit(r.result.algorithm_audit, r.result.algorithm_audit_root_hash) for r in records])")
    lines.append("EOF")
    lines.append("```")
    lines.append("")
    lines.append("关联本地运行日志（Layer 1）：日志中 `decision sealed` / `audit event appended` / ")
    lines.append("`hub report sealed` 三行所附哈希应与上表逐一对应，核对任一行被篡改都会破坏相应校验。")
    lines.append("")
    lines.append("## 6. 边界声明")
    lines.append("")
    lines.append("- 本报告为本地生成的展示层文件，**不构成签名审计记录**，不能单独作为合规证据。")
    lines.append("- 哈希校验只能证明记录未被篡改，**不能证明评估结论正确**；结论正确性属于人类审批者的裁量。")
    lines.append("- 复核证据的完整性受本地文件保管方式约束；如需防篡改介质，请接入签名/公证环节。")
    lines.append("")

    target = out_path or (out_dir / f"expert-review-{now[:10]}.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    return target