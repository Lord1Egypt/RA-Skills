#!/usr/bin/env python3
"""Generate self-contained HTML viewer for prompt-eval results.

Supports progressive phases:
  Phase A (--phase stage2): Test case browser with inputs only
  Phase B (--phase stage3): Outputs appended to each case
  Phase C (--phase stage5): Scores attached below outputs as rubric + feedback enabled
  Phase D (--phase stage6): With --previous, diff view between two runs

The Effect tab is added automatically whenever effect-lane artifacts
(effect_raw_judgments.json / effect_summary.json) exist in the output directory.
No extra flag is needed.

Usage:
  python generate_viewer.py <output_dir> --phase stage2 --title "My Prompt"
  python generate_viewer.py <output_dir> --phase stage3
  python generate_viewer.py <output_dir> --phase stage5
  python generate_viewer.py <output_dir> --phase stage6 --previous <prev_dir>

Static export:
  python generate_viewer.py <output_dir> --phase stage5 --static result.html
"""

import argparse
import base64
import csv
import io
import json
import mimetypes
import os
import re
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

# Output type classification
TEXT_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".tsx",
                   ".yaml", ".yml", ".xml", ".html", ".css", ".sh", ".rb", ".go",
                   ".rs", ".java", ".c", ".cpp", ".h", ".hpp", ".sql", ".r", ".toml"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def classify_content_type(text):
    """Infer the best rendering mode for output text."""
    if text is None:
        return "null"
    text = text.strip()
    if not text:
        return "empty"
    if text.startswith("{") or text.startswith("["):
        try:
            json.loads(text)
            return "json"
        except (json.JSONDecodeError, ValueError):
            pass
    if text.startswith("<") and ">" in text[:100]:
        lower = text[:200].lower()
        if any(tag in lower for tag in ["<html", "<xml", "<context", "<message", "<response"]):
            return "xml"
    if re.search(r"^#{1,6}\s", text, re.MULTILINE) or "```" in text:
        return "markdown"
    if re.search(r"^\s*(def |function |class |import |from |package |const |let |var )", text, re.MULTILINE):
        return "code"
    return "text"


def parse_csv_scores(csv_path):
    """Parse final_scored_results.csv into a dict keyed by test_id."""
    if not csv_path.exists():
        return {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["test_id"]: dict(row) for row in reader}


def extract_tp_scores(case_data):
    """Extract only valid 1-3 Test Point scores and their paired reasons.

    Summary fields such as total_score, avg_tp_score, and score_pct are never
    Test Points. They must not enter the denominator or any TP aggregation.
    """
    scores = {}
    reasons = {}
    for key, value in case_data.items():
        if not key.startswith("TP"):
            continue
        if key.endswith("_score"):
            tp_id = key[:-len("_score")]
            try:
                score = int(value)
            except (TypeError, ValueError):
                continue
            if score in (1, 2, 3):
                scores[tp_id] = score
        elif key.endswith("_reason"):
            reasons[key[:-len("_reason")]] = value
    return scores, reasons


def apply_score_summary(run):
    """Compute all score summaries locally from valid TP scores."""
    values = [score for score in run["scores"].values() if score in (1, 2, 3)]
    total = sum(values)
    applicable = len(values)
    max_score = applicable * 3
    run["total_score"] = total
    run["max_score"] = max_score
    run["avg_tp_score"] = round(total / applicable, 2) if applicable else None
    run["score_pct"] = round(total / max_score * 100) if max_score else None
    run["is_bad_case"] = bool(values) and (
        run["score_pct"] <= 50 or any(score == 1 for score in values)
    )


def active_iteration_dir(output_dir):
    """Resolve the active iteration for the new project/iteration layout.

    Old flat run directories keep working: absent manifest means `output_dir` is
    itself the iteration directory.
    """
    root = Path(output_dir)
    manifest = _read_json(root / "run_manifest.json") or {}
    active = manifest.get("active_iteration")
    if active:
        candidate = root / active
        if candidate.is_dir():
            return candidate
    return root


