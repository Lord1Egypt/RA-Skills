"""Markdown rendering helpers."""

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


def render_discovery_markdown(response: DiscoveryResponse) -> str:
    lines = [
        "# IPO Discovery Export",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        "",
        "| Symbol | Name | Deadline | Listing | Entry Fee (HKD) | Status |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]

    for item in response.data.items:
        lines.append(
            "| {symbol} | {name} | {deadline} | {listing} | {entry_fee} | {status} |".format(
                symbol=item.symbol or "-",
                name=item.name,
                deadline=item.deadline_date.isoformat() if item.deadline_date else "-",
                listing=item.listing_date.isoformat() if item.listing_date else "-",
                entry_fee=f"{item.entry_fee_hkd:,.2f}" if item.entry_fee_hkd is not None else "-",
                status=item.data_status,
            )
        )

    if response.data.issues:
        lines.extend(["", "## Issues", ""])
        for issue in response.data.issues:
            lines.append(f"- `{issue.code}` `{issue.source}`: {issue.message}")

    return "\n".join(lines)


def render_snapshot_markdown(response: SnapshotResponse) -> str:
    data = response.data
    lines = [
        "# IPO Snapshot Export",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        "",
        f"## {data.company_name or '未知标的'} (`{data.symbol}`)",
        "",
        "| Field | Value | Selected Source |",
        "| --- | --- | --- |",
    ]

    field_source_map = {item.field_name: item.source for item in data.field_sources}
    rows = [
        ("industry", data.industry),
        ("sponsors", ", ".join(data.sponsors) if data.sponsors else None),
        ("offer_price_floor", data.offer_price_floor),
        ("offer_price_ceiling", data.offer_price_ceiling),
        ("lot_size", data.lot_size),
        ("entry_fee_hkd", data.entry_fee_hkd),
        ("deadline_date", data.deadline_date.isoformat() if data.deadline_date else None),
        ("listing_date", data.listing_date.isoformat() if data.listing_date else None),
    ]
    for field_name, value in rows:
        lines.append(
            f"| {field_name} | {value if value not in (None, '') else '-'} | {field_source_map.get(field_name, '-')} |"
        )

    if data.quality is not None:
        lines.extend(
            [
                "",
                "## Quality",
                "",
                f"- overall_confidence: `{data.quality.overall_confidence:.2f}`",
                f"- missing_fields: `{', '.join(data.quality.missing_fields) if data.quality.missing_fields else 'none'}`",
                f"- conflict_fields: `{', '.join(conflict.field_name for conflict in data.quality.conflicts) if data.quality.conflicts else 'none'}`",
            ]
        )

    if data.issues:
        lines.extend(["", "## Issues", ""])
        for issue in data.issues:
            lines.append(f"- `{issue.code}` `{issue.source}`: {issue.message}")

    return "\n".join(lines)


def render_error_markdown(response: ErrorResponse) -> str:
    details = json.dumps(response.error.details, ensure_ascii=False, indent=2) if response.error.details else "{}"
    return "\n".join(
        [
            "# hkipo-next Error",
            "",
            f"- code: `{response.error.code}`",
            f"- run_id: `{response.meta.run_id}`",
            f"- timestamp: `{response.meta.timestamp.isoformat()}`",
            f"- schema_version: `{response.meta.schema_version}`",
            f"- data_status: `{response.meta.data_status}`",
            "",
            response.error.message,
            "",
            "```json",
            details,
            "```",
        ]
    )


def render_profile_markdown(response: ProfileResponse) -> str:
    profile = response.data.profile
    lines = [
        "# hkipo-next Profile",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        "",
        "## Effective Profile",
        "",
        f"- risk_profile: `{profile.risk_profile}`",
        f"- default_output_format: `{profile.default_output_format}`",
        f"- max_budget_hkd: `{profile.max_budget_hkd:.2f}`",
        f"- financing_preference: `{profile.financing_preference}`",
        f"- api_token_configured: `{str(profile.api_token_configured).lower()}`",
        "",
        "## Source Trace",
        "",
    ]
    for field_name, source in response.data.sources.items():
        lines.append(f"- `{field_name}`: `{source}`")
    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    for note in response.data.notes:
        lines.append(f"- {note}")
    lines.extend(
        [
            "",
            f"`config_file`: `{response.data.config_file}`",
        ]
    )
    return "\n".join(lines)


def render_watchlist_markdown(response: WatchlistResponse) -> str:
    lines = [
        "# hkipo-next Watchlist",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- operation: `{response.data.operation}`",
        f"- total_items: `{response.data.total_items}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
    ]
    if response.data.changed_symbols:
        lines.extend(["## Changed Symbols", ""])
        for symbol in response.data.changed_symbols:
            lines.append(f"- `{symbol}`")
        lines.append("")
    lines.extend(["## Symbols", ""])
    if response.data.symbols:
        for symbol in response.data.symbols:
            lines.append(f"- `{symbol}`")
    else:
        lines.append("- _empty_")
    return "\n".join(lines)


def render_review_list_markdown(response: ReviewListResponse) -> str:
    lines = [
        "# hkipo-next Review History",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- total_items: `{response.data.total_items}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
        "| Created At | Symbol | Command | Decision | Score | Parameter Version | Status |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for item in response.data.items:
        lines.append(
            (
                f"| {item.created_at.isoformat()} | {item.symbol} | {item.command} | "
                f"{item.decision} | {item.score:.2f} | {item.parameter_version} | {item.data_status} |"
            )
        )
    return "\n".join(lines)


def render_review_export_markdown(response: ReviewExportResponse) -> str:
    lines = [
        "# hkipo-next Review Export",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- export_path: `{response.data.export_path}`",
        f"- total_items: `{response.data.total_items}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
    ]
    if response.data.filters.from_date is not None:
        lines.append(f"- from: `{response.data.filters.from_date.isoformat()}`")
    if response.data.filters.to_date is not None:
        lines.append(f"- to: `{response.data.filters.to_date.isoformat()}`")
    if response.data.filters.limit is not None:
        lines.append(f"- limit: `{response.data.filters.limit}`")
    return "\n".join(lines)


def render_review_detail_markdown(response: ReviewDetailResponse) -> str:
    record = response.data.record
    lines = [
        "# hkipo-next Review Detail",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- record_id: `{record.record_id}`",
        f"- symbol: `{record.symbol}`",
        f"- command: `{record.command}`",
        f"- created_at: `{record.created_at.isoformat()}`",
        f"- parameter_version: `{record.parameter_version}`",
        "",
        "## Prediction",
        "",
        f"- decision: `{record.decision}`",
        f"- score: `{record.score:.2f}`",
        "",
    ]
    if record.actual_result is not None:
        lines.extend(
            [
                "## Actual Result",
                "",
                f"- allocated_lots: `{record.actual_result.allocated_lots}`",
                f"- listing_return_pct: `{record.actual_result.listing_return_pct}`",
                f"- exit_return_pct: `{record.actual_result.exit_return_pct}`",
                f"- realized_pnl_hkd: `{record.actual_result.realized_pnl_hkd}`",
                f"- exited_at: `{record.actual_result.exited_at.isoformat() if record.actual_result.exited_at else None}`",
                f"- notes: `{record.actual_result.notes}`",
                f"- actual_updated_at: `{record.actual_updated_at.isoformat() if record.actual_updated_at else None}`",
                "",
            ]
        )
    if record.variance_note is not None:
        lines.extend(
            [
                "## Variance",
                "",
                record.variance_note,
                "",
                f"`variance_updated_at`: `{record.variance_updated_at.isoformat() if record.variance_updated_at else None}`",
                "",
            ]
        )
    lines.extend(["## Revisions", ""])
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
                f"- `{revision.updated_at.isoformat()}` `{revision.revision_id}` "
                + " ".join(f"`{bit}`" for bit in actual_bits)
                + f" `variance_note={revision.variance_note}`"
            )
        )
    lines.extend(["", f"`storage_path`: `{response.data.storage_path}`"])
    return "\n".join(lines)


