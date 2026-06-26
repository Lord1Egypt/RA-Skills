"""Human-readable output renderers."""

from __future__ import annotations

import json

from hkipo_next.contracts.discovery import DiscoveryResponse
from hkipo_next.contracts.decision_card import BatchResponse, DecisionCardResponse
from hkipo_next.contracts.errors import ErrorResponse
from hkipo_next.contracts.preferences import ProfileResponse, WatchlistResponse
from hkipo_next.contracts.review import (
    ReviewDetailResponse,
    ReviewExportResponse,
    ReviewListResponse,
    SuggestionDetailResponse,
    SuggestionImportResponse,
    SuggestionListResponse,
)
from hkipo_next.contracts.scoring import ParameterComparisonResponse, ParametersResponse, ScoreResponse
from hkipo_next.contracts.snapshot import SnapshotResponse


WINDOW_LABELS = {
    "deadline": "即将截止",
    "listing": "即将上市",
}


def render_discovery_response(response: DiscoveryResponse) -> str:
    data = response.data
    lines = [
        f"发现窗口: {WINDOW_LABELS[data.filter.window]}（未来 {data.filter.days} 天）",
        f"命中标的: {data.total_items}",
    ]

    if not data.items:
        lines.append("当前窗口内没有匹配的 IPO。")
    else:
        label = "截止" if data.filter.window == "deadline" else "上市"
        for item in data.items:
            parts = [f"- {item.name}"]
            if item.symbol:
                parts[0] = f"- {item.name} ({item.symbol})"
            target_date = item.deadline_date if data.filter.window == "deadline" else item.listing_date
            if target_date is not None:
                parts.append(f"{label}: {target_date.isoformat()}")
            if item.entry_fee_hkd is not None:
                parts.append(f"入场费: {item.entry_fee_hkd:,.0f} HKD")
            if item.data_status == "partial":
                parts.append("状态: 降级")
            lines.append(" | ".join(parts))

    if data.issues:
        lines.append("")
        lines.append(f"降级提示: {len(data.issues)} 项")
        for issue in data.issues:
            lines.append(f"- {issue.code}/{issue.source}: {issue.message}")

    lines.append("")
    lines.append(f"run_id: {response.meta.run_id}")
    lines.append(f"timestamp: {response.meta.timestamp.isoformat()}")
    lines.append(f"schema_version: {response.meta.schema_version}")
    lines.append(f"data_status: {response.meta.data_status}")
    return "\n".join(lines)


def render_error_response(response: ErrorResponse) -> str:
    lines = [f"{response.error.code}: {response.error.message}"]
    if response.error.details:
        lines.append(json.dumps(response.error.details, ensure_ascii=False, indent=2))
    lines.append(f"run_id: {response.meta.run_id}")
    lines.append(f"schema_version: {response.meta.schema_version}")
    lines.append(f"data_status: {response.meta.data_status}")
    return "\n".join(lines)


def render_snapshot_response(response: SnapshotResponse) -> str:
    data = response.data
    lines = [f"{data.company_name or '未知标的'} ({data.symbol})"]

    if data.offer_price_floor is not None or data.offer_price_ceiling is not None:
        lines.append(
            f"价格区间: {data.offer_price_floor or '-'} - {data.offer_price_ceiling or '-'} HKD"
        )
    if data.lot_size is not None:
        lines.append(f"每手股数: {data.lot_size}")
    if data.entry_fee_hkd is not None:
        lines.append(f"入场费: {data.entry_fee_hkd:,.2f} HKD")
    if data.deadline_date is not None:
        lines.append(f"截止日: {data.deadline_date.isoformat()}")
    if data.listing_date is not None:
        lines.append(f"上市日: {data.listing_date.isoformat()}")
    if data.industry:
        lines.append(f"行业: {data.industry}")
    if data.sponsors:
        lines.append(f"保荐人: {', '.join(data.sponsors)}")

    if data.quality is not None:
        lines.append(f"整体置信度: {data.quality.overall_confidence:.2f}")
        if data.quality.missing_fields:
            lines.append(f"缺失字段: {', '.join(data.quality.missing_fields)}")
        if data.quality.conflicts:
            lines.append(f"冲突字段: {', '.join(conflict.field_name for conflict in data.quality.conflicts)}")

    if data.issues:
        lines.append("")
        lines.append(f"降级提示: {len(data.issues)} 项")
        for issue in data.issues:
            lines.append(f"- {issue.code}/{issue.source}: {issue.message}")

    lines.append("")
    lines.append(f"run_id: {response.meta.run_id}")
    lines.append(f"timestamp: {response.meta.timestamp.isoformat()}")
    lines.append(f"schema_version: {response.meta.schema_version}")
    lines.append(f"data_status: {response.meta.data_status}")
    return "\n".join(lines)