def artifact_path(output_dir, relative_path, legacy_name=None):
    """Prefer active iteration paths; fall back to candidate and legacy paths."""
    iteration = active_iteration_dir(output_dir)
    candidate_paths = [relative_path]
    candidate_fallbacks = {
        "design/test_cases.json": ["validation/cases.json"],
        "execution/candidate_outputs.json": ["validation/candidate_outputs.json"],
        "scoring/functional/scored_results.json": ["validation/functional_scores.json"],
    }
    candidate_paths.extend(candidate_fallbacks.get(relative_path, []))
    for relative in candidate_paths:
        candidate = iteration / relative
        if candidate.exists():
            return candidate
    if legacy_name:
        legacy = Path(output_dir) / legacy_name
        if legacy.exists():
            return legacy
    return iteration / relative_path


def load_phase_a(output_dir):
    """Load functional test definitions from active iteration or legacy run."""
    path = artifact_path(output_dir, "design/test_cases.json", "test_cases.json")
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("test_cases", data) if isinstance(data, dict) else data
    if not isinstance(cases, list):
        cases = [cases]
    return [_build_case_a(c) for c in cases]


def _build_case_a(c):
    return {
        "test_id": c.get("test_id", ""),
        "test_category": c.get("test_category", ""),
        "test_subcategory": c.get("test_subcategory", ""),
        "eval_type": c.get("eval_type", "quantitative"),
        "test_description": c.get("test_description", ""),
        "input": c.get("input", {}),
        "expected_behavior": c.get("expected_behavior", ""),
        "output": None,
        "scores": {},
        "reasons": {},
        "total_score": None,
        "avg_tp_score": None,
        "score_pct": None,
        "overall_comment": "",
        "is_bad_case": False,
        "run_status": "pending",
        "phase": "A",
        "content_type": "null",
    }


def apply_phase_b(runs, output_dir):
    """Apply execution results from test_cases_with_results.json or execution_scores.json."""
    # Priority 1: test_cases_with_results.json
    path = artifact_path(output_dir, "execution/candidate_outputs.json", "test_cases_with_results.json")
    if not path.exists():
        path = artifact_path(output_dir, "execution/execution_scores.json", "execution_scores.json")
    if not path.exists():
        return runs

    data = json.loads(path.read_text(encoding="utf-8"))
    results = data if isinstance(data, list) else data.get(
        "test_cases", data.get("executed_results", data)
    )
    if not isinstance(results, list):
        results = [results] if isinstance(results, dict) else []

    result_map = {}
    for r in results:
        result_map[r["test_id"]] = r.get("result_aftertest")

    for run in runs:
        if run["test_id"] in result_map:
            output = result_map[run["test_id"]]
            run["output"] = output
            run["content_type"] = classify_content_type(output)
            run["run_status"] = "failed" if output is None else "ok"
            run["phase"] = "B"
    return runs


def apply_phase_c(runs, output_dir):
    """Apply scores from final_scored_results.json, execution_scores.json, or CSV."""
    json_path = artifact_path(output_dir, "scoring/functional/scored_results.json", "final_scored_results.json")
    csv_path = artifact_path(output_dir, "scoring/functional/scored_results.csv", "final_scored_results.csv")
    exec_path = artifact_path(output_dir, "execution/execution_scores.json", "execution_scores.json")

    # Priority 1: per-case array from final_scored_results.json
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            score_map = {item["test_id"]: item for item in data}
            for run in runs:
                if run["test_id"] in score_map:
                    _apply_scores_to_run(run, score_map[run["test_id"]])

    # Priority 2: execution_scores.json (scores use "TP1_mandatory_collection" format)
    if exec_path.exists():
        data = json.loads(exec_path.read_text(encoding="utf-8"))
        exec_results = data.get("executed_results", [])
        for er in exec_results:
            tid = er.get("test_id")
            run = next((r for r in runs if r["test_id"] == tid), None)
            if not run:
                continue
            if not run.get("output") and er.get("result_aftertest"):
                run["output"] = er["result_aftertest"]
                run["content_type"] = classify_content_type(er["result_aftertest"])
                run["run_status"] = "ok"
                if run["phase"] < "B":
                    run["phase"] = "B"
            # Only apply exec scores if run hasn't been scored by Priority 1
            # and exec entry actually has score data
            scores_raw = er.get("scores", {})
            if scores_raw and run["phase"] < "C":
                reasons_raw = er.get("score_reasons", {})
                scores = {}
                reasons = {}
                for k, v in scores_raw.items():
                    parts = k.split("_", 1)
                    tp_id = parts[0] if parts[0].startswith("TP") else k
                    scores[tp_id] = int(v)
                    reasons[tp_id] = reasons_raw.get(tp_id, reasons_raw.get(k, ""))
                run["scores"] = scores
                run["reasons"] = reasons
                apply_score_summary(run)
                run["phase"] = "C"

    # Priority 3: CSV
    if csv_path.exists():
        csv_scores = parse_csv_scores(csv_path)
        for run in runs:
            if run["test_id"] in csv_scores:
                _apply_scores_to_run(run, csv_scores[run["test_id"]])

    return runs