def render_suggestion_import_markdown(response: SuggestionImportResponse) -> str:
    lines = [
        "# hkipo-next Suggestion Import",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- source_file: `{response.data.source_file}`",
        f"- imported_count: `{response.data.imported_count}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
    ]
    for item in response.data.items:
        lines.append(f"- `{item.suggestion_id}` `{item.impact_scope}` `{item.status}` {item.title}")
    return "\n".join(lines)


def render_suggestion_list_markdown(response: SuggestionListResponse) -> str:
    lines = [
        "# hkipo-next Suggestions",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- total_items: `{response.data.total_items}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
    ]
    for item in response.data.items:
        lines.extend(
            [
                f"## {item.title}",
                "",
                f"- suggestion_id: `{item.suggestion_id}`",
                f"- source: `{item.source}`",
                f"- impact_scope: `{item.impact_scope}`",
                f"- status: `{item.status}`",
                f"- record_id: `{item.record_id}`",
                f"- batch_id: `{item.batch_id}`",
                "",
                item.summary,
                "",
            ]
        )
    return "\n".join(lines)


def render_suggestion_detail_markdown(response: SuggestionDetailResponse) -> str:
    suggestion = response.data.suggestion
    lines = [
        "# hkipo-next Suggestion Detail",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- suggestion_id: `{suggestion.suggestion_id}`",
        f"- source: `{suggestion.source}`",
        f"- impact_scope: `{suggestion.impact_scope}`",
        f"- status: `{suggestion.status}`",
        f"- current_parameter_version: `{response.data.current_parameter_version}`",
        "",
        f"## {suggestion.title}",
        "",
        suggestion.summary,
        "",
    ]
    if suggestion.rationale:
        lines.extend(["## Rationale", "", suggestion.rationale, ""])
    lines.extend(["## Preview Changes", ""])
    if response.data.preview_changes:
        for change in response.data.preview_changes:
            lines.append(
                (
                    f"- `{change.field_path}`: `{change.current_value}` -> `{change.suggested_value}` "
                    f"`will_change={str(change.will_change).lower()}` `reason={change.reason}`"
                )
            )
    else:
        lines.append("- No structured field changes.")
    if response.data.adoption is not None:
        adoption = response.data.adoption
        lines.extend(
            [
                "",
                "## Adoption",
                "",
                f"- decision: `{adoption.decision}`",
                f"- decided_at: `{adoption.decided_at.isoformat()}`",
                f"- before_version: `{adoption.before_parameter_version}`",
                f"- after_version: `{adoption.after_parameter_version}`",
                f"- decision_note: `{adoption.decision_note}`",
            ]
        )
        lines.extend(["", "## Recorded Adoption Changes", ""])
        if adoption.applied_changes:
            for change in adoption.applied_changes:
                lines.append(
                    (
                        f"- `{change.field_path}`: `{change.current_value}` -> `{change.suggested_value}` "
                        f"`will_change={str(change.will_change).lower()}` `reason={change.reason}`"
                    )
                )
        else:
            lines.append("- No structured field changes.")
    lines.extend(["", f"`storage_path`: `{response.data.storage_path}`"])
    return "\n".join(lines)


def render_parameters_markdown(response: ParametersResponse) -> str:
    lines = [
        "# hkipo-next Parameter Versions",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- operation: `{response.data.operation}`",
        f"- active_version: `{response.data.active_version or '-'}`",
        f"- storage_path: `{response.data.storage_path}`",
        "",
    ]
    if response.data.parameter_set is not None:
        parameter_set = response.data.parameter_set
        lines.extend(
            [
                "## Selected Version",
                "",
                f"- version: `{parameter_set.parameter_version}`",
                f"- name: `{parameter_set.name}`",
                f"- created_at: `{parameter_set.created_at.isoformat()}`",
                f"- is_active: `{str(parameter_set.is_active).lower()}`",
                "",
            ]
        )
    if response.data.versions:
        lines.extend(["## Versions", ""])
        for record in response.data.versions:
            active_label = "active" if record.is_active else "inactive"
            lines.append(f"- `{record.parameter_version}` `{record.name}` `{active_label}`")
    return "\n".join(lines)


def render_parameter_comparison_markdown(response: ParameterComparisonResponse) -> str:
    lines = [
        "# hkipo-next Parameter Comparison",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- symbol: `{response.data.symbol}`",
        f"- active_version: `{response.data.active_version or '-'}`",
        f"- risk_profile: `{response.data.risk_profile}`",
        "",
        "| Version | Score | Action |",
        "| --- | ---: | --- |",
        f"| {response.data.baseline_version} | {response.data.baseline_score:.2f} | {response.data.baseline_action} |",
        f"| {response.data.candidate_version} | {response.data.candidate_score:.2f} | {response.data.candidate_action} |",
        "",
        f"`score_delta`: `{response.data.score_delta:+.2f}`",
        "",
        "## Factor Deltas",
        "",
    ]
    for delta in response.data.factor_deltas:
        lines.append(
            f"- `{delta.name}`: `{delta.baseline:.2f}` -> `{delta.candidate:.2f}` (`{delta.delta:+.2f}`)"
        )
    lines.extend(
        [
            "",
            f"`storage_path`: `{response.data.storage_path}`",
        ]
    )
    return "\n".join(lines)


def render_score_markdown(response: ScoreResponse) -> str:
    data = response.data
    lines = [
        "# hkipo-next Score",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- rule_version: `{response.meta.rule_version}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- symbol: `{data.symbol}`",
        f"- parameter_version: `{data.parameter_version}`",
        f"- risk_profile: `{data.risk_profile}`",
        f"- score: `{data.score:.2f}`",
        f"- action: `{data.action}`",
        "",
        "## Factors",
        "",
        "| Factor | Raw | Contribution | Reason |",
        "| --- | ---: | ---: | --- |",
    ]
    for factor in data.factors:
        lines.append(
            f"| {factor.name} | {factor.raw_score:.2f} | {factor.contribution:.2f} | {factor.reason} |"
        )
    lines.extend(
        [
            "",
            "## Cost Breakdown",
            "",
            f"- handling_fee_hkd: `{data.cost_breakdown.handling_fee_hkd:.2f}`",
            f"- financing_cost_hkd: `{data.cost_breakdown.financing_cost_hkd:.2f}`",
            f"- opportunity_cost_hkd: `{data.cost_breakdown.opportunity_cost_hkd:.2f}`",
            f"- total_cost_hkd: `{data.cost_breakdown.total_cost_hkd:.2f}`",
            f"- cost_ratio_pct: `{data.cost_breakdown.cost_ratio_pct:.2f}`",
            "",
            "## Assumptions",
            "",
        ]
    )
    for assumption in data.assumptions:
        lines.append(f"- {assumption}")
    lines.extend(
        [
            "",
            "## Risk Disclosure",
            "",
            data.risk_disclosure,
        ]
    )
    if data.source_issue_count:
        lines.extend(
            [
                "",
                f"`source_issue_count`: `{data.source_issue_count}`",
            ]
    )
    return "\n".join(lines)


