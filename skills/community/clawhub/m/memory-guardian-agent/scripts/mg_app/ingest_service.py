"""Application-layer ingest orchestration."""

from __future__ import annotations

import os

from mg_utils import _now_iso
from memory_ingest import (
    _assign_memory_type,
    _build_new_memory,
    _build_content_from_case_fields,
    _classify,
    _compute_provenance_confidence,
    _determine_provenance,
    _run_quality_gate,
    _security_precheck,
    _write_memory_file,
    check_security,
    extract_entities,
    quick_dedup_check,
)


def _fill_fields(content=None, situation=None, judgment=None, consequence=None, action_conclusion=None):
    """Normalize ingest fields into a single payload."""
    built_content, is_case = _build_content_from_case_fields(
        situation,
        judgment,
        consequence,
        action_conclusion,
        content,
    )
    return {
        "content": built_content,
        "is_case": is_case,
        "situation": situation,
        "judgment": judgment,
        "consequence": consequence,
        "action_conclusion": action_conclusion,
    }


def _detect_provenance(content, situation=None, is_case=False, source=None):
    """Derive provenance level/source for one ingest request."""
    return _determine_provenance(content, situation, is_case, source=source)


def _evaluate_pool(content, memories):
    """Inspect the current memory pool before writing."""
    active_count = sum(
        1 for mem in memories if mem.get("status", "active") in ("active", "observing")
    )
    return {
        "duplicate": quick_dedup_check(content, memories),
        "active_count": active_count,
    }


def _gate_check(meta_path, meta, mem, *, content, situation=None, judgment=None,
                consequence=None, action_conclusion=None, tags=None):
    """Run quality gate evaluation for a candidate memory."""
    intervention_level, queue_result = _run_quality_gate(
        mem,
        content,
        meta,
        meta_path,
        situation,
        judgment,
        consequence,
        action_conclusion,
        tags,
    )
    return {
        "intervention_level": intervention_level,
        "queue_result": queue_result,
    }