def _apply_scores_to_run(run, score_data):
    scores, reasons = extract_tp_scores(score_data)
    run["scores"] = scores
    run["reasons"] = reasons
    apply_score_summary(run)
    run["overall_comment"] = score_data.get("overall_comment", "")
    run["run_status"] = score_data.get("run_status", "ok")
    run["phase"] = "C"


def load_previous_runs(output_dir):
    """Load data from a previous run for diff view."""
    if not output_dir:
        return None
    prev_dir = Path(output_dir)
    if not prev_dir.exists():
        return None
    runs = load_phase_a(prev_dir)
    runs = apply_phase_b(runs, prev_dir)
    runs = apply_phase_c(runs, prev_dir)
    return [r for r in runs if isinstance(r, dict)]


def build_benchmark(runs):
    """Build benchmark stats from scored runs."""
    scored = [r for r in runs if isinstance(r, dict) and r["phase"] >= "C"]
    if not scored:
        return None

    # Collect all TP IDs
    tp_ids = set()
    for r in scored:
        tp_ids.update(r["scores"].keys())

    tp_stats = []
    for tp_id in sorted(tp_ids):
        vals = [r["scores"].get(tp_id) for r in scored if r["scores"].get(tp_id)]
        if not vals:
            continue
        avg = round(sum(vals) / len(vals), 2)
        tp_stats.append({
            "id": tp_id,
            "count": len(vals),
            "avg": avg,
            "dist": {"1": vals.count(1), "2": vals.count(2), "3": vals.count(3)},
            "pass_rate": round(vals.count(3) / len(vals) * 100),
            "status": "✅" if avg >= 2.5 else "⚠️" if avg >= 2.0 else "❌",
        })

    # Dimension stats
    dims = {}
    for r in scored:
        cat = r.get("test_category", "unknown")
        if cat not in dims:
            dims[cat] = {"total": 0, "bad": 0, "pass": 0}
        dims[cat]["total"] += 1
        if r["is_bad_case"]:
            dims[cat]["bad"] += 1
        if r.get("avg_tp_score", 0) >= 2.0:
            dims[cat]["pass"] += 1

    dim_stats = []
    for name, stats in sorted(dims.items()):
        pct = round(stats["pass"] / stats["total"] * 100) if stats["total"] else 0
        dim_stats.append({"name": name, **stats, "pass_pct": pct})

    bad_count = sum(1 for r in scored if r["is_bad_case"])
    safety_fail = sum(1 for r in scored
                      if r.get("eval_type") == "safety"
                      and r["scores"].get("TP_safety") == 1)

    return {
        "tps": tp_stats,
        "dimensions": dim_stats,
        "total_cases": len(scored),
        "bad_count": bad_count,
        "safety_failures": safety_fail,
        "overall_pass_rate": round(
            sum(1 for r in scored if r.get("avg_tp_score", 0) >= 2.5) / len(scored) * 100
        ),
    }


