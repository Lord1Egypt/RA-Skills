"""Review history orchestration for persistence and export."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
from copy import deepcopy

from hkipo_next.config.parameters import ParameterRepository
from hkipo_next.contracts.decision_card import BatchResponse, DecisionCardData, DecisionCardResponse
from hkipo_next.contracts.errors import AppError, AppException
from hkipo_next.contracts.review import (
    ImportedSuggestion,
    OpenClawSuggestionFile,
    ResolvedSuggestionChange,
    ReviewActualResult,
    ReviewDetailData,
    ReviewExportData,
    ReviewExportFilters,
    ReviewExportResponse,
    ReviewListData,
    ReviewRecord,
    ReviewSuggestion,
    SuggestionAdoption,
    SuggestionDetailData,
    SuggestionImportData,
    SuggestionListData,
)
from hkipo_next.contracts.scoring import ParameterSet, ParameterVersion, ScoreResponse, ScoreSummary
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.storage.review_store import ReviewStore
from hkipo_next.utils.output import export_rendered_output


class ReviewService:
    """Persist and export review-friendly history records."""

    def __init__(self, store: ReviewStore, *, review_artifacts_dir: str | Path):
        self.store = store
        self.review_artifacts_dir = Path(review_artifacts_dir)
        self.store.initialize()

    def record_score_response(self, response: ScoreResponse) -> ReviewRecord:
        record = self._record_from_score(
            command="score",
            run_id=response.meta.run_id,
            batch_id=None,
            summary=response.data,
            created_at=response.meta.timestamp,
            data_status=response.meta.data_status,
            rule_version=response.meta.rule_version,
            schema_version=response.meta.schema_version,
        )
        self.store.save_records([record])
        return record

    def record_decision_card_response(self, response: DecisionCardResponse) -> ReviewRecord:
        record = self._record_from_decision_card(
            command="decision-card",
            run_id=response.meta.run_id,
            batch_id=None,
            created_at=response.meta.timestamp,
            data_status=response.meta.data_status,
            rule_version=response.meta.rule_version,
            schema_version=response.meta.schema_version,
            data=response.data,
        )
        self.store.save_records([record])
        return record

    def record_batch_response(self, response: BatchResponse) -> list[ReviewRecord]:
        records = [
            self._record_from_decision_card(
                command="batch",
                run_id=response.meta.run_id,
                batch_id=response.meta.run_id,
                created_at=response.meta.timestamp,
                data_status=item.data_status,
                rule_version=response.meta.rule_version,
                schema_version=response.meta.schema_version,
                data=item.decision_card,
            )
            for item in response.data.items
            if item.ok and item.decision_card is not None
        ]
        if records:
            self.store.save_records(records)
        return records

    def list_records(
        self,
        *,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int | None = None,
    ) -> ReviewListData:
        items = self.store.list_records(from_date=from_date, to_date=to_date, limit=limit)
        return ReviewListData(
            total_items=len(items),
            items=items,
            storage_path=str(self.store.path),
        )

    def get_record_detail(self, *, record_id: str) -> ReviewDetailData:
        record = self.store.get_record(record_id)
        if record is None:
            raise KeyError(record_id)
        return ReviewDetailData(
            record=record,
            revisions=self.store.list_revisions(record_id),
            storage_path=str(self.store.path),
        )

    def update_record_detail(
        self,
        *,
        record_id: str,
        actual_result: ReviewActualResult | None,
        variance_note: str | None,
        updated_at: datetime,
    ) -> ReviewDetailData:
        record = self.store.update_record(
            record_id=record_id,
            actual_result=actual_result,
            variance_note=variance_note,
            updated_at=updated_at,
        )
        return ReviewDetailData(
            record=record,
            revisions=self.store.list_revisions(record_id),
            storage_path=str(self.store.path),
        )

    def export_records(
        self,
        *,
        run_context: RunContext,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int | None = None,
        output_path: str | None = None,
    ) -> ReviewExportData:
        records = self.store.list_records(from_date=from_date, to_date=to_date, limit=limit)
        target = Path(output_path) if output_path is not None else self.review_artifacts_dir / "review-input.json"
        filters = ReviewExportFilters(
            from_date=from_date,
            to_date=to_date,
            limit=limit,
        )
        data = ReviewExportData(
            generated_at=run_context.timestamp,
            export_path=str(target),
            filters=filters,
            total_items=len(records),
            records=records,
            storage_path=str(self.store.path),
        )
        envelope = ReviewExportResponse(
            data=data,
            meta=run_context.meta(
                degraded=False,
                data_status="complete",
            ),
        )
        export_rendered_output(render_model_as_json(envelope), str(target))
        return data

    def import_suggestions(
        self,
        *,
        source_file: str | Path,
        imported_at: datetime,
    ) -> SuggestionImportData:
        source_path = Path(source_file)
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        suggestion_file = OpenClawSuggestionFile.model_validate(payload)
        suggestions = [
            self._build_suggestion(
                source=suggestion_file.source,
                default_batch_id=suggestion_file.batch_id,
                imported_at=imported_at,
                suggestion=item,
            )
            for item in suggestion_file.suggestions
        ]
        self.store.save_suggestions(suggestions)
        return SuggestionImportData(
            source_file=str(source_path),
            imported_count=len(suggestions),
            items=suggestions,
            storage_path=str(self.store.path),
        )

    def list_suggestions(
        self,
        *,
        record_id: str | None = None,
        batch_id: str | None = None,
        status: str | None = None,
    ) -> SuggestionListData:
        items = self.store.list_suggestions(record_id=record_id, batch_id=batch_id, status=status)
        return SuggestionListData(
            total_items=len(items),
            items=items,
            storage_path=str(self.store.path),
        )

    def get_suggestion_detail(
        self,
        *,
        suggestion_id: str,
        parameter_repository: ParameterRepository,
    ) -> SuggestionDetailData:
        suggestion = self.store.get_suggestion(suggestion_id)
        if suggestion is None:
            raise KeyError(suggestion_id)
        active = parameter_repository.get_active()
        return SuggestionDetailData(
            suggestion=suggestion,
            current_parameter_version=active.parameter_version if active is not None else None,
            preview_changes=self._resolve_preview_changes(suggestion, active),
            adoption=self.store.get_adoption(suggestion_id),
            storage_path=str(self.store.path),
        )

    def accept_suggestion_detail(
        self,
        *,
        suggestion_id: str,
        parameter_repository: ParameterRepository,
        decided_at: datetime,
        decision_note: str | None,
    ) -> SuggestionDetailData:
        suggestion = self.store.get_suggestion(suggestion_id)
        if suggestion is None:
            raise KeyError(suggestion_id)
        adoption = self.store.get_adoption(suggestion_id)
        if adoption is not None:
            if adoption.decision == "accepted":
                return self.get_suggestion_detail(
                    suggestion_id=suggestion_id,
                    parameter_repository=parameter_repository,
                )
            raise AppException(AppError.rule("该 suggestion 已被拒绝，不能再次接受。"))

        active = parameter_repository.get_active()
        preview_changes = self._resolve_preview_changes(suggestion, active)
        before_version = active.parameter_version if active is not None else None
        after_version = before_version

        if suggestion.impact_scope == "parameter-set":
            if active is None:
                raise AppException(AppError.arg("当前没有 active 参数版本，无法应用 suggestion。"))
            invalid_paths = [change.field_path for change in preview_changes if change.reason is not None]
            if invalid_paths:
                raise AppException(
                    AppError.rule(
                        "suggestion 包含无法应用的参数路径。",
                        details={"field_paths": invalid_paths},
                    )
                )
            if any(change.will_change for change in preview_changes):
                new_parameter_set = self._build_updated_parameter_set(
                    active,
                    preview_changes,
                    suggestion_id=suggestion_id,
                )
                new_version = parameter_repository.save(new_parameter_set, activate=True)
                after_version = new_version.parameter_version

        adoption = SuggestionAdoption(
            suggestion_id=suggestion_id,
            decision="accepted",
            decided_at=decided_at,
            decision_note=decision_note,
            before_parameter_version=before_version,
            after_parameter_version=after_version,
            applied_changes=preview_changes,
        )
        self.store.save_adoption(adoption)
        self.store.update_suggestion_status(suggestion_id, "applied")
        return self.get_suggestion_detail(
            suggestion_id=suggestion_id,
            parameter_repository=parameter_repository,
        )

    def reject_suggestion_detail(
        self,
        *,
        suggestion_id: str,
        parameter_repository: ParameterRepository,
        decided_at: datetime,
        decision_note: str | None,
    ) -> SuggestionDetailData:
        suggestion = self.store.get_suggestion(suggestion_id)
        if suggestion is None:
            raise KeyError(suggestion_id)
        adoption = self.store.get_adoption(suggestion_id)
        if adoption is not None:
            if adoption.decision == "rejected":
                return self.get_suggestion_detail(
                    suggestion_id=suggestion_id,
                    parameter_repository=parameter_repository,
                )
            raise AppException(AppError.rule("该 suggestion 已被接受，不能再次拒绝。"))

        active = parameter_repository.get_active()
        preview_changes = self._resolve_preview_changes(suggestion, active)
        adoption = SuggestionAdoption(
            suggestion_id=suggestion_id,
            decision="rejected",
            decided_at=decided_at,
            decision_note=decision_note,
            before_parameter_version=active.parameter_version if active is not None else None,
            after_parameter_version=active.parameter_version if active is not None else None,
            applied_changes=preview_changes,
        )
        self.store.save_adoption(adoption)
        self.store.update_suggestion_status(suggestion_id, "rejected")
        return self.get_suggestion_detail(
            suggestion_id=suggestion_id,
            parameter_repository=parameter_repository,
        )

    @staticmethod
    def _record_from_score(
        *,
        command: str,
        run_id: str,
        batch_id: str | None,
        summary: ScoreSummary,
        created_at: datetime,
        data_status: str,
        rule_version: str,
        schema_version: str,
    ) -> ReviewRecord:
        return ReviewRecord(
            record_id=f"{run_id}:{command}:{summary.symbol}",
            command=command,
            command_run_id=run_id,
            batch_id=batch_id,
            symbol=summary.symbol,
            created_at=created_at,
            parameter_version=summary.parameter_version,
            parameter_name=summary.parameter_name,
            risk_profile=summary.risk_profile,
            decision=summary.action,
            score=summary.score,
            data_status=data_status,
            rule_version=rule_version,
            schema_version=schema_version,
            source_issue_count=summary.source_issue_count,
            prediction_payload=summary.model_dump(mode="json"),
        )

    @classmethod
    def _record_from_decision_card(
        cls,
        *,
        command: str,
        run_id: str,
        batch_id: str | None,
        created_at: datetime,
        data_status: str,
        rule_version: str,
        schema_version: str,
        data: DecisionCardData,
    ) -> ReviewRecord:
        return ReviewRecord(
            record_id=f"{run_id}:{command}:{data.symbol}",
            command=command,
            command_run_id=run_id,
            batch_id=batch_id,
            symbol=data.symbol,
            created_at=created_at,
            parameter_version=data.parameter_version,
            parameter_name=None,
            risk_profile=data.risk_profile,
            decision=data.decision,
            score=data.score,
            data_status=data_status,
            rule_version=rule_version,
            schema_version=schema_version,
            source_issue_count=data.source_issue_count,
            prediction_payload=data.model_dump(mode="json"),
        )

    @staticmethod
    def _build_suggestion(
        *,
        source: str,
        default_batch_id: str | None,
        imported_at: datetime,
        suggestion: ImportedSuggestion,
    ) -> ReviewSuggestion:
        return ReviewSuggestion(
            suggestion_id=suggestion.suggestion_id,
            source=source,
            record_id=suggestion.record_id,
            batch_id=suggestion.batch_id or default_batch_id,
            impact_scope=suggestion.impact_scope,
            title=suggestion.title,
            summary=suggestion.summary,
            rationale=suggestion.rationale,
            suggested_changes=suggestion.suggested_changes,
            status="pending",
            imported_at=imported_at,
        )

    @staticmethod
    def _resolve_preview_changes(
        suggestion: ReviewSuggestion,
        active: ParameterVersion | None,
    ) -> list[ResolvedSuggestionChange]:
        preview: list[ResolvedSuggestionChange] = []
        parameter_snapshot = None
        if active is not None:
            parameter_snapshot = active.model_dump(
                mode="python",
                exclude={"parameter_version", "created_at", "is_active"},
            )
        for change in suggestion.suggested_changes:
            current_value = change.current_value
            reason = change.reason
            if suggestion.impact_scope == "parameter-set" and parameter_snapshot is not None:
                try:
                    current_value = ReviewService._get_nested_value(parameter_snapshot, change.field_path)
                except KeyError:
                    reason = "unknown field_path"
            elif suggestion.impact_scope == "parameter-set" and parameter_snapshot is None:
                reason = "no active parameter version"
            preview.append(
                ResolvedSuggestionChange(
                    field_path=change.field_path,
                    current_value=current_value,
                    suggested_value=change.suggested_value,
                    will_change=current_value != change.suggested_value,
                    reason=reason,
                )
            )
        return preview

    @staticmethod
    def _build_updated_parameter_set(
        active: ParameterVersion,
        changes: list[ResolvedSuggestionChange],
        *,
        suggestion_id: str,
    ) -> ParameterSet:
        snapshot = active.model_dump(
            mode="python",
            exclude={"parameter_version", "created_at", "is_active"},
        )
        for change in changes:
            if change.will_change:
                ReviewService._set_nested_value(snapshot, change.field_path, change.suggested_value)
        notes = snapshot.get("notes")
        note_line = f"Applied OpenClaw suggestion {suggestion_id}"
        snapshot["notes"] = f"{notes}\n{note_line}" if notes else note_line
        return ParameterSet.model_validate(snapshot)

    @staticmethod
    def _get_nested_value(payload: dict[str, object], field_path: str):
        current = payload
        for part in field_path.split("."):
            if not isinstance(current, dict) or part not in current:
                raise KeyError(field_path)
            current = current[part]
        return current

    @staticmethod
    def _set_nested_value(payload: dict[str, object], field_path: str, value) -> None:
        current = payload
        parts = field_path.split(".")
        for part in parts[:-1]:
            if not isinstance(current, dict) or part not in current:
                raise KeyError(field_path)
            current = current[part]
        if not isinstance(current, dict) or parts[-1] not in current:
            raise KeyError(field_path)
        current[parts[-1]] = deepcopy(value)
