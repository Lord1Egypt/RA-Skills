"""Host-owned planning workflow: real receipts in, report text and files out.

All arguments and files are prepared by the Agent, never by the family. Network
discovery stays with the host; this module owns the previously manual plumbing.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from uuid import uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.contracts import CapabilityReport, EvidenceStatus, SourceCandidate, SourceTier
from scripts.adapters import StructuredAdapterError
from scripts.decision_policy import DecisionPolicySnapshot
from scripts.evidence import EvidenceStore
from scripts.planning_profile import PlanningProfile
from scripts.planning_session import (
    PlanningSession, PlanningSessionReplayContext, PlanningSessionReplayJournal,
    PlanningSessionInputError, SessionStage, build_task_evidence_outcome,
)
from scripts.preflight import detect_capabilities
from scripts.query_plan import build_query_plan, load_province_catalog
from scripts.questionnaire_intake import build_profile_from_questionnaire
from scripts.intake_progress import IntakeGateError, assess_intake, require_confirmed_intake


def _digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _directory(root: Path, name: str) -> Path:
    path = root / name
    path.mkdir(mode=0o700, exist_ok=True)
    if path.is_symlink() or path.resolve() != root / name:
        raise ValueError("workspace directory is not private")
    return path


class PlanningWorkflow:
    """Small host facade; every successful update saves a replayable checkpoint."""

    def __init__(self, root: Path, context: PlanningSessionReplayContext):
        self.root = root.resolve(strict=True)
        self.journal = PlanningSessionReplayJournal(_directory(self.root, "journal"))
        self.context = context

    @property
    def session(self):
        return self.context.session

    @property
    def profile(self):
        return self.context.profile

    @property
    def plan(self):
        return self.context.query_plan

    @classmethod
    def start(cls, root: Path, profile: PlanningProfile, capability: CapabilityReport, *, confirmed: bool):
        if confirmed is not True:
            raise ValueError("profile confirmation is required")
        root = Path(root).resolve(strict=True)
        journal = PlanningSessionReplayJournal(_directory(root, "journal"))
        session = PlanningSession.create(uuid4().hex, profile).confirm_profile(profile.digest)
        journal.save(session, profile=profile)
        session = session.with_preflight(capability)
        journal.save(session, profile=profile, capability_report=capability)
        plan = build_query_plan(profile, load_province_catalog(), DecisionPolicySnapshot.load_default())
        session = session.with_query_plan(plan, profile=profile)
        journal.save(session, profile=profile, capability_report=capability, query_plan=plan)
        return cls(root, journal.load(session.session_id))

    @classmethod
    def resume(cls, root: Path, session_id: str):
        root = Path(root).resolve(strict=True)
        journal = PlanningSessionReplayJournal(_directory(root, "journal"))
        return cls(root, journal.load(session_id))

    def _save(self, context):
        self.journal.save(
            context.session, profile=context.profile, query_plan=context.query_plan,
            capability_report=context.capability_report, bundle_path=context.bundle_path,
            task_outcomes=context.task_outcomes,
        )
        self.context = context

    def pending(self):
        if self.session.stage not in {SessionStage.QUERY_PLAN_READY, SessionStage.RESEARCH_IN_PROGRESS}:
            return ()
        available = self.session.next_tasks(self.plan, profile=self.profile)
        canonical = {task.task_id: task for task in self.plan.tasks}
        return tuple(canonical[task.task_id] for task in available)

    def _bundle(self, outcomes, candidates=()):
        store = EvidenceStore.create(_directory(self.root, "snapshots"), self.context.capability_report)
        seen = {}
        sources = list(candidates)
        if self.context.bundle_path is not None:
            from scripts.validate_evidence import validate_bundle_snapshot
            validation = validate_bundle_snapshot(
                self.context.bundle_path, _allow_empty=not self.session.completed_task_ids,
            )
            snapshot = validation.snapshot
            if snapshot is None:
                raise ValueError("previous evidence bundle no longer validates")
            for record in snapshot.candidates:
                value = record.to_dict()
                value["tier"] = SourceTier(value["tier"])
                sources.append(SourceCandidate(**value))
        for outcome in outcomes:
            for bridge in outcome._bridges:
                sources.extend(getattr(bridge, "candidates", ()))
        for source in sources:
            if source.source_id in seen:
                if seen[source.source_id] != source.to_dict():
                    raise ValueError("source ID refers to different public materials")
            else:
                store.add_candidate(source)
                seen[source.source_id] = source.to_dict()
        for outcome in outcomes:
            outcome.validate(self.profile, self.plan)
            for bridge in outcome._bridges:
                if not set(bridge.source_ids) <= seen.keys():
                    raise ValueError("completed bridge requires its original source candidates")
                bridge.persist(store)
        store.finalize()
        return store.session_path

    def complete(self, task_id: str, bridges, *, candidates=()):
        task = next((t for t in self.pending() if t.task_id == task_id), None)
        if task is None:
            raise ValueError("task is not pending")
        outcome = build_task_evidence_outcome(self.profile, self.plan, task, tuple(bridges))
        session = self.session.ingest_task(
            task_id, query_plan_digest=self.session.query_plan_digest,
            query_plan=self.plan, profile=self.profile, outcome="completed", evidence_outcome=outcome,
        )
        outcomes = tuple(sorted((*self.context.task_outcomes, outcome), key=lambda item: item.task_id))
        self._save(replace(self.context, session=session, task_outcomes=outcomes,
                           bundle_path=self._bundle(outcomes, candidates)))

    def unavailable(self, task_ids, *, reason: str, newer_task: str | None = None):
        ids = tuple(task_ids)
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("select distinct pending tasks")
        session = self.session
        newer = None
        if newer_task is not None:
            newer = next((item for item in self.context.task_outcomes if item.task_id == newer_task), None)
            if newer is None:
                raise ValueError("newer task must identify a completed evidence receipt")
        for task_id in ids:
            session = session.ingest_task(
                task_id, query_plan_digest=session.query_plan_digest, query_plan=self.plan,
                profile=self.profile, outcome="unavailable", unavailable_reason=reason,
                newer_evidence_outcome=newer,
            )
        bundle = self.context.bundle_path or self._bundle(self.context.task_outcomes)
        self._save(replace(self.context, session=session, bundle_path=bundle))

    def ingest(self, task_id: str, submission):
        """Extract saved source files and construct receipts in this process.

        The submission is host-owned extraction configuration, not an evidence
        receipt. No caller-supplied status or digest can authorize a fact.
        """
        task = next((t for t in self.pending() if t.task_id == task_id), None)
        if task is None:
            raise ValueError("task is not pending")
        sources = submission["sources"]
        if not sources or len(sources) > task.max_candidates:
            raise ValueError("source count is outside the task candidate limit")
        extracted, candidates = [], []
        for source in sources:
            from scripts.adapters import read_stable_local_file
            path = Path(source["path"])
            raw = read_stable_local_file(path, suffixes=(".html", ".htm", ".xlsx", ".xls", ".txt", ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".json"))
            metadata = dict(source["candidate"])
            actual_hash = "sha256:" + hashlib.sha256(raw).hexdigest()
            if metadata.get("content_hash", actual_hash) != actual_hash:
                raise ValueError("saved source hash does not match its metadata")
            metadata["content_hash"] = actual_hash
            metadata["tier"] = SourceTier(metadata["tier"])
            candidate = SourceCandidate(**metadata)
            options = source.get("options", {})
            if source["adapter"] == "html":
                from scripts.adapters import ColumnMapping
                from scripts.adapters.html_table import extract_html_table
                mapping = ColumnMapping(options["columns"], roles=options.get("roles"),
                                        score_scale=options.get("score_scale"))
                document = extract_html_table(path, table_index=options["table_index"],
                    expected_caption=options.get("caption"), mapping=mapping)
            elif source["adapter"] in {"xlsx", "xls"}:
                from scripts.adapters import ColumnMapping
                if source["adapter"] == "xlsx":
                    from scripts.adapters.spreadsheet import extract_spreadsheet, SpreadsheetDependencyError
                    extractor, dependency_error = extract_spreadsheet, SpreadsheetDependencyError
                else:
                    from scripts.adapters.xls import extract_xls, XlsDependencyError
                    extractor, dependency_error = extract_xls, XlsDependencyError
                mapping = ColumnMapping(options["columns"], roles=options.get("roles"),
                                        score_scale=options.get("score_scale"))
                try:
                    document = extractor(path, sheet=options["sheet"], mapping=mapping)
                except dependency_error:
                    raise ModuleNotFoundError("spreadsheet parser unavailable") from None
            elif source["adapter"] == "pdf_text":
                if task.kind not in {"strong_foundation", "comprehensive_evaluation", "hk_macao_admission", "special_pathway"}:
                    raise ValueError("PDF prose requires a pathway task; numeric tables need an exact table adapter")
                from scripts.adapters.pdf_text import extract_pdf_text, PdfDependencyError
                try:
                    document = extract_pdf_text(path)
                except PdfDependencyError:
                    raise ModuleNotFoundError("PDF text parsers unavailable") from None
            elif source["adapter"] == "pdf_table":
                from scripts.adapters import ColumnMapping
                from scripts.adapters.pdf_table import extract_pdf_table
                from scripts.adapters.pdf_text import PdfDependencyError
                mapping = ColumnMapping(options["columns"], roles=options.get("roles"),
                                        score_scale=options.get("score_scale"))
                try:
                    document = extract_pdf_table(
                        path, mapping=mapping, headers=options["headers"],
                        page_number=options["page_number"], header_line=options["header_line"],
                        first_data_line=options["first_data_line"], last_data_line=options["last_data_line"],
                        column_group=options.get("column_group", 1), expected_caption=options.get("caption"),
                    )
                except PdfDependencyError:
                    raise ModuleNotFoundError("PDF table parsers unavailable") from None
            elif source["adapter"] == "public_text":
                from scripts.adapters.public_text import PublicTextField, bind_public_text
                document = bind_public_text(source_id=candidate.source_id, url=candidate.url,
                    text=raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n"),
                    fields={key: PublicTextField(**value) for key, value in options["fields"].items()})
            elif source["adapter"] == "ocr_rows":
                from scripts.adapters import ColumnMapping
                from scripts.adapters.ocr_rows import normalize_ocr_rows
                mapping = ColumnMapping(options["columns"], roles=options.get("roles"),
                    score_scale=options["score_scale"])
                document = normalize_ocr_rows(Path(options["ocr_path"]), mapping,
                    score_scale=options["score_scale"], min_exact_confidence=0.95)
            else:
                raise ValueError("unsupported host source adapter")
            if read_stable_local_file(path, suffixes=(path.suffix,)) != raw:
                raise ValueError("saved public source changed during extraction")
            extracted.append(document)
            candidates.append(candidate)
        bridges = []
        if task.kind in {"strong_foundation", "comprehensive_evaluation", "hk_macao_admission", "special_pathway"}:
            from scripts.adapters.pathway_extraction import extract_pathway_policy
            from scripts.adapters.pathway_bridge import bridge_pathway_policy_evidence
            maps = [s.get("options", {}).get("field_map", submission.get("field_map")) for s in sources]
            projection = extract_pathway_policy(profile=self.profile, plan=self.plan, task=task,
                extraction=tuple(extracted), field_map=tuple(maps), candidates=tuple(candidates))
            bridges.append(bridge_pathway_policy_evidence(projection))
        elif all(source["adapter"] == "public_text" for source in sources):
            from scripts.adapters.school_fit_bridge import bridge_school_fit_public_text
            bridges.append(bridge_school_fit_public_text(self.profile, self.plan, task,
                tuple(extracted), tuple(candidates)))
        else:
            records = submission["records"]
            if not records:
                raise ValueError("no extracted records were selected")
            for record in records:
                indexes = record["rows"]
                if len(indexes) != len(extracted) or any(type(i) is not int or i < 0 for i in indexes):
                    raise ValueError("select one source row per document")
                rows = tuple(table.rows[index] for table, index in zip(extracted, indexes))
                if task.kind in {"score_table", "joy_report"}:
                    from scripts.adapters.rank_bridge import bridge_rank_evidence
                    if any(row.values != rows[0].values for row in rows[1:]):
                        raise ValueError("source values conflict; record source_conflict")
                    bridges.append(bridge_rank_evidence(profile=self.profile, plan=self.plan, task=task,
                        table=extracted[0], extracted_row=rows[0], candidates=tuple(candidates),
                        coverage_status=EvidenceStatus(record.get("coverage_status", "partial"))))
                elif task.kind == "batch_admission":
                    from scripts.adapters.admission_bridge import bridge_admission_evidence
                    from scripts.validate_data import ValidatedAdmissionRow
                    if any(row.values != rows[0].values for row in rows[1:]):
                        raise ValueError("source values conflict; record source_conflict")
                    values = {"year": task.year, "province": task.province,
                              "subject_group": task.subject_group, "remarks": "", **rows[0].values}
                    dataset = ValidatedAdmissionRow.from_mapping(values)
                    fact_id = "admission-" + _digest(dataset.to_dict()).split(":")[1][:24]
                    bridges.append(bridge_admission_evidence(table=extracted[0], adapter_row=rows[0],
                        task=task, dataset_row=dataset, fact_id=fact_id, candidates=tuple(candidates),
                        coverage_status=EvidenceStatus(record.get("coverage_status", "partial"))))
                else:
                    from scripts.adapters.school_fit_bridge import bridge_school_fit_evidence
                    bridges.append(bridge_school_fit_evidence(profile=self.profile, plan=self.plan, task=task,
                        tables=tuple(extracted), adapter_rows=rows, candidates=tuple(candidates)))
        self.complete(task_id, bridges, candidates=candidates)

    def finish(self, *, format="markdown") -> Path:
        if self.pending():
            raise ValueError("research tasks remain; record results or their actual unavailable reasons")
        if self.session.stage is SessionStage.RESEARCH_IN_PROGRESS:
            session, _ = self.context.finalize_evidence()
            self._save(replace(self.context, session=session))
        if self.session.stage is SessionStage.EVIDENCE_FINALIZED:
            session, _ = self.context.calculate()
            self._save(replace(self.context, session=session))
        _published_session, publication = self.context.publish(format=format)
        # Keep the calculation checkpoint for retry and alternate format export.
        directory = _directory(self.root, "reports")
        extension = "md" if format == "markdown" else "docx"
        destination = directory / f"{self.session.session_id}.{extension}"
        content = publication.rendered_bytes
        if destination.exists():
            if destination.is_symlink() or destination.read_bytes() != content:
                raise ValueError("report destination already contains a different artifact")
            return destination
        fd, temp_name = tempfile.mkstemp(prefix=".report-", dir=directory)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            # Hard link is exclusive and atomic on supported local filesystems.
            os.link(temp_path, destination)
        finally:
            temp_path.unlink(missing_ok=True)
        return destination

    def brief(self, submission):
        """Deliver a bounded planning reference without closing deep research."""
        from scripts.planning_brief import build_planning_brief
        result = build_planning_brief(self.profile, submission, research_year=self.plan.research_year)
        identity = _digest({"submission": submission, "result": result})[7:23]
        directory = _directory(self.root, "reports")
        destination = directory / f"{self.session.session_id}.brief-{identity}.md"
        content = result["report_text"].encode("utf-8")
        if destination.exists():
            if destination.is_symlink() or destination.read_bytes() != content:
                raise ValueError("brief destination already contains a different artifact")
        else:
            with destination.open("xb") as output:
                output.write(content)
        # Keep the source submission in the private workspace, not in a receipt.
        record = directory / f"{self.session.session_id}.brief-{identity}.json"
        body = json.dumps({"submission": submission, "result": result}, ensure_ascii=False, sort_keys=True).encode("utf-8")
        if record.exists():
            if record.is_symlink() or record.read_bytes() != body:
                raise ValueError("brief source record disagrees")
        else:
            with record.open("xb") as output:
                output.write(body)
        return {**result, "report_generated": True, "report": str(destination), "session_id": self.session.session_id,
                "research_summary": self.research_summary()}

    def report_text(self) -> str:
        """Return complete chat source text from the authenticated calculation.

        Replaying the publication keeps text available for DOCX exports and
        resumed sessions without trusting a mutable report attachment.
        """
        _session, publication = self.context.publish(format="markdown")
        return publication.rendered_bytes.decode("utf-8")

    def delivery(self):
        """Describe what the replayed evidence supports, not just task closure."""
        _session, publication = self.context.publish(format="markdown")
        calculation = publication._calculation_outcome
        fact_count = len(calculation._evidence_outcome._snapshot.facts)
        mode = "profile_only" if fact_count == 0 else (
            "partial" if calculation.degraded else "evidence_supported"
        )
        return {"mode": mode, "evidence_fact_count": fact_count, "degraded": calculation.degraded}

    def research_summary(self):
        completed = len(self.session.completed_task_ids)
        unavailable = len(self.session.unavailable_task_ids)
        total = len(self.session.expected_task_ids)
        return {
            "total": total, "completed": completed, "unavailable": unavailable,
            "pending": total - completed - unavailable,
            "unavailable_by_reason": dict(sorted(Counter(self.session.unavailable_reason_codes).items())),
        }

    def _older_year_resolution(self, pending):
        """Offer bounded hints using the same receipt gate as an explicit update."""
        hints, suggested = [], set()
        newer_outcomes = sorted(self.context.task_outcomes, key=lambda item: (-item.year, item.task_id))
        for newer in newer_outcomes:
            if not newer.usable or "official" not in newer.evidence_statuses:
                continue
            ids = []
            for task in pending:
                if (task.task_id in suggested or task.kind != newer.kind
                        or task.target_name != newer.target_name or task.year >= newer.year):
                    continue
                try:
                    # The immutable transition is checked but never persisted here.
                    self.session.ingest_task(
                        task.task_id, query_plan_digest=self.session.query_plan_digest,
                        query_plan=self.plan, profile=self.profile, outcome="unavailable",
                        unavailable_reason="newer_comparable_year_accepted", newer_evidence_outcome=newer,
                    )
                except PlanningSessionInputError:
                    continue
                ids.append(task.task_id)
                suggested.add(task.task_id)
            if ids:
                hints.append({"newer_task": newer.task_id, "task_ids": ids,
                              "reason": "newer_comparable_year_accepted"})
        return hints

    def status(self, *, limit=3):
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("task display limit must be between 1 and 100")
        pending = sorted(self.pending(), key=lambda task: (-task.year, task.kind, task.task_id))
        result = {
            "initial_delivery_action": "collect_sources_then_brief",
            "session_id": self.session.session_id,
            "stage": self.session.stage.value,
            "completed": len(self.session.completed_task_ids),
            "unavailable": len(self.session.unavailable_task_ids),
            "pending": len(pending),
            "next": [t.to_dict() for t in pending[:limit]],
            "research_summary": self.research_summary(),
            "older_year_resolution": self._older_year_resolution(pending),
            "first_delivery": {
                "applies_only_before_first_report": True,
                "command": "brief",
                "mode": "planning_reference",
                "requires_deep_task_closure": False,
                "original_page_budget": 24,
                "research_minutes": 8,
                "includes_setup_and_repair": True,
                "max_attempts_per_failed_action": 2,
                "switch_after_no_progress_seconds": 90,
                "budget_exhausted_action": "deliver_supported_seven_section_reference",
                "ordinary_counts": {"冲": 3, "稳": 4, "保": 5},
                "pathway_counts": {"冲": 1, "稳": 1, "保": 1},
            },
        }
        if self.session.stage is SessionStage.CALCULATION_COMPLETE:
            result["delivery"] = self.delivery()
        return result

    def public_sources(self):
        """Give the host real public links for the report's source identifiers."""
        if self.context.bundle_path is None:
            return []
        from scripts.validate_evidence import validate_bundle_snapshot
        snapshot = validate_bundle_snapshot(
            self.context.bundle_path, _allow_empty=not self.session.completed_task_ids,
        ).snapshot
        if snapshot is None:
            raise ValueError("report sources no longer validate")
        keys = ("source_id", "url", "publisher", "tier", "published_at", "retrieved_at")
        return [{key: record.to_dict()[key] for key in keys} for record in snapshot.candidates]