def _read_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return None


def _as_list(data, *keys):
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            if isinstance(data.get(key), list):
                return data[key]
    return []


def _percentile(values, pct):
    if not values:
        return None
    ordered = sorted(values)
    idx = (len(ordered) - 1) * pct
    low, high = int(idx), min(int(idx) + 1, len(ordered) - 1)
    return round(ordered[low] + (ordered[high] - ordered[low]) * (idx - low), 3)


def _unblind(judgment):
    """Resolve a blinded winner label into candidate / baseline / tie."""
    winner = str(judgment.get("winner", "")).strip().lower()
    if winner in ("candidate", "baseline", "tie"):
        return winner
    mapping = judgment.get("presented_as") or {}
    normalized = {str(k).strip().lower(): str(v).strip().lower()
                  for k, v in mapping.items()}
    resolved = normalized.get(winner)
    if resolved in ("candidate", "baseline"):
        return resolved
    return "tie"


def load_effect(output_dir):
    """Load and aggregate effect-evaluation artifacts. Returns None when absent."""
    raw = _as_list(_read_json(artifact_path(output_dir, "scoring/effect/raw_judgments.json",
                                              "effect_raw_judgments.json")), "judgments", "records")
    summary = _read_json(artifact_path(output_dir, "scoring/effect/summary.json",
                                       "effect_summary.json")) or {}
    validity = _read_json(artifact_path(output_dir, "scoring/effect/validity.json",
                                        "effect_validity.json")) or {}
    personas = _as_list(_read_json(artifact_path(output_dir, "design/effect_personas.json",
                                                  "effect_personas.json")), "personas")
    cases = _as_list(_read_json(artifact_path(output_dir, "design/effect_cases.json",
                                               "effect_cases.json")), "effect_cases", "cases")
    profile = _read_json(artifact_path(output_dir, "design/effect_profile.json",
                                       "effect_profile.json")) or {}

    if not raw and not summary and not personas and not cases:
        return None

    persona_map = {p.get("persona_id"): p for p in personas if isinstance(p, dict)}
    case_map = {c.get("test_id", c.get("case_id")): c for c in cases if isinstance(c, dict)}

    scored = [j for j in raw if isinstance(j, dict) and not j.get("is_anchor")]
    anchors = [j for j in raw if isinstance(j, dict) and j.get("is_anchor")]
    panel = _build_panel(personas, cases, profile)

    if not scored and not summary:
        # Step 2E: panel and cases exist, judging has not run yet.
        return {
            "enabled": True,
            "stage": "design",
            "baseline_type": (_read_json(out / "baseline_spec.json") or {}).get(
                "baseline_type", "not yet selected"),
            "judges": len(personas),
            "cases": len(cases),
            "success_action": (profile.get("success_action") or {}).get("primary", ""),
            "target_user": (profile.get("target_user") or {}).get("who", ""),
            "panel": panel,
            "case_rows": [],
            "segments": [],
            "gates": [],
            "dealbreakers": [],
            "validity": None,
            "overall_win_rate": None,
            "action_rate": None,
            "median_win_rate": None,
            "p25_win_rate": None,
        }

    by_case = {}
    for j in scored:
        cid = j.get("case_id") or j.get("test_id") or "unknown"
        by_case.setdefault(cid, []).append(j)

    case_rows = []
    for cid, judgments in by_case.items():
        votes = {"candidate": 0, "baseline": 0, "tie": 0}
        acts = {"yes": 0, "maybe": 0, "no": 0}
        rows = []
        for j in judgments:
            side = _unblind(j)
            votes[side] += 1
            act = str(j.get("would_act", "")).strip().lower()
            if act in acts:
                acts[act] += 1
            persona = persona_map.get(j.get("persona_id"), {})
            rows.append({
                "persona_id": j.get("persona_id", ""),
                "label": persona.get("label", ""),
                "stance": persona.get("stance", ""),
                "decision_role": persona.get("decision_role", ""),
                "winner": side,
                "margin": j.get("margin", ""),
                "would_act": act,
                "reason": j.get("reason", ""),
                "deal_breaker": j.get("deal_breaker", ""),
            })
        total = max(len(judgments), 1)
        win_rate = (votes["candidate"] + 0.5 * votes["tie"]) / total
        top = max(votes.values())
        source = case_map.get(cid, {})
        case_rows.append({
            "case_id": cid,
            "effect_case_type": source.get("effect_case_type", ""),
            "win_rate": round(win_rate * 100, 1),
            "votes": votes,
            "acts": acts,
            "action_rate": round(acts["yes"] / total * 100, 1),
            "divergence": round((1 - top / total) * 100, 1),
            "judge_count": len(judgments),
            "candidate_output": source.get("candidate_output"),
            "baseline_output": source.get("baseline_output"),
            "judgments": sorted(rows, key=lambda r: (r["winner"] != "baseline", r["persona_id"])),
        })
    case_rows.sort(key=lambda c: c["win_rate"])

    segments = summary.get("segments") or []
    if not segments and scored:
        buckets = {}
        for j in scored:
            persona = persona_map.get(j.get("persona_id"), {})
            name = persona.get("stance") or "unsegmented"
            b = buckets.setdefault(name, {"name": name, "wins": 0.0, "total": 0,
                                          "yes": 0, "judges": set()})
            side = _unblind(j)
            b["wins"] += 1 if side == "candidate" else 0.5 if side == "tie" else 0
            b["total"] += 1
            if str(j.get("would_act", "")).strip().lower() == "yes":
                b["yes"] += 1
            b["judges"].add(j.get("persona_id"))
        segments = [{
            "name": b["name"],
            "judges": len(b["judges"]),
            "win_rate": round(b["wins"] / max(b["total"], 1) * 100, 1),
            "action_rate": round(b["yes"] / max(b["total"], 1) * 100, 1),
        } for b in sorted(buckets.values(), key=lambda x: x["name"])]

    win_rates = [c["win_rate"] for c in case_rows]
    overall = summary.get("overall_win_rate")
    if overall is not None and overall <= 1:
        overall = round(overall * 100, 1)
    if overall is None and scored:
        wins = sum(1 if _unblind(j) == "candidate" else 0.5 if _unblind(j) == "tie" else 0
                   for j in scored)
        overall = round(wins / len(scored) * 100, 1)

    yes_total = sum(1 for j in scored
                    if str(j.get("would_act", "")).strip().lower() == "yes")
    dealbreakers = _load_dealbreakers(output_dir, scored, persona_map)
    gates = _build_gates(validity, anchors, scored)

    return {
        "enabled": True,
        "stage": "results",
        "baseline_type": summary.get("baseline_type") or "unspecified",
        "judges": summary.get("judges") or len({j.get("persona_id") for j in scored}),
        "cases": summary.get("cases") or len(case_rows),
        "calls_used": summary.get("calls_used"),
        "overall_win_rate": overall,
        "action_rate": round(yes_total / len(scored) * 100, 1) if scored else None,
        "median_win_rate": _percentile(win_rates, 0.5),
        "p25_win_rate": _percentile(win_rates, 0.25),
        "success_action": (profile.get("success_action") or {}).get("primary", ""),
        "target_user": (profile.get("target_user") or {}).get("who", ""),
        "validity": validity.get("overall") or gates.get("overall"),
        "gates": gates.get("gates", []),
        "segments": segments,
        "panel": panel,
        "case_rows": case_rows,
        "dealbreakers": dealbreakers,
        "personas": [{"persona_id": p.get("persona_id"), "label": p.get("label"),
                      "stance": p.get("stance"), "decision_role": p.get("decision_role"),
                      "attention": p.get("attention")}
                     for p in personas if isinstance(p, dict)],
    }