def render_decision_card_markdown(response: DecisionCardResponse) -> str:
    data = response.data
    lines = [
        "# hkipo-next Decision Card",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- rule_version: `{response.meta.rule_version}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- symbol: `{data.symbol}`",
        f"- decision: `{data.decision}`",
        f"- score: `{data.score:.2f}`",
        f"- parameter_version: `{data.parameter_version}`",
        f"- risk_profile: `{data.risk_profile}`",
        "",
        f"## {data.headline}",
        "",
        "### Position",
        "",
        f"- position_size_pct: `{data.position_suggestion.position_size_pct:.2f}`",
        f"- suggested_budget_hkd: `{data.position_suggestion.suggested_budget_hkd:.2f}`",
        f"- subscription_mode: `{data.position_suggestion.subscription_mode}`",
        "",
        "### Exit Plan",
        "",
        f"- take_profit_pct: `{data.exit_plan.take_profit_pct:.2f}`",
        f"- stop_loss_pct: `{data.exit_plan.stop_loss_pct:.2f}`",
        f"- max_holding_days: `{data.exit_plan.max_holding_days}`",
        f"- note: {data.exit_plan.note}",
        "",
        "### Top Reasons",
        "",
    ]
    for reason in data.top_reasons:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            "### Risk Disclosure",
            "",
            data.risk_disclosure,
        ]
    )
    return "\n".join(lines)


def render_batch_markdown(response: BatchResponse) -> str:
    data = response.data
    lines = [
        "# hkipo-next Batch",
        "",
        f"- run_id: `{response.meta.run_id}`",
        f"- timestamp: `{response.meta.timestamp.isoformat()}`",
        f"- rule_version: `{response.meta.rule_version}`",
        f"- schema_version: `{response.meta.schema_version}`",
        f"- data_status: `{response.meta.data_status}`",
        f"- source: `{data.source}`",
        f"- active_parameter_version: `{data.active_parameter_version or '-'}`",
        f"- risk_profile: `{data.risk_profile}`",
        "",
        "| Symbol | OK | Decision | Score | Status | Error |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for item in data.items:
        decision = item.decision_card.decision if item.decision_card is not None else "-"
        score = f"{item.decision_card.score:.2f}" if item.decision_card is not None else "-"
        error = f"{item.error.code}: {item.error.message}" if item.error is not None else "-"
        lines.append(
            f"| {item.symbol} | {str(item.ok).lower()} | {decision} | {score} | {item.data_status} | {error} |"
        )
    lines.extend(
        [
            "",
            f"`total_items`: `{data.summary.total_items}`",
            f"`success_count`: `{data.summary.success_count}`",
            f"`partial_count`: `{data.summary.partial_count}`",
            f"`failure_count`: `{data.summary.failure_count}`",
        ]
    )
    return "\n".join(lines)