def render_profile_response(response: ProfileResponse) -> str:
    profile = response.data.profile
    lines = [
        "当前 profile:",
        f"- 风险偏好: {profile.risk_profile}",
        f"- 默认输出格式: {profile.default_output_format}",
        f"- 预算上限: {profile.max_budget_hkd:,.2f} HKD",
        f"- 融资偏好: {profile.financing_preference}",
        f"- API Token: {'已配置' if profile.api_token_configured else '未配置'}",
        "",
        "来源追踪:",
    ]
    for field_name, source in response.data.sources.items():
        lines.append(f"- {field_name}: {source}")
    lines.extend(
        [
            "",
            f"config_file: {response.data.config_file}",
        ]
    )
    for note in response.data.notes:
        lines.append(f"note: {note}")
    lines.extend(
        [
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_watchlist_response(response: WatchlistResponse) -> str:
    lines = [
        f"watchlist 操作: {response.data.operation}",
        f"当前数量: {response.data.total_items}",
    ]
    if response.data.changed_symbols:
        lines.append(f"变更标的: {', '.join(response.data.changed_symbols)}")
    if response.data.symbols:
        lines.append("当前列表:")
        lines.extend(f"- {symbol}" for symbol in response.data.symbols)
    else:
        lines.append("当前列表为空。")
    lines.extend(
        [
            "",
            f"storage_path: {response.data.storage_path}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_review_list_response(response: ReviewListResponse) -> str:
    lines = [
        f"复盘记录数量: {response.data.total_items}",
        f"storage_path: {response.data.storage_path}",
    ]
    if response.data.items:
        lines.append("")
        for item in response.data.items:
            lines.append(
                (
                    f"- {item.created_at.isoformat()} | {item.symbol} | {item.command} | "
                    f"{item.decision} | score={item.score:.2f} | "
                    f"{item.parameter_version} | {item.data_status}"
                )
            )
    else:
        lines.append("当前没有复盘记录。")
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_review_export_response(response: ReviewExportResponse) -> str:
    lines = [
        f"复盘数据集已导出: {response.data.export_path}",
        f"导出记录数: {response.data.total_items}",
        f"storage_path: {response.data.storage_path}",
    ]
    if response.data.filters.from_date is not None:
        lines.append(f"from: {response.data.filters.from_date.isoformat()}")
    if response.data.filters.to_date is not None:
        lines.append(f"to: {response.data.filters.to_date.isoformat()}")
    if response.data.filters.limit is not None:
        lines.append(f"limit: {response.data.filters.limit}")
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_review_detail_response(response: ReviewDetailResponse) -> str:
    record = response.data.record
    lines = [
        f"record_id: {record.record_id}",
        f"symbol: {record.symbol}",
        f"command: {record.command}",
        f"created_at: {record.created_at.isoformat()}",
        f"decision: {record.decision}",
        f"score: {record.score:.2f}",
        f"parameter_version: {record.parameter_version}",
        f"data_status: {record.data_status}",
        "",
        "预测快照:",
        f"- decision: {record.prediction_payload.get('decision', record.decision)}",
        f"- score: {record.prediction_payload.get('score', record.score)}",
    ]
    if record.actual_result is not None:
        lines.extend(
            [
                "",
                "实际结果:",
                f"- allocated_lots: {record.actual_result.allocated_lots}",
                f"- listing_return_pct: {record.actual_result.listing_return_pct}",
                f"- exit_return_pct: {record.actual_result.exit_return_pct}",
                f"- realized_pnl_hkd: {record.actual_result.realized_pnl_hkd}",
                f"- exited_at: {record.actual_result.exited_at.isoformat() if record.actual_result.exited_at else None}",
                f"- notes: {record.actual_result.notes}",
                f"- actual_updated_at: {record.actual_updated_at.isoformat() if record.actual_updated_at else None}",
            ]
        )
    if record.variance_note is not None:
        lines.extend(
            [
                "",
                f"偏差说明: {record.variance_note}",
                f"variance_updated_at: {record.variance_updated_at.isoformat() if record.variance_updated_at else None}",
            ]
        )
    lines.extend(
        [
            "",
            f"修订历史: {len(response.data.revisions)}",
        ]
    )
    for revision in response.data.revisions:
        actual_bits = []
        if revision.actual_result is not None:
            actual_bits = [
                f"allocated_lots={revision.actual_result.allocated_lots}",
                f"listing_return_pct={revision.actual_result.listing_return_pct}",
                f"exit_return_pct={revision.actual_result.exit_return_pct}",
                f"realized_pnl_hkd={revision.actual_result.realized_pnl_hkd}",
            ]
        lines.append(
            (
                f"- {revision.updated_at.isoformat()} | revision_id={revision.revision_id} | "
                + " | ".join(actual_bits + [f"variance_note={revision.variance_note}"])
            )
        )
    lines.extend(
        [
            "",
            f"storage_path: {response.data.storage_path}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_suggestion_import_response(response: SuggestionImportResponse) -> str:
    lines = [
        f"suggestions 导入完成: {response.data.source_file}",
        f"imported_count: {response.data.imported_count}",
        f"storage_path: {response.data.storage_path}",
    ]
    for item in response.data.items:
        lines.append(
            f"- {item.suggestion_id} | {item.impact_scope} | {item.title} | {item.status}"
        )
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_suggestion_list_response(response: SuggestionListResponse) -> str:
    lines = [
        f"suggestions 数量: {response.data.total_items}",
        f"storage_path: {response.data.storage_path}",
    ]
    for item in response.data.items:
        lines.append(
            (
                f"- {item.suggestion_id} | {item.source} | {item.impact_scope} | "
                f"{item.title} | status={item.status}"
            )
        )
        lines.append(f"  summary: {item.summary}")
        if item.record_id is not None:
            lines.append(f"  record_id: {item.record_id}")
        if item.batch_id is not None:
            lines.append(f"  batch_id: {item.batch_id}")
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_suggestion_detail_response(response: SuggestionDetailResponse) -> str:
    suggestion = response.data.suggestion
    lines = [
        f"suggestion_id: {suggestion.suggestion_id}",
        f"title: {suggestion.title}",
        f"source: {suggestion.source}",
        f"impact_scope: {suggestion.impact_scope}",
        f"status: {suggestion.status}",
        f"current_parameter_version: {response.data.current_parameter_version}",
        f"summary: {suggestion.summary}",
    ]
    if suggestion.rationale:
        lines.append(f"rationale: {suggestion.rationale}")
    lines.extend(["", "当前差异预览:"])
    if response.data.preview_changes:
        for change in response.data.preview_changes:
            lines.append(
                (
                    f"- {change.field_path}: {change.current_value} -> {change.suggested_value} | "
                    f"will_change={change.will_change} | reason={change.reason}"
                )
            )
    else:
        lines.append("- 无结构化字段变更")
    if response.data.adoption is not None:
        adoption = response.data.adoption
        lines.extend(
            [
                "",
                f"决策: {adoption.decision}",
                f"decided_at: {adoption.decided_at.isoformat()}",
                f"before_version: {adoption.before_parameter_version}",
                f"after_version: {adoption.after_parameter_version}",
                f"decision_note: {adoption.decision_note}",
            ]
        )
        lines.extend(["", "已记录变更:"])
        if adoption.applied_changes:
            for change in adoption.applied_changes:
                lines.append(
                    (
                        f"- {change.field_path}: {change.current_value} -> {change.suggested_value} | "
                        f"will_change={change.will_change} | reason={change.reason}"
                    )
                )
        else:
            lines.append("- 无结构化字段变更")
    lines.extend(
        [
            "",
            f"storage_path: {response.data.storage_path}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_parameters_response(response: ParametersResponse) -> str:
    lines = [
        f"参数操作: {response.data.operation}",
        f"active_version: {response.data.active_version or '-'}",
    ]
    if response.data.parameter_set is not None:
        parameter_set = response.data.parameter_set
        lines.extend(
            [
                f"版本: {parameter_set.parameter_version}",
                f"名称: {parameter_set.name}",
                f"创建时间: {parameter_set.created_at.isoformat()}",
                f"是否 active: {'yes' if parameter_set.is_active else 'no'}",
                "权重:",
                (
                    f"- quality={parameter_set.weights.snapshot_quality:.2f}, "
                    f"affordability={parameter_set.weights.affordability:.2f}, "
                    f"pricing={parameter_set.weights.pricing_stability:.2f}, "
                    f"sponsor={parameter_set.weights.sponsor_support:.2f}, "
                    f"cost={parameter_set.weights.cost_efficiency:.2f}"
                ),
            ]
        )
    if response.data.versions:
        lines.append("版本列表:")
        for record in response.data.versions:
            marker = "*" if record.is_active else "-"
            lines.append(f"{marker} {record.parameter_version} | {record.name} | {record.created_at.isoformat()}")
    lines.extend(
        [
            "",
            f"storage_path: {response.data.storage_path}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_parameter_comparison_response(response: ParameterComparisonResponse) -> str:
    lines = [
        f"参数对比: {response.data.symbol}",
        (
            f"{response.data.baseline_version}: {response.data.baseline_score:.2f}"
            f" ({response.data.baseline_action})"
        ),
        (
            f"{response.data.candidate_version}: {response.data.candidate_score:.2f}"
            f" ({response.data.candidate_action})"
        ),
        f"score_delta: {response.data.score_delta:+.2f}",
        f"action_changed: {'yes' if response.data.action_changed else 'no'}",
        f"risk_profile: {response.data.risk_profile}",
        "关键因子变化:",
    ]
    for delta in response.data.factor_deltas:
        lines.append(
            f"- {delta.name}: {delta.baseline:.2f} -> {delta.candidate:.2f} ({delta.delta:+.2f})"
        )
    lines.extend(
        [
            "",
            f"storage_path: {response.data.storage_path}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_score_response(response: ScoreResponse) -> str:
    action_labels = {
        "participate": "参与",
        "cautious": "谨慎参与",
        "pass": "放弃",
    }
    data = response.data
    lines = [
        f"评分结果: {data.symbol}",
        f"总分: {data.score:.2f}",
        f"建议动作: {action_labels.get(data.action, data.action)}",
        f"参数版本: {data.parameter_version}",
        f"风险偏好: {data.risk_profile}",
    ]
    if data.snapshot_overall_confidence is not None:
        lines.append(f"快照置信度: {data.snapshot_overall_confidence:.2f}")
    lines.extend(["", "因子贡献:"])
    for factor in data.factors:
        lines.append(
            f"- {factor.name}: raw={factor.raw_score:.2f}, contribution={factor.contribution:.2f} | {factor.reason}"
        )
    lines.extend(
        [
            "",
            "成本拆解:",
            f"- 手续费: {data.cost_breakdown.handling_fee_hkd:.2f} HKD",
            f"- 融资成本: {data.cost_breakdown.financing_cost_hkd:.2f} HKD",
            f"- 资金占用成本: {data.cost_breakdown.opportunity_cost_hkd:.2f} HKD",
            f"- 总成本: {data.cost_breakdown.total_cost_hkd:.2f} HKD",
            f"- 成本占比: {data.cost_breakdown.cost_ratio_pct:.2f}%",
            "",
            "关键假设:",
        ]
    )
    for assumption in data.assumptions:
        lines.append(f"- {assumption}")
    lines.extend(
        [
            "",
            f"风险披露: {data.risk_disclosure}",
        ]
    )
    if data.source_issue_count:
        lines.append(f"源数据提示: {data.source_issue_count} 项，结果按最小可用路径生成。")
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"rule_version: {response.meta.rule_version}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_decision_card_response(response: DecisionCardResponse) -> str:
    data = response.data
    lines = [
        f"决策卡: {data.symbol}",
        f"建议动作: {data.decision}",
        f"Headline: {data.headline}",
        f"分数: {data.score:.2f}",
        f"参数版本: {data.parameter_version}",
        f"风险偏好: {data.risk_profile}",
        f"仓位建议: {data.position_suggestion.position_size_pct:.2f}% "
        f"({data.position_suggestion.suggested_budget_hkd:.2f} HKD, {data.position_suggestion.subscription_mode})",
        (
            f"退出阈值: 止盈 {data.exit_plan.take_profit_pct:.2f}% | "
            f"止损 {data.exit_plan.stop_loss_pct:.2f}% | "
            f"最长持有 {data.exit_plan.max_holding_days} 天"
        ),
        f"退出说明: {data.exit_plan.note}",
        "关键理由:",
    ]
    lines.extend(f"- {reason}" for reason in data.top_reasons)
    lines.extend(
        [
            "",
            f"风险披露: {data.risk_disclosure}",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"rule_version: {response.meta.rule_version}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)


def render_batch_response(response: BatchResponse) -> str:
    data = response.data
    lines = [
        f"批处理来源: {data.source}",
        f"总数: {data.summary.total_items}",
        f"成功: {data.summary.success_count}",
        f"部分降级: {data.summary.partial_count}",
        f"失败: {data.summary.failure_count}",
        f"active_parameter_version: {data.active_parameter_version or '-'}",
        f"risk_profile: {data.risk_profile}",
        "",
        "批处理结果:",
    ]
    for item in data.items:
        if item.ok and item.decision_card is not None:
            lines.append(
                f"- {item.symbol}: {item.decision_card.decision} | "
                f"score={item.decision_card.score:.2f} | status={item.data_status}"
            )
        elif item.error is not None:
            lines.append(
                f"- {item.symbol}: {item.error.code} | {item.error.message} | status={item.data_status}"
            )
    lines.extend(
        [
            "",
            f"run_id: {response.meta.run_id}",
            f"timestamp: {response.meta.timestamp.isoformat()}",
            f"rule_version: {response.meta.rule_version}",
            f"schema_version: {response.meta.schema_version}",
            f"data_status: {response.meta.data_status}",
        ]
    )
    return "\n".join(lines)