def _build_panel(personas, cases, profile):
    """Summarize the judge panel and effect cases for the design-stage review."""
    def tally(key):
        counts = {}
        for p in personas:
            if isinstance(p, dict):
                counts[p.get(key) or "unspecified"] = counts.get(p.get(key) or "unspecified", 0) + 1
        return [{"name": k, "count": v,
                 "pct": round(v / max(len(personas), 1) * 100)}
                for k, v in sorted(counts.items(), key=lambda kv: -kv[1])]

    stances = tally("stance")
    adversarial = next((s["count"] for s in stances if s["name"] == "adversarial"), 0)
    adv_pct = round(adversarial / max(len(personas), 1) * 100)

    case_types = {}
    for c in cases:
        if isinstance(c, dict):
            t = c.get("effect_case_type") or "derived"
            case_types[t] = case_types.get(t, 0) + 1

    checks = [
        {"label": "Adversarial judges >= 40%", "value": f"{adv_pct}%",
         "pass": adv_pct >= 40},
        {"label": "Decision roles covered >= 3", "value": str(len(tally("decision_role"))),
         "pass": len(tally("decision_role")) >= 3},
        {"label": "Panel size >= 10", "value": str(len(personas)),
         "pass": len(personas) >= 10},
        {"label": "Effect cases <= 20", "value": str(len(cases)),
         "pass": 0 < len(cases) <= 20},
    ]

    return {
        "profile": {
            "business_goal": profile.get("business_goal", ""),
            "target_user": (profile.get("target_user") or {}).get("who", ""),
            "success_action": (profile.get("success_action") or {}).get("primary", ""),
            "failure_risks": profile.get("failure_risks", []),
            "use_context": profile.get("use_context", {}),
            "decision_criteria": profile.get("decision_criteria", []),
            "stakes": profile.get("stakes", ""),
            "inferred_fields": profile.get("inferred_fields", []),
        },
        "stances": stances,
        "roles": tally("decision_role"),
        "attention": tally("attention"),
        "adversarial_pct": adv_pct,
        "checks": checks,
        "case_types": [{"name": k, "count": v} for k, v in sorted(case_types.items())],
        "personas": [{
            "persona_id": p.get("persona_id", ""),
            "label": p.get("label", ""),
            "stance": p.get("stance", ""),
            "decision_role": p.get("decision_role", ""),
            "attention": p.get("attention", ""),
            "current_situation": p.get("current_situation", ""),
            "what_they_care_about": p.get("what_they_care_about", []),
            "what_makes_them_act": p.get("what_makes_them_act", ""),
            "what_makes_them_bounce": p.get("what_makes_them_bounce", []),
            "action_threshold": p.get("action_threshold", ""),
            "is_core": bool(p.get("is_core_screening_judge")),
        } for p in personas if isinstance(p, dict)],
        "cases": [{
            "case_id": c.get("test_id", c.get("case_id", "")),
            "effect_case_type": c.get("effect_case_type", "derived"),
            "source": c.get("source", ""),
            "visible_portion": c.get("visible_portion", "full"),
            "persona_scope": c.get("persona_scope", "all"),
            "input": c.get("input", {}),
        } for c in cases if isinstance(c, dict)],
    }


