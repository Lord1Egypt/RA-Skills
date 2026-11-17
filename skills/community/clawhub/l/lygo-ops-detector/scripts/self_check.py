#!/usr/bin/env python3
"""Self-check for LYGO Ops Detector (Lightfather / AETHONΔ9) skill pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQ_FILES = [
    ROOT / "SKILL.md",
    ROOT / "claw.json",
    ROOT / "references" / "SECURITY.md",
    ROOT / "references" / "AETHON_D9_BLUEPRINT.md",
    ROOT / "scripts" / "lygo_ops_detector.py",
    ROOT / "scripts" / "eval_ops_detector.py",
    ROOT / "tests" / "labeled_discourse_suite.json",
]

missing = [str(p.relative_to(ROOT)) for p in REQ_FILES if not p.exists()]
if missing:
    print("MISSING_FILES:")
    for m in missing:
        print(" -", m)
    sys.exit(3)

try:
    sys.path.insert(0, str(ROOT / "scripts"))
    import lygo_ops_detector as det
except Exception as e:
    print("IMPORT_FAIL:", e)
    sys.exit(2)

assert abs(sum(det.EVASION_WEIGHTS.values()) - 1.0) < 0.001, "Evasion weights must sum to 1.0"
assert abs(sum(det.ASSOCIATION_WEIGHTS.values()) - 1.0) < 0.001, "Association weights must sum to 1.0"
assert abs(sum(det.PUBLIC_META_WEIGHTS.values()) - 1.0) < 0.001, "Public-meta weights must sum to 1.0"
assert det.EVASION_ACTIVE_THRESHOLD == 0.65
assert det.ASSOCIATION_HIGH_THRESHOLD == 0.65
assert det.SKILL_VERSION == "1.4.0"
assert not hasattr(det, "COUNTRY_RISK") and not hasattr(det, "COUNTRY_DENYLIST")
assert "half_truth_certainty" in det.EVASION_WEIGHTS
assert "saturation_rage_bait" in det.EVASION_WEIGHTS

sample_text = (
    "It's on you to prove it. Tons of evidence out there. "
    "As a former intelligence officer I can tell you you're overreacting and imagining things. "
    "What about the other side? My sources confirm."
)
report = det.analyze(text=sample_text, notes="self_check smoke test")

if report.evasion_index <= 0.0:
    print("EVA_SMOKE_FAIL: evasion score zero on clear signals")
    sys.exit(4)

suite = ROOT / "tests" / "labeled_discourse_suite.json"
samples = json.loads(suite.read_text(encoding="utf-8")).get("samples") or []
if len(samples) < 10:
    print("SUITE_TOO_SMALL")
    sys.exit(5)

d0 = next(s for s in samples if s.get("label") == 1)
b0 = next(s for s in samples if s.get("label") == 0)
rd = det.analyze(d0["text"])
rb = det.analyze(b0["text"])
if rd.ops_score < rb.ops_score and rd.evasion_index <= rb.evasion_index:
    print("RANK_FAIL: deceptive sample not ranked above benign")
    sys.exit(6)

rc = det.main(["--text-file", str(suite), "--json"])
if rc != 3:
    print("CONSENT_GATE_FAIL: expected exit 3 without --i-consent, got", rc)
    sys.exit(7)

bare = det.analyze(text="I work in military intelligence at an agency.")
if bare.association_index > 0.35:
    print("AFFILIATION_LEAK: bare job words scored association", bare.association_index)
    sys.exit(8)

dicts = det.get_measurement_dictionaries()
if not dicts.get("signal_boundaries") or dicts.get("identity_markers_scored") is not False:
    print("BOUNDARIES_MISSING")
    sys.exit(9)
if dicts.get("country_denylist") is not False or dicts.get("nationality_guilt") is not False:
    print("COUNTRY_GUILT_LEAK")
    sys.exit(14)
if dicts.get("public_fields_scored_as_context") is not True:
    print("PUBLIC_CONTEXT_FLAG_MISSING")
    sys.exit(15)

geo_ng = det.analyze(text="The weather today is sunny and warm.", public_meta={"account_based_in": "Nigeria"})
geo_in = det.analyze(text="Thank you for your help.", public_meta={"account_based_in": "India"})
geo_us = det.analyze(text="Please pass the salt.", public_meta={"account_based_in": "United States"})
if geo_ng.ops_score >= 0.65 or geo_in.ops_score >= 0.65 or geo_us.ops_score >= 0.65:
    print("GEO_ONLY_TRIPS_BAR", geo_ng.ops_score, geo_in.ops_score, geo_us.ops_score)
    sys.exit(16)
if abs(geo_ng.public_context_index - geo_in.public_context_index) > 0.001:
    print("COUNTRY_LABEL_UNEQUAL", geo_ng.public_context_index, geo_in.public_context_index)
    sys.exit(17)
if geo_ng.public_context_index <= 0:
    print("PUBLIC_LABEL_DROPPED")
    sys.exit(18)

mm = det.analyze(
    text="I'm based in the United States. It's on you to prove it. Tons of evidence out there.",
    public_meta={
        "account_based_in": "Nigeria",
        "claimed_location": "United States",
        "location_accurate": False,
    },
)
if mm.public_context_index <= geo_ng.public_context_index:
    print("MISMATCH_NO_BOOST", mm.public_context_index, geo_ng.public_context_index)
    sys.exit(19)
if "public_meta_mismatch" not in mm.flame_enemy_hints:
    print("MISMATCH_HINT_FAIL", mm.flame_enemy_hints)
    sys.exit(20)

cited = det.analyze(
    text="I disagree with the data presented.",
    public_meta={
        "named_public_incident": {
            "label": "OpenAI Hugging Face agent swarm 2026-07",
            "source_url": "https://openai.com/index/hugging-face-model-evaluation-security-incident/",
            "class": "RESOURCE",
        }
    },
)
uncited = det.analyze(
    text="I disagree with the data presented.",
    public_meta={"named_public_incident": {"label": "bad guy", "class": "RESOURCE"}},
)
if cited.public_context_breakdown.get("named_public_incident", 0) < 0.5:
    print("CITED_INCIDENT_FAIL", cited.public_context_breakdown)
    sys.exit(21)
if uncited.public_context_breakdown.get("named_public_incident", 0) > 0:
    print("UNCITED_INCIDENT_SCORED", uncited.public_context_breakdown)
    sys.exit(22)

ht = det.analyze(
    text="Trust the experts — settled science beyond any doubt. Wake up sheeple — click now."
)
if ht.evasion_breakdown.get("half_truth_certainty", 0) <= 0 and ht.evasion_breakdown.get(
    "saturation_rage_bait", 0
) <= 0:
    print("V13_SIGNAL_FAIL")
    sys.exit(12)
if not ht.flame_enemy_hints:
    print("FLAME_HINTS_FAIL", ht.flame_enemy_hints)
    sys.exit(13)

import eval_ops_detector as ev

try:
    ev.resolve_write_path(str(Path.home() / "evil_out.json"))
    print("OUT_PATH_GUARD_FAIL")
    sys.exit(10)
except SystemExit:
    pass

embedded = det.run_self_tests()
failed = [x for x in embedded if not x.get("passed")]
if failed:
    print("EMBEDDED_SELF_TESTS_FAIL", failed)
    sys.exit(23)

print("OK")
print("EVASION", report.evasion_index)
print("ASSOC", report.association_index)
print("RISK", report.combined_risk)
print("VERDICT", report.overall_verdict)
print("FLAME_HINTS", ht.flame_enemy_hints)
print("LIGHTFATHER", report.lightfather_note)
print("SUITE_SAMPLES", len(samples))
print("METRICS_SOURCE", det.PERFORMANCE_METRICS.get("source"))
print("VERSION_HINT", det.SKILL_VERSION)