class IngestService:
    """Thin app service over meta repository + legacy helper logic."""

    def __init__(self, repo):
        self.repo = repo

    def _update_existing(self, meta, update_id, content, importance, tags,
                         situation, judgment, consequence, action_conclusion,
                         reversibility, boundary_words, alternatives,
                         provenance_source=None):
        now = _now_iso()
        target = None
        for mem in meta.get("memories", []):
            if mem.get("id") == update_id:
                target = mem
                break

        if not target:
            return {"action": "not_found", "id": update_id}

        target["content"] = content or target.get("content", "")
        if importance is not None:
            target["importance"] = importance
            target["decay_score"] = importance
        if tags:
            target["tags"] = list(set(target.get("tags", []) + tags))
        if situation:
            target["situation"] = situation
        if judgment:
            target["judgment"] = judgment
        if consequence:
            target["consequence"] = consequence
        if action_conclusion:
            target["action_conclusion"] = action_conclusion
        if reversibility is not None:
            target["reversibility"] = reversibility
        if boundary_words:
            target["boundary_words"] = boundary_words
        if alternatives:
            target["alternatives_considered"] = alternatives

        target["entities"] = extract_entities(target["content"])
        target["last_accessed"] = now
        target["updated_at"] = now

        # Update provenance, confidence, memory_type (before single save)
        previous_level = target.get("provenance_level")
        previous_source = target.get("provenance_source")
        new_level, new_source = _determine_provenance(
            target["content"],
            target.get("situation"),
            target.get("case_type") == "case",
            source=provenance_source,
        )
        target["provenance_level"] = new_level
        target["provenance_source"] = new_source
        target["confidence"] = _compute_provenance_confidence(
            new_level,
            verification_count=target.get("verification_count", 0),
            decay_config=meta.get("decay_config", {}),
        )
        target["memory_type"] = _assign_memory_type(
            new_level,
            target.get("situation") if target.get("case_type") == "case" else None,
            target.get("tags", []),
        )
        target.setdefault("quality_gate", {})
        target["quality_gate"]["confidence"] = target["confidence"]

        # Single save (merged from two separate saves)
        self.repo.save_meta(meta)

        if previous_level != new_level or previous_source != new_source:
            self.repo.append_event(
                {
                    "event_type": "PROVENANCE_UPDATED",
                    "memory_id": update_id,
                    "from_level": previous_level,
                    "to_level": new_level,
                    "from_source": previous_source,
                    "to_source": new_source,
                },
                context={"command": "ingest_update"},
            )
        return {"action": "updated", "id": update_id}

    def ingest(self, content, importance, tags, workspace=None,
               update_id=None, situation=None, judgment=None, consequence=None,
               action_conclusion=None, reversibility=None, boundary_words=None,
               alternatives=None, skip_security=False, provenance_source=None):
        meta = self.repo.load_meta(persist=True)
        workspace = workspace or self.repo.workspace

        if update_id:
            return self._update_existing(
                meta,
                update_id,
                content,
                importance,
                tags,
                situation,
                judgment,
                consequence,
                action_conclusion,
                reversibility,
                boundary_words,
                alternatives,
                provenance_source,
            )

        if not skip_security:
            blocked = _security_precheck(content, workspace)
            if blocked:
                return {"action": "blocked", "violations": blocked}

        fields = _fill_fields(
            content=content,
            situation=situation,
            judgment=judgment,
            consequence=consequence,
            action_conclusion=action_conclusion,
        )
        if not fields["content"]:
            return {"action": "error", "message": "No content"}

        pool = _evaluate_pool(fields["content"], meta.get("memories", []))
        if pool["duplicate"]:
            return {"action": "dedup_found", "existing": pool["duplicate"].get("id")}

        # v0.4.5: Step 1 — Classification
        classification = _classify(
            fields["content"],
            tags_hint=tags,
            is_case=fields["is_case"],
            situation=fields["situation"],
            judgment=fields["judgment"],
        )

        # Collect existing memory_ids for uniqueness
        existing_ids = set()
        for m in meta.get("memories", []):
            if m.get("memory_id"):
                existing_ids.add(m["memory_id"])

        mem, cost_factors, is_l1, importance_explain = _build_new_memory(
            fields["content"],
            importance,
            tags,
            fields["situation"],
            fields["judgment"],
            fields["consequence"],
            fields["action_conclusion"],
            reversibility,
            boundary_words,
            alternatives,
            provenance_source,
            fields["is_case"],
            meta.get("decay_config", {}),
            classification=classification,
            existing_ids=existing_ids,
        )

        # v0.4.5: Ensure memory_id uniqueness with existing pool (edge case: collision within same second)
        if mem["memory_id"] in existing_ids:
            from mg_utils import generate_memory_id
            mem["memory_id"] = generate_memory_id(
                fields["content"], existing_ids=existing_ids
            )
            # Re-derive file_path
            from mg_utils import derive_file_path, classify_confidence_level
            if mem.get("inbox_reason") == "uncertain":
                mem["file_path"] = f"memory/_inbox/uncertain/{mem['memory_id']}.md"
            else:
                mem["file_path"] = derive_file_path(
                    mem["memory_id"], mem["tags"], fields["content"]
                )

        # v0.4.5: Step 2 — Confidence gate (already handled in _build_new_memory)
        # classification_confidence, needs_review, inbox_reason are set

        gate = _gate_check(
            self.repo.meta_path,
            meta,
            mem,
            content=fields["content"],
            situation=fields["situation"],
            judgment=fields["judgment"],
            consequence=fields["consequence"],
            action_conclusion=fields["action_conclusion"],
            tags=tags,
        )
        if gate["queue_result"]:
            self.repo.append_event(
                {
                    "event_type": "MEMORY_INGEST_QUEUED",
                    "memory_id": mem["id"],
                    "provenance_level": mem.get("provenance_level"),
                },
                context={"command": "ingest"},
            )
            return {"action": "queued", "id": mem["id"], "queue_result": gate["queue_result"]}

        # v0.4.5: Step 3 — Write memory file + update meta.json
        # File is written first; if mutate_meta fails, clean up the file
        written_file = _write_memory_file(
            mem["memory_id"],
            fields["content"],
            mem.get("file_path", ""),
            workspace=workspace,
        )

        def mutator(working):
            working.setdefault("memories", []).append(mem)
            return mem

        try:
            self.repo.mutate_meta(mutator, context={"command": "ingest"})
        except Exception:
            # Roll back: remove the file that was already written
            if written_file and os.path.exists(written_file):
                try:
                    os.unlink(written_file)
                except OSError:
                    pass
            raise
        self.repo.append_event(
            {
                "event_type": "MEMORY_INGESTED",
                "memory_id": mem["id"],
                "provenance_level": mem.get("provenance_level"),
                "provenance_source": mem.get("provenance_source"),
                "is_case": fields["is_case"],
            },
            context={"command": "ingest"},
        )
        return {
            "action": "created",
            "id": mem["id"],
            "memory": mem,
            "cost_factors": cost_factors,
            "is_l1": is_l1,
            "importance_explain": importance_explain,
            "classification": classification,
            "written_file": written_file,
        }