def _load_dealbreakers(output_dir, scored, persona_map):
    csv_path = artifact_path(output_dir, "scoring/effect/dealbreakers.csv",
                             "effect_dealbreakers.csv")
    if csv_path.exists():
        with open(csv_path, "r", encoding="utf-8") as f:
            return [dict(row) for row in csv.DictReader(f)]
    counts = {}
    for j in scored:
        quote = str(j.get("deal_breaker") or "").strip()
        if not quote or quote.lower() == "none":
            continue
        key = quote.lower()[:80]
        entry = counts.setdefault(key, {"cluster_label": quote[:90],
                                        "mention_count": 0,
                                        "representative_quote": quote,
                                        "dominant_segment": "",
                                        "stances": {}})
        entry["mention_count"] += 1
        stance = persona_map.get(j.get("persona_id"), {}).get("stance", "unsegmented")
        entry["stances"][stance] = entry["stances"].get(stance, 0) + 1
    rows = []
    for entry in counts.values():
        stances = entry.pop("stances")
        entry["dominant_segment"] = max(stances, key=stances.get) if stances else ""
        rows.append(entry)
    rows.sort(key=lambda r: -r["mention_count"])
    return rows[:20]


def _build_gates(validity, anchors, scored):
    """Use effect_validity.json when present, otherwise derive what we can."""
    if validity.get("gate_1_anchor_accuracy") is not None:
        gates = []
        for key, label in (("gate_1_anchor_accuracy", "Anchor accuracy"),
                           ("gate_2_divergence", "Divergence"),
                           ("gate_3_position_bias", "Position bias"),
                           ("gate_4_discrimination", "Discrimination")):
            g = validity.get(key) or {}
            value = g.get("value", g.get("high_divergence_share",
                          g.get("sample_one_win_share", g.get("win_rate"))))
            gates.append({"label": label, "value": value, "pass": bool(g.get("pass"))})
        return {"gates": gates, "overall": validity.get("overall")}

    gates = []
    if anchors:
        correct = sum(1 for a in anchors if a.get("anchor_correct"))
        gates.append({"label": "Anchor accuracy",
                      "value": round(correct / len(anchors), 3),
                      "pass": correct / len(anchors) >= 0.85})
    if scored:
        one = sum(1 for j in scored if str(j.get("winner", "")).lower() == "sample_one")
        share = one / len(scored)
        gates.append({"label": "Position bias", "value": round(share, 3),
                      "pass": 0.45 <= share <= 0.55})
    overall = "RELIABLE" if gates and all(g["pass"] for g in gates) else \
              "UNVERIFIED" if not gates else "UNRELIABLE"
    return {"gates": gates, "overall": overall}


