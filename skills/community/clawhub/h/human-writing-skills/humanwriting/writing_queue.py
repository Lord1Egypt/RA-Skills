"""Persistent outline-to-manuscript tasks executed by a host's writing agents."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit_storage import atomic_write, package_lock, package_path, serialized
from .compiler import CORE_REVIEW_MODULES, VOICE_AUDIT_MODULES, compile_prompt
from .detection import has_directed_interaction
from .linter import lint_text
from .skills import list_style_skills, load_many


PLAN_FILE = "writing-plan.json"
STATE_FILE = "writing-state.json"
MAX_REVISIONS = 2
MAX_PROMPT = 60000
MAX_RESULT = 160000
LEASE_SECONDS = 3600
SERIOUS_STYLES = {"academic-paper", "news-report", "formal-document"}


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def _nonempty(value: Any, label: str, maximum: int = 12000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{label} must be non-empty text of at most {maximum} characters.")
    return value


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f"{label} must be a list of non-empty strings.")
    if len(set(value)) != len(value):
        raise ValueError(f"{label} must not contain duplicates.")
    return value


def count_length(text: str, unit: str) -> int:
    if unit == "characters":
        return len(re.sub(r"\s", "", text))
    if unit == "words":
        return len(re.findall(r"\w+(?:['\u2019-]\w+)*", text, re.UNICODE))
    raise ValueError("length_unit must be characters or words.")


def _units(text: str, prefix: str) -> list[dict[str, str]]:
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = [p[start:start + 2000] for p in parts for start in range(0, len(p), 2000)]
    return [{"id": f"{prefix}{i:04d}", "text": p} for i, p in enumerate(chunks, 1)]


def _write_id(index: int) -> str:
    return f"write-{index:04d}"


def _review_id(index: int) -> str:
    return f"review-{index:04d}"


def plan_long_form_writing(
    outline_path: str | Path,
    output_dir: str | Path,
    *,
    style: str,
    target_length: int,
    chunk_size: int = 5000,
    length_unit: str = "characters",
    execution_mode: str = "sequential",
    max_parallel: int = 4,
    context_paths: list[str] | None = None,
    source_paths: list[str] | None = None,
    reference_paths: list[str] | None = None,
) -> dict[str, Any]:
    """Snapshot inputs and create five-role assignments, without calling a model."""
    if style not in list_style_skills():
        raise ValueError("Unknown writing style.")
    if type(target_length) is not int or not 1 <= target_length <= 5000000:
        raise ValueError("target_length must be an integer between 1 and 5000000.")
    if type(chunk_size) is not int or not 200 <= chunk_size <= 12000:
        raise ValueError("chunk_size must be an integer between 200 and 12000.")
    if length_unit not in {"characters", "words"} or execution_mode not in {"sequential", "contract"}:
        raise ValueError("Invalid length_unit or execution_mode.")
    if type(max_parallel) is not int or not 1 <= max_parallel <= 32:
        raise ValueError("max_parallel must be an integer between 1 and 32.")
    count = math.ceil(target_length / chunk_size)
    if count > 1000:
        raise ValueError("At most 1000 writing chunks can be planned in one project.")
    package = Path(output_dir).resolve()
    if package.exists() and (not package.is_dir() or any(package.iterdir())):
        raise ValueError("Writing output directory must be empty.")
    inputs: dict[str, list[dict[str, str]]] = {}
    snapshots: list[tuple[str, str]] = []
    originals: list[str] = []
    for kind, paths, prefix in (
        ("outline", [str(outline_path)], "O"),
        ("context", context_paths or [], "C"),
        ("sources", source_paths or [], "S"),
        ("references", reference_paths or [], "R"),
    ):
        group = []
        for file_index, value in enumerate(paths, 1):
            original = Path(value).resolve()
            if not original.is_file() or original.stat().st_size > 2000000:
                raise ValueError(f"{kind} input must be a file of at most 2 MB.")
            text = original.read_text(encoding="utf-8-sig")
            if not text.strip():
                raise ValueError(f"{kind} input is empty.")
            originals.append(str(original))
            units = _units(text, prefix)
            for item in units:
                item["id"] = f"{prefix}{len(group) + 1:04d}"
                item["path"] = f"inputs/{item['id']}.md"
                item["sha256"] = _hash(item["text"])
                snapshots.append((item["path"], item["text"]))
                group.append(item)
        inputs[kind] = [{k: v for k, v in item.items() if k != "text"} for item in group]
    if sum(len(text) for path, text in snapshots if path.startswith("inputs/C")) > 12000:
        raise ValueError("Canonical context exceeds 12000 characters; supply a compact approved ledger.")
    if sum(len(text) for path, text in snapshots if path.startswith("inputs/O")) > 24000:
        raise ValueError("Outline exceeds 24000 characters; use an approved hierarchical outline.")
    plan = {
        "schema": 1, "mode": "long-form-writing", "style": style,
        "target_length": target_length, "chunk_size": chunk_size, "chunk_count": count,
        "length_unit": length_unit, "execution_mode": execution_mode,
        "max_parallel": max_parallel, "max_revisions": MAX_REVISIONS,
        "targets": [min(chunk_size, target_length - i * chunk_size) for i in range(count)],
        "inputs": inputs, "original_paths": originals,
    }
    package.mkdir(parents=True, exist_ok=True)
    (package / "inputs").mkdir()
    (package / "results").mkdir()
    for path, text in snapshots:
        atomic_write(package_path(package, path, "input"), text)
    plan_text = _json(plan)
    atomic_write(package / PLAN_FILE, plan_text)
    atomic_write(package / STATE_FILE, _json({"schema": 1, "plan_sha256": _hash(plan_text),
        "entries": {}, "feedback": {}, "revision_counts": {}, "blocked": {}}))
    return {"package_dir": str(package), "chunk_count": count, "target_length": target_length,
        "length_unit": length_unit, "task_count": 2 * count + 3,
        "next_action": "Claim outline-check, submit its result, then claim chunk-plan. The host runs the agents."}


def _load(package_dir: str | Path):
    package = Path(package_dir).resolve()
    try:
        plan_text = package_path(package, PLAN_FILE, "plan").read_text(encoding="utf-8")
        plan = json.loads(plan_text)
        state = json.loads(package_path(package, STATE_FILE, "state").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("Writing package is missing or malformed.") from exc
    if state.get("plan_sha256") != _hash(plan_text) or plan.get("mode") != "long-form-writing":
        raise ValueError("Writing plan changed; create a new package from the corrected inputs.")
    for group in plan["inputs"].values():
        for item in group:
            text = package_path(package, item["path"], "input").read_text(encoding="utf-8")
            if _hash(text) != item["sha256"]:
                raise ValueError("A writing input snapshot changed; existing approvals are stale.")
    return package, plan, state


def _save(package: Path, state: dict) -> None:
    atomic_write(package / STATE_FILE, _json(state))


def _result(package: Path, state: dict, task_id: str) -> dict | None:
    entry = state["entries"].get(task_id, {})
    if entry.get("status") != "submitted":
        return None
    path = package_path(package, entry["result_path"], "result")
    text = path.read_text(encoding="utf-8")
    if _hash(text) != entry["sha256"]:
        raise ValueError(f"Stored result {task_id} changed; approval is invalid.")
    return json.loads(text)


def _tasks(plan: dict) -> list[str]:
    return ["outline-check", "chunk-plan", *[task for i in range(1, plan["chunk_count"] + 1)
        for task in (_write_id(i), _review_id(i))], "continuity"]


def _chunk(package: Path, state: dict, index: int) -> dict:
    planning = _result(package, state, "chunk-plan")
    if not planning:
        raise ValueError("Chunk planning has not passed.")
    return planning["chunks"][index - 1]


def _dependencies(package: Path, plan: dict, state: dict, task: str) -> list[str]:
    if task == "outline-check":
        return []
    if task == "chunk-plan":
        return ["outline-check"]
    if task == "continuity":
        return [_review_id(i) for i in range(1, plan["chunk_count"] + 1)]
    kind, number = task.split("-")
    index = int(number)
    if kind == "review":
        return [_write_id(index)]
    if not _result(package, state, "chunk-plan"):
        return ["chunk-plan"]
    chunk = _chunk(package, state, index)
    deps = sorted(int(x.split("-")[1]) for x in chunk["depends_on"])
    if plan["execution_mode"] == "sequential" and index > 1:
        deps = sorted(set(deps + [index - 1]))
    return ["chunk-plan", *[_review_id(i) for i in deps]]


def _ready_error(package: Path, plan: dict, state: dict, task: str) -> str | None:
    if task not in _tasks(plan):
        raise ValueError(f"Unknown writing task: {task}")
    if task in state["blocked"]:
        return state["blocked"][task]
    for dep in _dependencies(package, plan, state, task):
        result = _result(package, state, dep)
        if not result or result.get("decision", "pass") != "pass":
            return f"Waiting for {dep}"
    if _result(package, state, task):
        return "Already submitted"
    return None


def _active(entry: dict) -> bool:
    return entry.get("status") == "claimed" and (
        datetime.now(timezone.utc).timestamp() - entry.get("claimed_at", 0) < LEASE_SECONDS)


def list_writing_tasks(package_dir: str | Path) -> dict[str, Any]:
    package, plan, state = _load(package_dir)
    rows = []
    active_count = sum(_active(entry) for entry in state["entries"].values())
    for task in _tasks(plan):
        entry = state["entries"].get(task, {})
        error = _ready_error(package, plan, state, task)
        claimed = _active(entry)
        rows.append({"task_id": task, "role": task.split("-")[0],
            "ready": error is None and not claimed and active_count < plan["max_parallel"],
            "dependency_error": error, "status": "claimed" if claimed else "expired" if entry.get("status") == "claimed" else entry.get("status", "pending"),
            "agent_id": entry.get("agent_id"),
            "depends_on": _dependencies(package, plan, state, task)})
    return {"package_dir": str(package), "mode": plan["mode"], "tasks": rows,
        "max_parallel": plan["max_parallel"], "active_claims": active_count}


def _input_text(package: Path, plan: dict, kind: str, ids: list[str] | None = None) -> str:
    return "\n\n".join(f"[{item['id']}]\n" + package_path(package, item["path"], "input").read_text(encoding="utf-8")
        for item in plan["inputs"][kind] if ids is None or item["id"] in ids)


def _paragraphs(text: str) -> list[dict[str, str]]:
    return [{"id": f"P{i:04d}", "text": p.strip()} for i, p in
        enumerate(re.split(r"\n\s*\n", text.strip()), 1) if p.strip()]


def _schema(task: str, style: str | None = None) -> dict:
    if task == "outline-check":
        return {"decision": "pass|revise", "coverage": [{"id": "O0001", "quote": "exact outline excerpt", "note": "check contradictions and missing prerequisites"}], "issues": []}
    if task == "chunk-plan":
        return {"style_contract": "approved voice, language and genre limits", "chunks": [{
            "id": "chunk-0001", "title": "planning label only", "brief": "what this block changes or establishes",
            "outline_ids": ["O0001"], "entry_state": "required starting facts", "exit_state": "required ending facts",
            "source_ids": [], "reference_ids": [], "depends_on": [], "independent": False}]}
    if task.startswith("write-"):
        return {"text": "complete prose, not a summary", "covered_outline_ids": ["O0001"],
            "state": {"stable.fact.key": "current fact, preserve all predecessor keys"},
            "state_changes": [{"key": "existing.key", "before": "old fact, or list of conflicting incoming values", "after": "new fact", "evidence": "exact excerpt showing change"}],
            "pending_threads": [], "resolved_threads": [{"thread": "incoming pending item", "evidence": "exact excerpt resolving it"}],
            "handoff": "compact continuation note"}
    if task.startswith("review-"):
        return {"decision": "pass|revise", "text_sha256": "digest supplied in assignment",
            "coverage": [{"id": "P0001", "quote": "exact paragraph excerpt", "note": "specific editorial assessment"}],
            "checks": {key: {"status": "pass|issue", "note": "evidence-based assessment"}
                for key in ("outline", "continuity", "voice", "naturalness", *(["sources"] if style in SERIOUS_STYLES else []))},
            "issues": [{"paragraph_id": "P0001", "quote": "exact excerpt", "reason": "specific defect", "suggestion": "local fix"}]}
    return {"decision": "pass|revise", "chunks": [{"id": "chunk-0001", "text_sha256": "current digest", "note": "outline and voice assessment"}],
        "boundaries": [{"left": "chunk-0001", "right": "chunk-0002", "left_quote": "ending excerpt", "right_quote": "opening excerpt", "note": "state and transition assessment"}],
        "revision_chunks": [], "issues": []}


def _incoming(package: Path, plan: dict, state: dict, task: str) -> list[tuple[int, dict]]:
    return [(int(dep.split("-")[1]), _result(package, state, _write_id(int(dep.split("-")[1]))))
        for dep in _dependencies(package, plan, state, task) if dep.startswith("review-")]


def _effective_incoming(package: Path, plan: dict, state: dict, task: str) -> list[tuple[int, dict]]:
    def ancestors(index):
        seen = set()
        queue = [index]
        while queue:
            for dep in _dependencies(package, plan, state, _write_id(queue.pop())):
                if dep.startswith("review-"):
                    number = int(dep.split("-")[1])
                    if number not in seen:
                        seen.add(number)
                        queue.append(number)
        return seen

    incoming = _incoming(package, plan, state, task)
    # An approved descendant already carries its ancestors' state. Conflicts
    # between incomparable branches must survive until explicitly reconciled.
    superseded = {i for j, _ in incoming for i in ancestors(j)}
    return [(i, prior) for i, prior in incoming if i not in superseded]


def _incoming_facts(package: Path, plan: dict, state: dict, task: str) -> dict:
    values: dict[str, list[str]] = {}
    for _, prior in _effective_incoming(package, plan, state, task):
        for key, value in prior["state"].items():
            if value not in values.setdefault(key, []):
                values[key].append(value)
    return {key: group[0] if len(group) == 1 else group for key, group in values.items()}


def _prompt(package: Path, plan: dict, state: dict, task: str, claim_token: str) -> str:
    schema = _json({"claim_token": claim_token, **_schema(task, plan["style"])})
    header = f"Role assignment: {task}\nReturn one JSON object using this shape (examples are not facts):\n{schema}\n"
    context = _input_text(package, plan, "context")
    if task == "outline-check":
        return header + "Check every outline unit against the canonical context. Quote each unit; flag contradictions, absent evidence and missing prerequisites. Do not rewrite or silently invent fixes. pass requires no unresolved issues.\n\nOutline:\n" + _input_text(package, plan, "outline") + "\nCanonical context:\n" + context
    if task == "chunk-plan":
        catalog = {kind: [{**item, "preview": package_path(package, item["path"], "input").read_text(encoding="utf-8")[:160]}
            for item in plan["inputs"][kind]] for kind in ("sources", "references")}
        return header + f"Allocate exactly {plan['chunk_count']} blocks in order; targets {plan['targets']} {plan['length_unit']}. Cover every outline unit without inventing events. Set explicit entry/exit contracts, factual source IDs and optional voice reference IDs. Read selected input files fully before assigning them; previews are discovery only. Execution mode: {plan['execution_mode']}. In contract mode, independent=true explicitly attests that a block can be written without predecessor drafts; otherwise declare earlier chunk dependencies. Shared characters/timelines usually require sequential dependencies. Labels are not prose subheadings.\n" + _input_text(package, plan, "outline") + "\nCanonical context:\n" + context + "\nInput catalog:\n" + _json(catalog)
    if task.startswith("write-"):
        index = int(task.split("-")[1])
        chunk = _chunk(package, state, index)
        incoming = [{"chunk_index": i, "pending_threads": r["pending_threads"], "handoff": r["handoff"], "ending": r["text"][-1000:]}
            for i, r in _effective_incoming(package, plan, state, task)]
        brief = _json(chunk) + f"\nWrite approximately {plan['targets'][index-1]} {plan['length_unit']}; accepted range 80%-120%. Do not pad. This is block {index}/{plan['chunk_count']}, not necessarily a chapter ending. Preserve all incoming state keys; changes require a literal quote showing the transition. Do not treat a planned state as an observed event. Carry pending replies, props, positions, promises, terminology and evidence limitations forward. For an incoming pending item no longer pending, include resolved_threads with the exact original thread and literal evidence of resolution in this prose. Return only this block's prose; do not recap earlier blocks.\n"
        if task in state["feedback"]:
            brief += "\nEditor feedback on previous attempt (read the referenced report, with pagination when needed, before revising):\n" + _json(state["feedback"][task])
        references = [str(package_path(package, item["path"], "reference")) for item in plan["inputs"]["references"] if item["id"] in chunk.get("reference_ids", [])]
        sources = [str(package_path(package, item["path"], "source")) for item in plan["inputs"]["sources"] if item["id"] in chunk.get("source_ids", [])]
        shared = "Canonical context:\n" + context + "\nRequired outline units:\n" + _input_text(package, plan, "outline", chunk["outline_ids"]) + "\nStyle contract:\n" + _result(package, state, "chunk-plan")["style_contract"] + "\nObserved predecessor state (read-only):\n" + _json(incoming) + "\nMerged incoming facts (list-valued conflicts require state_changes.before to repeat the full list and quote an explicit resolution):\n" + _json(_incoming_facts(package, plan, state, task))
        return header + compile_prompt(style=plan["style"], task=brief, context_text=shared,
            source_paths=sources, reference_paths=references,
            source_budget=max(5000, sum(Path(p).stat().st_size for p in sources)),
            reference_budget=max(3000, sum(Path(p).stat().st_size for p in references)))
    if task.startswith("review-"):
        index = int(task.split("-")[1])
        draft = _result(package, state, _write_id(index))
        modules = list(CORE_REVIEW_MODULES)
        if plan["style"] in {"fiction", "webnovel"} and has_directed_interaction(draft["text"]):
            modules.extend(VOICE_AUDIT_MODULES)
        if plan["style"] in {"academic-paper", "news-report", "formal-document"}:
            modules.extend(["protected-content", "source-grounding"])
        header += "\nRelevant editorial modules:\n" + "\n\n".join(skill.content for skill in load_many(modules)) + "\n"
        schema_note = "For serious documents add a sources check: verify assigned evidence, numbers, attribution and uncertainty; missing evidence requires narrowing, not invention.\n" if plan["style"] in {"academic-paper", "news-report", "formal-document"} else "For narrative prose check directed dialogue/actions receive a response or evidenced delay; track physical state and earned scene endings. Do not force a reaction after every line.\n"
        leads = lint_text(draft["text"], style=plan["style"]).to_dict()
        leads["total_findings"] = len(leads["findings"])
        leads["findings"] = leads["findings"][:20]
        chunk = _chunk(package, state, index)
        review_prompt = "\n\n".join([
            header,
            f"Independently review the complete {plan['style']} block. Cover every paragraph, use exact quotes, check outline adherence, voice, continuity and specific AI-like repetition/filler. Preserve useful ambiguity and voice. Do not flag a pattern solely because a detector might. pass requires no unresolved issues and all checks pass; otherwise request bounded local revision.",
            schema_note,
            "Contract:\n" + _json(chunk),
            "Style contract:\n" + _result(package, state, "chunk-plan")["style_contract"],
            "Canonical context:\n" + context,
            "Outline:\n" + _input_text(package, plan, "outline", chunk["outline_ids"]),
            "Observed incoming state and pending exchanges:\n" + _json([
                {"state": r["state"], "pending_threads": r["pending_threads"]}
                for _, r in _effective_incoming(package, plan, state, _write_id(index))]),
            "Writer state:\n" + _json({k: v for k, v in draft.items() if k not in {"text", "claim_token"}}),
            "text_sha256: " + _hash(draft["text"]),
            "Paragraphs:\n" + _json(_paragraphs(draft["text"])),
            "Deterministic leads (first 20, not automatic defects):\n" + _json(leads),
            "Assigned factual sources:\n" + _input_text(package, plan, "sources", chunk.get("source_ids", [])),
            "Supplied voice references:\n" + _input_text(package, plan, "references", chunk.get("reference_ids", [])),
        ])
        if len(review_prompt) <= MAX_PROMPT:
            return review_prompt
        review_path = package / f"review-input-{index:04d}-{claim_token}.md"
        atomic_write(review_path, review_prompt)
        return header + (
            f"\nPaged review assignment: {review_path}\n"
            f"Total characters: {len(review_prompt)}. Read the entire assignment with "
            "read_project_context, following offset/next_offset until next_offset is null. "
            "It contains the full prose, numbered paragraphs, outline, state and sources. "
            "Keep per-paragraph notes while reading; do not treat this pointer or the first page as full coverage. "
            "Submit the same current claim_token and all paragraph receipts.\n")
    summaries = []
    for i in range(1, plan["chunk_count"] + 1):
        draft = _result(package, state, _write_id(i))
        summaries.append({"id": f"chunk-{i:04d}", "text_sha256": _hash(draft["text"]),
            "result_path": state["entries"][_write_id(i)]["result_path"],
            "contract": _chunk(package, state, i), "state": draft["state"], "pending_threads": draft["pending_threads"],
            "handoff": draft["handoff"], "opening": draft["text"][:500], "ending": draft["text"][-500:]})
    # Large indexes stay on disk. The host can page through them instead of
    # inserting the entire book's accumulated ledgers into one model context.
    index_path = package / "continuity-index.json"
    atomic_write(index_path, _json(summaries))
    return header + "Act as the main continuity editor. Compare every adjacent boundary, outline coverage, stable voice, cumulative state and unresolved threads. Planned transitions need evidence in actual prose. Each chapter need not close every thread. Read every entry of the boundary manifest below, using offset/next_offset pagination with read_project_context if needed. Read result_path files for any non-boundary claim; do not claim to have read full bodies from excerpts. Return every chunk's current digest and every adjacent pair, quoting both sides. pass requires no unresolved issues; revise lists affected chunk IDs.\nCanonical context:\n" + context + "\nOutline:\n" + _input_text(package, plan, "outline") + f"\nBoundary manifest: {index_path}\nEntries: {plan['chunk_count']}. result_path values are relative to {package}.\n"


@serialized
def claim_writing_task(package_dir: str | Path, task_id: str, agent_id: str) -> dict[str, Any]:
    package, plan, state = _load(package_dir)
    _nonempty(agent_id, "agent_id", 100)
    error = _ready_error(package, plan, state, task_id)
    if error:
        raise ValueError(f"Task {task_id} is not ready: {error}")
    current = state["entries"].get(task_id, {})
    if _active(current) and current["agent_id"] != agent_id:
        raise ValueError("Task is already claimed by another agent.")
    if not _active(current) and sum(_active(e) for e in state["entries"].values()) >= plan["max_parallel"]:
        raise ValueError("Maximum parallel claims reached.")
    if task_id.startswith("review-"):
        writer = state["entries"][_write_id(int(task_id.split("-")[1]))]
        if writer["agent_id"] == agent_id:
            raise ValueError("A chunk must be reviewed by an agent other than its writer.")
    if task_id == "continuity" and any(state["entries"][_write_id(i)]["agent_id"] == agent_id for i in range(1, plan["chunk_count"] + 1)):
        raise ValueError("Final continuity reviewer must be independent of the chunk writers.")
    claim_token = current["claim_token"] if _active(current) else uuid.uuid4().hex
    prompt = _prompt(package, plan, state, task_id, claim_token)
    if len(prompt) > MAX_PROMPT:
        relative = f"results/{task_id}-{claim_token}-assignment.md"
        path = package_path(package, relative, "assignment")
        atomic_write(path, prompt)
        prompt = (f"Role assignment: {task_id}\nFull assignment: {path}\n"
            f"Assignment characters: {len(prompt)}\n"
            "Read the complete assignment with read_project_context using offset/next_offset pagination, "
            "then execute it. Do not use a preview or skip any assigned material. "
            "Return the current claim_token and the exact result schema supplied with this claim.\n")
    state["entries"][task_id] = {**current, "status": "claimed", "agent_id": agent_id,
        "claimed_at": datetime.now(timezone.utc).timestamp(), "claim_token": claim_token}
    _save(package, state)
    return {"task_id": task_id, "agent_id": agent_id, "content": prompt,
        "claim_token": claim_token, "lease_seconds": LEASE_SECONDS,
        "result_schema": {"claim_token": claim_token, **_schema(task_id, plan["style"])},
        "next_action": "Host runs this assignment, then submits the actual result with this claim_token and the same agent_id."}


def _quote(quote: Any, text: str) -> None:
    if not isinstance(quote, str) or not quote.strip() or quote not in text:
        raise ValueError("Evidence quote must occur literally in the assigned text.")


def _coverage(rows: Any, units: list[dict]) -> None:
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Coverage must be a list of evidence records.")
    if [r.get("id") for r in rows] != [u["id"] for u in units]:
        raise ValueError("Coverage must include every assigned unit once, in order.")
    for row, unit in zip(rows, units):
        _quote(row.get("quote"), unit["text"])
        if len(row["quote"].strip()) < min(8, len(unit["text"].strip())):
            raise ValueError("Coverage evidence is too short to identify the assigned unit.")
        _nonempty(row.get("note"), "coverage note", 2000)


def _decision(result: dict) -> str:
    decision = result.get("decision")
    if decision not in {"pass", "revise"} or not isinstance(result.get("issues"), list):
        raise ValueError("Review requires decision pass/revise and an issues list.")
    if (decision == "pass") != (not result["issues"]):
        raise ValueError("Pass requires no unresolved issues; revise requires specific issues.")
    return decision


def _validate(package: Path, plan: dict, state: dict, task: str, result: dict) -> None:
    if task == "outline-check":
        _decision(result)
        _coverage(result.get("coverage"), [{"id": u["id"], "text": package_path(package, u["path"], "input").read_text(encoding="utf-8")} for u in plan["inputs"]["outline"]])
    elif task == "chunk-plan":
        _nonempty(result.get("style_contract"), "style_contract", 2000)
        chunks = result.get("chunks")
        if not isinstance(chunks, list) or len(chunks) != plan["chunk_count"]:
            raise ValueError("Chunk count must match the target allocation.")
        outlines = {x["id"] for x in plan["inputs"]["outline"]}
        covered = set()
        for i, chunk in enumerate(chunks, 1):
            if not isinstance(chunk, dict) or chunk.get("id") != f"chunk-{i:04d}":
                raise ValueError("Chunks must have consecutive planned IDs.")
            for key in ("title", "brief", "entry_state", "exit_state"):
                _nonempty(chunk.get(key), key, 3000)
            ids = _strings(chunk.get("outline_ids"), "outline_ids")
            if not ids or not set(ids) <= outlines:
                raise ValueError("Every block must cite known outline IDs.")
            covered.update(ids)
            for field, kind in (("source_ids", "sources"), ("reference_ids", "references")):
                selected = _strings(chunk.get(field, []), field)
                if not set(selected) <= {u["id"] for u in plan["inputs"][kind]}:
                    raise ValueError(f"Unknown {field}.")
            deps = _strings(chunk.get("depends_on"), "depends_on")
            if any(d not in {f"chunk-{j:04d}" for j in range(1, i)} for d in deps):
                raise ValueError("Dependencies must refer to earlier chunks; cycles are forbidden.")
            if type(chunk.get("independent")) is not bool:
                raise ValueError("independent must be an explicit boolean.")
            if plan["execution_mode"] == "contract" and i > 1 and not deps and not chunk["independent"]:
                raise ValueError("Parallel blocks require explicit independence and entry/exit contracts.")
        if covered != outlines:
            raise ValueError("Chunk plan does not cover every outline unit.")
    elif task.startswith("write-"):
        index = int(task.split("-")[1])
        text = _nonempty(result.get("text"), "text", 80000)
        target = plan["targets"][index - 1]
        size = count_length(text, plan["length_unit"])
        if not math.ceil(target * .8) <= size <= math.ceil(target * 1.2):
            raise ValueError(f"Draft length {size} is outside 80%-120% of target {target}.")
        if set(_strings(result.get("covered_outline_ids"), "covered_outline_ids")) != set(_chunk(package, state, index)["outline_ids"]):
            raise ValueError("Writer must cover exactly the assigned outline IDs.")
        ledger = result.get("state")
        if not isinstance(ledger, dict) or len(ledger) > 150:
            raise ValueError("state must be a compact object of at most 150 persistent facts.")
        for key, value in ledger.items():
            _nonempty(key, "state key", 100)
            _nonempty(value, "state value", 300)
        if len(_json(ledger)) > 8000:
            raise ValueError("State ledger exceeds 8000 characters; compact the project scope.")
        changes = result.get("state_changes")
        if not isinstance(changes, list) or any(not isinstance(c, dict) for c in changes):
            raise ValueError("state_changes must be a list of evidence records.")
        old = _incoming_facts(package, plan, state, task)
        for key, before in old.items():
            if key not in ledger:
                raise ValueError(f"Incoming fact {key} disappeared from the handoff state.")
            if ledger[key] != before:
                change = next((c for c in changes if c.get("key") == key and c.get("before") == before and c.get("after") == ledger[key]), None)
                if not change:
                    raise ValueError(f"Changed fact {key} needs an evidenced transition.")
        for change in changes:
            if change.get("key") not in old or change.get("before") != old[change["key"]] or change.get("after") != ledger.get(change["key"]):
                raise ValueError("State change must match incoming and outgoing facts.")
            _quote(change.get("evidence"), text)
        threads = _strings(result.get("pending_threads"), "pending_threads")
        if len(threads) > 30 or any(len(t) > 300 for t in threads):
            raise ValueError("pending_threads must remain compact.")
        resolved = result.get("resolved_threads", [])
        if not isinstance(resolved, list) or any(not isinstance(r, dict) for r in resolved):
            raise ValueError("resolved_threads must be evidence records.")
        incoming_threads = {thread for _, prior in _effective_incoming(package, plan, state, task) for thread in prior["pending_threads"]}
        for record in resolved:
            if record.get("thread") not in incoming_threads or record["thread"] in threads:
                raise ValueError("Resolution must refer to an incoming item no longer pending.")
            _quote(record.get("evidence"), text)
        if incoming_threads - set(threads) != {record["thread"] for record in resolved}:
            raise ValueError("Incoming pending threads cannot disappear without resolution evidence.")
        _nonempty(result.get("handoff"), "handoff", 2000)
    elif task.startswith("review-"):
        decision = _decision(result)
        draft = _result(package, state, _write_id(int(task.split("-")[1])))
        if result.get("text_sha256") != _hash(draft["text"]):
            raise ValueError("Review digest does not match the current draft.")
        paragraphs = _paragraphs(draft["text"])
        _coverage(result.get("coverage"), paragraphs)
        checks = result.get("checks")
        required = {"outline", "continuity", "voice", "naturalness"}
        if plan["style"] in {"academic-paper", "news-report", "formal-document"}:
            required.add("sources")
        if not isinstance(checks, dict) or not required <= checks.keys():
            raise ValueError("Review lacks required genre-specific checks.")
        for check in checks.values():
            if not isinstance(check, dict) or check.get("status") not in {"pass", "issue"}:
                raise ValueError("Review checks require pass/issue status.")
            _nonempty(check.get("note"), "check note", 2000)
            if decision == "pass" and check["status"] != "pass":
                raise ValueError("An unresolved check prevents approval.")
        for issue in result["issues"]:
            if not isinstance(issue, dict):
                raise ValueError("Editorial issues require paragraph evidence.")
            para = next((p for p in paragraphs if p["id"] == issue.get("paragraph_id")), None)
            if not para:
                raise ValueError("Issue cites an unknown paragraph.")
            _quote(issue.get("quote"), para["text"])
            _nonempty(issue.get("reason"), "issue reason", 2000)
            _nonempty(issue.get("suggestion"), "issue suggestion", 2000)
    else:
        decision = _decision(result)
        chunks = result.get("chunks")
        expected = [f"chunk-{i:04d}" for i in range(1, plan["chunk_count"] + 1)]
        if not isinstance(chunks, list) or any(not isinstance(c, dict) for c in chunks) or [c.get("id") for c in chunks] != expected:
            raise ValueError("Final review must cover every chunk in order.")
        for i, chunk in enumerate(chunks, 1):
            if chunk.get("text_sha256") != _hash(_result(package, state, _write_id(i))["text"]):
                raise ValueError("Final review contains a stale draft digest.")
            _nonempty(chunk.get("note"), "chunk assessment", 2000)
        boundaries = result.get("boundaries")
        if not isinstance(boundaries, list) or len(boundaries) != len(expected) - 1:
            raise ValueError("Final review must cover every adjacent boundary.")
        for i, row in enumerate(boundaries, 1):
            if not isinstance(row, dict) or (row.get("left"), row.get("right")) != (expected[i-1], expected[i]):
                raise ValueError("Boundary IDs must match adjacent chunks.")
            _quote(row.get("left_quote"), _result(package, state, _write_id(i))["text"][-500:])
            _quote(row.get("right_quote"), _result(package, state, _write_id(i + 1))["text"][:500])
            _nonempty(row.get("note"), "boundary assessment", 2000)
        revisions = _strings(result.get("revision_chunks"), "revision_chunks")
        if not set(revisions) <= set(expected) or (decision == "pass" and revisions) or (decision == "revise" and not revisions):
            raise ValueError("Final revision requests must identify affected chunks.")


def _invalidate(package: Path, plan: dict, state: dict, changed: str) -> None:
    affected = {changed}
    for task in _tasks(plan):
        if any(dep in affected for dep in _dependencies(package, plan, state, task)):
            affected.add(task)
    for task in affected:
        entry = state["entries"].get(task)
        if entry:
            entry["status"] = "stale"


@serialized
def submit_writing_result(package_dir: str | Path, task_id: str, result: dict, agent_id: str) -> dict[str, Any]:
    package, plan, state = _load(package_dir)
    if not isinstance(result, dict):
        raise ValueError("result must be an object.")
    if len(_json(result)) > MAX_RESULT:
        raise ValueError("Writing result exceeds the per-task limit.")
    error = _ready_error(package, plan, state, task_id)
    if error:
        raise ValueError(f"Task {task_id} is not ready: {error}")
    entry = state["entries"].get(task_id, {})
    if not _active(entry) or entry.get("agent_id") != agent_id:
        raise ValueError("Task must have an active claim and be submitted by the same agent.")
    if result.get("claim_token") != entry["claim_token"]:
        raise ValueError("Result claim_token does not match the current assignment; stale results cannot be submitted.")
    _validate(package, plan, state, task_id, result)
    version = entry.get("version", 0) + 1
    relative = f"results/{task_id}-v{version}.json"
    stored = _json(result)
    atomic_write(package_path(package, relative, "result"), stored)
    state["entries"][task_id] = {"status": "submitted", "agent_id": agent_id,
        "version": version, "result_path": relative, "sha256": _hash(stored)}
    revise = result.get("decision") == "revise"
    if revise:
        if task_id.startswith("review-"):
            targets = [_write_id(int(task_id.split("-")[1]))]
        elif task_id == "continuity":
            targets = [_write_id(int(chunk.split("-")[1])) for chunk in result["revision_chunks"]]
        else:
            targets = []
        for target in targets:
            state["feedback"][target] = {"from_task": task_id, "result_path": str(package / relative),
                "focus_chunk": target.replace("write-", "chunk-"),
                "instruction": "Read the actual report. Resolve the relevant issues; never treat this pointer as an approval."}
            count = state["revision_counts"].get(target, 0) + 1
            state["revision_counts"][target] = count
            _invalidate(package, plan, state, target)
            if count > MAX_REVISIONS:
                state["blocked"][target] = "Revision budget exhausted; correct the brief or inputs and create a new package."
        if not targets:
            state["blocked"][task_id] = "Outline requires correction; create a new package from the corrected immutable inputs."
    _save(package, state)
    return {"task_id": task_id, "status": "blocked" if task_id in state["blocked"] else "revision_requested" if revise else "submitted",
        "result_path": relative, "result_sha256": _hash(stored), "blocked_tasks": state["blocked"]}


def verify_writing_project(package_dir: str | Path) -> dict[str, Any]:
    package, plan, state = _load(package_dir)
    incomplete = []
    for task in _tasks(plan):
        result = _result(package, state, task)
        if not result or result.get("decision", "pass") != "pass":
            incomplete.append(task)
    return {"package_dir": str(package), "ready_for_assembly": not incomplete,
        "chunk_count": plan["chunk_count"], "incomplete_tasks": incomplete,
        "blocked_tasks": state["blocked"], "length_unit": plan["length_unit"],
        "target_length": plan["target_length"], "semantic_quality": "agent-reviewed, not programmatically guaranteed"}


def _publish_new_text(output: Path, text: str) -> None:
    fd, temporary = tempfile.mkstemp(prefix=".writing-", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        # A same-directory hard link makes the completed file visible atomically
        # and fails if any other package has already published to this path.
        try:
            os.link(temporary, output)
        except FileExistsError as exc:
            raise ValueError("Assembly output already exists; it was not overwritten.") from exc
    finally:
        os.unlink(temporary)


def assemble_writing_project(package_dir: str | Path, output_path: str | Path) -> dict[str, Any]:
    package = Path(package_dir).resolve()
    with package_lock(package):
        verification = verify_writing_project(package)
        if not verification["ready_for_assembly"]:
            raise ValueError("Every writing, editorial and continuity task must pass before assembly.")
        package, plan, state = _load(package)
        output = Path(output_path).resolve()
        if output.exists() or str(output) in plan["original_paths"]:
            raise ValueError("Assembly must use a new output path; existing files are never overwritten.")
        if output.is_relative_to(package) and output != package / "manuscript.md":
            raise ValueError("Inside the writing package, assembly output must be manuscript.md.")
        text = "\n\n".join(_result(package, state, _write_id(i))["text"].strip()
            for i in range(1, plan["chunk_count"] + 1)) + "\n"
        output.parent.mkdir(parents=True, exist_ok=True)
        _publish_new_text(output, text)
        return {"output_path": str(output), "sha256": _hash(text), "length": count_length(text, plan["length_unit"]),
            "length_unit": plan["length_unit"], "chunk_count": plan["chunk_count"]}