def _failure_feedback(error):
    """Keep diagnostics useful to the host without echoing private input."""
    if isinstance(error, IntakeGateError):
        return {"ok": False, "report_generated": False, "error_code": "intake_incomplete",
                "user_message": error.progress["next_question"],
                "host_action": "First rebuild missing coverage from retained real user replies and confirmation; do not re-ask known facts or invent quotes. Then ask only a genuinely missing question or confirm the profile. Do not generate a personal report before readiness.",
                "user_action_required": False, "intake_progress": error.progress}
    if isinstance(error, ModuleNotFoundError):
        code = "capability_unavailable"
        message = "有一项辅助功能暂时用不了，我会先尝试现有方式继续处理。"
        action = "Check the needed capability; try an available reader or chat/Markdown delivery. Do not claim an export exists."
    elif isinstance(error, StructuredAdapterError):
        code = "source_unreadable"
        message = "这份资料暂时没能准确读出，我会换一种方式核对，能确认的内容先继续。"
        action = "Try an available reader or another readable source within the research budget; never invent extracted values."
    elif isinstance(error, FileNotFoundError):
        code = "input_unavailable"
        message = "暂时没能读到这一步需要的资料，我会先核对现有记录并尝试恢复。"
        action = "Locate the host-owned input or existing session; preserve the conversation draft. Do not ask the family for an internal path."
    elif isinstance(error, PermissionError):
        code = "storage_unavailable"
        message = "当前资料读取或保存受到限制，我会先尝试其他可用方式。"
        action = "Check access within existing permissions, retaining the original session. Request user action only for a verified unavoidable access gate."
    elif isinstance(error, OSError):
        code = "operation_unavailable"
        message = "这一步暂时没有完成，我会先处理当前能确认的内容，再尝试恢复。"
        action = "Inspect the host operation; attempt a bounded available fallback. Verify actual saved progress before claiming recovery."
    else:
        code = "input_invalid"
        message = "有一处资料需要重新核对，我会先检查现有记录，已能确认的内容继续处理。"
        action = "Check host-prepared inputs and evidence against their contract. Do not change student facts or bypass validation; reconfirm actual profile changes."
    return {"ok": False, "report_generated": False, "error_code": code,
            "user_message": message, "host_action": action, "user_action_required": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("start", "next", "brief", "ingest", "unavailable", "finish"))
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--session")
    profile_input = parser.add_mutually_exclusive_group()
    profile_input.add_argument("--answers", type=Path, help="normalized answers 1–20, or an exported confirmed v3 profile")
    profile_input.add_argument("--profile", type=Path, help="already confirmed PlanningProfile v3 JSON")
    parser.add_argument("--submission", type=Path)
    parser.add_argument("--confirmed", action="store_true")
    parser.add_argument("--intake", type=Path, help="Private field-level intake coverage and profile confirmation")
    parser.add_argument("--host-capability", action="append", default=[])
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--reason")
    parser.add_argument("--newer-task")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--format", choices=("markdown", "docx"), default="markdown")
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            selected = args.profile or args.answers
            if selected is None:
                raise ValueError("provide normalized --answers or an already confirmed --profile")
            data = json.loads(selected.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict):
                raise ValueError("answers/profile input must be a JSON object")
            if args.profile or data.get("schema_version") == "3.0":
                data = dict(data)
                claimed_digest = data.pop("digest", None)
                claimed_mode = data.pop("mode", None)
                profile = PlanningProfile.create(data)
                if claimed_digest is not None and claimed_digest != profile.digest:
                    raise ValueError("confirmed profile digest disagrees; reconfirm changed profile")
                if claimed_mode is not None and claimed_mode != profile.mode:
                    raise ValueError("confirmed profile mode disagrees")
            else:
                try:
                    answers = {int(k): v for k, v in data.items()}
                except ValueError:
                    raise ValueError("--answers needs keys 1–20; use --profile for a confirmed v3 profile") from None
                profile = build_profile_from_questionnaire(answers)
            if args.intake is None:
                raise IntakeGateError(assess_intake({"schema_version": "1.0", "responses": {}}))
            require_confirmed_intake(json.loads(args.intake.read_text(encoding="utf-8-sig")), profile.digest)
            workflow = PlanningWorkflow.start(
                args.workspace, profile, detect_capabilities(set(args.host_capability)), confirmed=args.confirmed,
            )
        else:
            if args.session is None:
                raise ValueError("session ID is required")
            workflow = PlanningWorkflow.resume(args.workspace, args.session)
        if args.command == "unavailable":
            workflow.unavailable(args.task, reason=args.reason, newer_task=args.newer_task)
        if args.command == "ingest":
            if len(args.task) != 1 or args.submission is None:
                raise ValueError("ingest requires one task and a host source submission")
            workflow.ingest(args.task[0], json.loads(args.submission.read_text(encoding="utf-8")))
        if args.command == "brief":
            if args.submission is None:
                raise ValueError("brief requires a host source submission")
            print(json.dumps(workflow.brief(json.loads(args.submission.read_text(encoding="utf-8"))), ensure_ascii=False))
        elif args.command == "finish":
            result = workflow.finish(format=args.format)
            print(json.dumps({"session_id": workflow.session.session_id, "report": str(result),
                              "format": args.format, "report_text": workflow.report_text(),
                              "sources": workflow.public_sources(), "delivery": workflow.delivery(),
                              "research_summary": workflow.research_summary()}, ensure_ascii=False))
        else:
            print(json.dumps({**workflow.status(limit=args.limit), "command": args.command,
                              "report_generated": False}, ensure_ascii=False))
        return 0
    except ModuleNotFoundError as error:
        print(json.dumps(_failure_feedback(error), ensure_ascii=False), file=sys.stderr)
        return 3
    except (ValueError, TypeError, OSError, KeyError, IndexError, StructuredAdapterError) as error:
        print(json.dumps(_failure_feedback(error), ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