def verify_html_script_safety(html, label="HTML"):
    """Fail fast when untrusted payload data prematurely closes a script block."""
    count = html.lower().count("</script>")
    if count != 1:
        raise ValueError(
            f"{label} contains {count} </script> sequences; expected exactly 1. "
            "Refusing to write a broken report. Embed data only via "
            "serialize_for_html_script()."
        )


def write_safe_html(path, html, label="HTML"):
    """Validate script safety, then write UTF-8 HTML."""
    verify_html_script_safety(html, label)
    Path(path).write_text(html, encoding="utf-8")


def serialize_for_html_script(data):
    """Serialize untrusted evaluation data safely for an HTML script element.

    `</` anywhere in the serialised string will close the <script> tag in the
    HTML parser regardless of JSON-string boundaries.  Three layers protect
    against this: (1) ensure_ascii removes non-ASCII; (2) < and > are replaced;
    (3) `</` is explicitly rewritten as a belt-and-suspenders guard.
    """
    return (json.dumps(data, ensure_ascii=True)
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029")
            .replace("</", "\\u003c/")
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("&", "\\u0026"))


def generate_html(title, runs, benchmark, previous_runs, phase, effect=None):
    """Inject data into the HTML template and return complete HTML string."""
    template_path = SCRIPT_DIR / "viewer.html"
    if not template_path.exists():
        print(f"Error: viewer.html not found at {template_path}", file=sys.stderr)
        sys.exit(1)
    template = template_path.read_text(encoding="utf-8")

    # Separate benchmark meta from runs
    clean_runs = [r for r in runs if isinstance(r, dict)]
    benchmark_meta = None

    previous = []
    if previous_runs:
        prev_map = {r["test_id"]: r for r in previous_runs}
        for run in clean_runs:
            prev = prev_map.get(run["test_id"], {})
            previous.append(prev)

    embedded = {
        "title": title,
        "phase": phase,
        "runs": clean_runs,
        "benchmark": benchmark,
        "previous": previous,
        "effect": effect,
    }
    data_json = serialize_for_html_script(embedded)
    data_literal = json.dumps(data_json)

    return template.replace("/*__EMBEDDED_DATA__*/", f"const EMBEDDED_DATA = JSON.parse({data_literal});")


def serve_html(html_str, port=8765):
    """Start a tiny HTTP server and open the browser."""
    html_bytes = html_str.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_bytes)))
                self.end_headers()
                self.wfile.write(html_bytes)
            elif self.path.startswith("/api/"):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b"{}")
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            if self.path == "/api/feedback":
                feedback_path = Path(os.environ.get("FEEDBACK_PATH", "/tmp/feedback.json"))
                try:
                    data = json.loads(body)
                    feedback_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ok"}).encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, fmt, *args):
            pass  # suppress logs

    server = HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"  Viewer: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        print("  (could not auto-open browser)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


def main():
    parser = argparse.ArgumentParser(description="Generate prompt-eval viewer HTML")
    parser.add_argument("output_dir", help="Path to evaluation output directory")
    parser.add_argument("--phase", default="stage2",
                        choices=["stage2", "stage3", "stage5", "stage6"],
                        help="Pipeline phase (default: stage2)")
    parser.add_argument("--title", default="Prompt Evaluation",
                        help="Display title for the viewer")
    parser.add_argument("--previous", default=None,
                        help="Previous output directory for diff view")
    parser.add_argument("--static", default=None,
                        help="Export static HTML to this path instead of serving")
    parser.add_argument("--port", type=int, default=8765,
                        help="HTTP server port (default: 8765)")
    parser.add_argument("--feedback-path", default=None,
                        help="Path to save feedback.json (default: output_dir/feedback.json)")

    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()

    if not output_dir.exists():
        print(f"Error: output_dir not found: {output_dir}", file=sys.stderr)
        sys.exit(1)

    # Set feedback path
    if args.feedback_path:
        os.environ["FEEDBACK_PATH"] = args.feedback_path
    else:
        os.environ["FEEDBACK_PATH"] = str(output_dir / "feedback.json")

    print(f"Prompt Eval Viewer — Phase {args.phase[-1]}")
    print(f"  Data directory: {output_dir}")

    # Phase A: test cases
    runs = load_phase_a(output_dir)
    print(f"  Phase A — Loaded {len(runs)} test cases")

    # Phase B: outputs
    if args.phase in ("stage3", "stage5", "stage6"):
        runs = apply_phase_b(runs, output_dir)
        with_output = sum(1 for r in runs if r.get("output"))
        print(f"  Phase B — {with_output}/{len(runs)} cases have outputs")

    # Phase C: scores
    if args.phase in ("stage5", "stage6"):
        runs = apply_phase_c(runs, output_dir)
        scored = sum(1 for r in runs if isinstance(r, dict) and not r.get("_meta") and r.get("scores"))
        print(f"  Phase C — {scored}/{len([r for r in runs if isinstance(r, dict) and not r.get('_meta')])} cases scored")

    # Build benchmark
    benchmark = build_benchmark(runs) if args.phase in ("stage5", "stage6") else None
    if benchmark:
        print(f"  Benchmark — {benchmark['total_cases']} cases, {benchmark['bad_count']} bad, "
              f"{benchmark['safety_failures']} safety failures")

    # Effect lane (auto-detected; absent for functional-only runs)
    effect = load_effect(output_dir)
    if effect and effect.get("stage") == "design":
        print(f"  Effect — design stage: {effect['judges']} judges, {effect['cases']} cases "
              f"(judging not run yet)")
    elif effect:
        print(f"  Effect — {effect['judges']} judges, {len(effect['case_rows'])} cases, "
              f"win rate {effect['overall_win_rate']}%, validity {effect['validity']}")

    # Phase D: previous
    previous_runs = load_previous_runs(args.previous) if args.previous else None
    if previous_runs:
        print(f"  Phase D — Loaded {len(previous_runs)} previous cases for diff")

    # Generate
    html = generate_html(args.title, runs, benchmark, previous_runs, args.phase, effect)

    if args.static:
        output_path = Path(args.static)
    else:
        output_path = output_dir / "viewer.html"

    write_safe_html(output_path, html, "viewer.html")
    print(f"  Static HTML → {output_path}")
    print("  Script safety: passed (exactly one closing </script> tag)")


    if not args.static:
        serve_html(html, args.port)


if __name__ == "__main__":
    main()
