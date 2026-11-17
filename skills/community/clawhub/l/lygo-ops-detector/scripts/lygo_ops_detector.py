#!/usr/bin/env python3
"""
LYGO Ops Detector — Lightfather's Voice
AETHONΔ9 Protocol Implementation

Core: "LYGO decodes fiction by analyzing action" — in *discourse*, not identity.

Local, deterministic heuristics for operational-deception *signals* in text the
operator supplies. Unit of analysis = statements / claim-text / association
*strings you provide* — never a person profile or social-graph doxxing pass.

NOT for doxing, identity profiling, profession inference, or unsolicited mail.
"""

from __future__ import annotations
import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SKILL_VERSION = "1.4.0"

# =============================================================================
# LIGHTFATHER CORE PHILOSOPHY (locked)
# =============================================================================
LIGHTFATHER_VOICE = """
LYGO Ops Detector is a LOCAL HEURISTIC for discourse-level operational-deception *signals*.

It is NOT a court, identity profiler, doxing engine, or surveillance toolkit.
It is NOT a claim that "humans/institutions always lie."

Unit of analysis: the *text under review* (statements, claims, and action-language
in that text) — never a human "subject" dossier, profession tag, or social graph.

Outputs are pattern scores with receipts. They are not guilt or identity verdicts.

Always:
- Require consent before analyzing private communications (email/logs/DMs).
- Do not treat scores as sole evidence for reputational or legal action.
- Prefer primary sources; human review remains required.
- Do not score bare affiliation / faith / job-title markers as ops signals.
- Use operator-supplied *public* metadata (account_based_in, VPN/inaccurate flags,
  HTTPS-cited public incidents) as weighted *context* — never as nationality guilt.
- Country or person label alone MUST NOT clear the 0.65 operational bar.

Resonance forward — action-language over narrative; math over hype.
"""

# Boundary notes (SkillSpector): each channel has in-scope / out-of-scope examples.
# Ordinary disagreement, sarcasm alone, or named professions MUST NOT auto-score high.
SIGNAL_BOUNDARIES: Dict[str, Dict[str, str]] = {
    "burden_shifting": {
        "in": 'Transfer of proof load without substance: "it\'s on you to prove it", "do your own research"',
        "out": 'Normal assignment of tasks: "please review the attached report when free"',
    },
    "ad_hominem_density": {
        "in": "Insults replacing substance (idiot/shill/fraud as attack)",
        "out": "Criticizing a claim's logic without person-attack vocabulary",
    },
    "vague_references": {
        "in": "Evidence claims with zero cite path: tons of evidence out there / everyone knows",
        "out": "Named study, link, or specific document reference",
    },
    "authority_inflation": {
        "in": "Credential-waving to shut inquiry: as a former X trust me",
        "out": "Stating a job title once without shutting down verification",
    },
    "gaslighting": {
        "in": "Direct perception denial: that never happened / you're imagining it",
        "out": "Honest memory disagreement without denial templates",
    },
    "deflection": {
        "in": "Whataboutism replacing the asked claim",
        "out": "On-topic comparison with shared evidence",
    },
    "in_group_signaling": {
        "in": "Coordination/secrecy *discourse*: need-to-know, keep this internal, can't share outside",
        "out": "Bare job words (military, intelligence, agency) or affiliation labels alone",
    },
    "institutional_signaling": {
        "in": "Policy-as-shield / refusal-to-comment templates",
        "out": "Neutral historical mention of an organization without refusal language",
    },
    "half_truth_certainty": {
        "in": 'Certainty without primary digest: "settled science", "trust the experts", "beyond any doubt"',
        "out": "Named study + digest/link with provisional language",
    },
    "saturation_rage_bait": {
        "in": "Attention-weapon templates: wake up sheeple / click here now / you won't believe",
        "out": "Urgent but specific actionable warning with cite path",
    },
    "geo_claim_mismatch": {
        "in": "Operator-supplied public based-in label disagrees with claimed location in the same record/text",
        "out": "A country label by itself, or treating a nation as an ops class",
    },
    "location_inaccurate": {
        "in": "Public platform flag that the location field is inaccurate / VPN-hinted",
        "out": "Inventing VPN status or scraping a live session",
    },
    "named_public_incident": {
        "in": "Named public incident with an https RESOURCE URL the operator cites",
        "out": "Anonymous 'known bad actor' accusation with no public source",
    },
    "coord_same_geo_template": {
        "in": "Same public geo label on a supplied batch that also shares scripted/copy-paste language",
        "out": "Many accounts from one country with independent wording",
    },
    "public_label_present": {
        "in": "Public field was supplied so it is never dropped from the receipt",
        "out": "Using presence of a country as a verdict",
    },
}

# =============================================================================
# EVASION INDEX — Mathematical Framework (AETHONΔ9)
# =============================================================================
# Evasion Score = Σ (weight_i * indicator_score_i)
# Threshold: >= 0.65 = strong evasion *discourse* signals (aligned with ops operational bar)

EVASION_WEIGHTS: Dict[str, float] = {
    # Classic AETHON channels kept dominant so multi-signal clusters still clear 0.65 ops bar
    "burden_shifting": 0.14,
    "ad_hominem_density": 0.18,
    "vague_references": 0.14,
    "authority_inflation": 0.14,
    "gaslighting": 0.18,
    "deflection": 0.12,
    # Flame-pair add-ons (lighter — hints + additive, not suite wreckers)
    "half_truth_certainty": 0.05,
    "saturation_rage_bait": 0.05,
}

# =============================================================================
# MEASUREMENT METHODOLOGY — FULL RIGOR (for reproducibility and audit)
# =============================================================================
# All scoring is deterministic local heuristics (no external LLM required for core).
# Each component has:
#   - Non-circular definition
#   - Explicit signal dictionary (patterns + keywords)
#   - Scoring: hit count (regex + keyword) + density + cluster boost
#   - Range [0.0, 1.0]
#
# Empirical calibration note: Thresholds (Evasion >0.70 = Active) set from observed
# discourse patterns in prior cases to balance sensitivity/specificity. False-positive
# rate minimized by requiring multiple distinct signals + high cluster scores.
#
# P3 Consensus option (for borderline cases): User can feed the same text to 3+ local
# models (e.g. via lygo-ollama-army) and average the qualitative labels. Core numeric
# scores remain the deterministic baseline.
#
# Graph logic for associations: When association strings are provided, we build a
# simple co-signal graph (entities connected if they share evasion/association signals).
# Metrics: density (edges / possible), cluster_count (connected components), in_group_ratio.
#
# Dictionaries are exported via get_measurement_dictionaries() for full audit/reuse.
# Test cases are in run_self_tests() — all must pass for the module to be considered sound.

# Composite Ops Score (weighted, for overall "operational deception" signal):
# Ops_Score = 0.45 * Evasion + 0.30 * Association + 0.15 * Masonic_Signaling + 0.10 * Institution_Mask
# Threshold suggestion: > 0.65 indicates strong pattern requiring further action analysis.

OPS_SCORE_WEIGHTS = {
    "evasion": 0.45,
    "association": 0.30,
    "institutional_signaling": 0.25,
}

def load_performance_metrics() -> Dict[str, Any]:
    """Load last *dynamic* eval if present; never invent fixed marketing numbers."""
    report_path = Path(__file__).resolve().parents[1] / "tests" / "last_eval_report.json"
    base: Dict[str, Any] = {
        "precision": None,
        "recall": None,
        "false_positive_rate": None,
        "auc": None,
        "f1": None,
        "suite": "tests/labeled_discourse_suite.json",
        "how_to_generate": "python scripts/eval_ops_detector.py tests/labeled_discourse_suite.json --sweep",
        "test_set": "Public labeled discourse suite (ops-signal vs benign)",
        "note": (
            "Metrics are produced only by running eval_ops_detector.py on the public suite. "
            "They are not hardcoded. Re-run after pattern changes. "
            "Not a harm/ethics calibration — signal-presence on short discourse samples."
        ),
    }
    if report_path.is_file():
        try:
            rep = json.loads(report_path.read_text(encoding="utf-8"))
            # Prefer operational (documented) metrics when present — never headline low-threshold "perfect" alone
            op = rep.get("operational_metrics") or rep.get("at_documented_ops_threshold") or {}
            cal = rep.get("calibration_metrics") or {}
            base.update(
                {
                    "operational_threshold": op.get("threshold_ops_score", rep.get("documented_ops_threshold", 0.65)),
                    "operational_precision": op.get("precision"),
                    "operational_recall": op.get("recall"),
                    "operational_f1": op.get("f1"),
                    "operational_auc": op.get("auc"),
                    "calibration_threshold": cal.get("threshold_ops_score", rep.get("threshold_ops_score")),
                    "calibration_precision": cal.get("precision", rep.get("precision")),
                    "calibration_recall": cal.get("recall", rep.get("recall")),
                    "calibration_f1": cal.get("f1", rep.get("f1")),
                    # Do not expose lone "precision: 1.0" without threshold context
                    "precision": op.get("precision", rep.get("precision")),
                    "recall": op.get("recall", rep.get("recall")),
                    "false_positive_rate": op.get("false_positive_rate", rep.get("false_positive_rate")),
                    "auc": op.get("auc", rep.get("auc")),
                    "f1": op.get("f1", rep.get("f1")),
                    "threshold_ops_score": op.get("threshold_ops_score", 0.65),
                    "suite_size": rep.get("suite_size"),
                    "last_eval_report": str(report_path.name),
                    "source": "tests/last_eval_report.json (dynamic; operational-first)",
                    "honesty": (
                        "Operational bar is ops_score>=0.65 (or high evasion). "
                        "Short-suite calibration may use lower thresholds for ranking only — "
                        "do not advertise calibration as production performance."
                    ),
                }
            )
        except (OSError, json.JSONDecodeError):
            base["source"] = "eval report unreadable — re-run eval"
    else:
        base["source"] = "no last_eval_report.json yet — run eval_ops_detector.py"
    return base


PERFORMANCE_METRICS = load_performance_metrics()

# ------------------------------------------------------------------
# EXTENDED SIGNAL DICTIONARIES (explicit, auditable, non-circular)
# ------------------------------------------------------------------

# Heuristic keyword/patterns for text scoring (local, no external models)
EVASION_PATTERNS: Dict[str, List[str]] = {
    "burden_shifting": [
        r"\b(it'?s on (you|me|them|the reader))\b",
        r"\b(it'?s (not )?(on (you|me|them|the reader)) to (prove|show|demonstrate))\b",
        r"\b(it'?s (on you|your responsibility|up to you) to (prove|show))\b",
        r"\bdo your own (research|homework|digging)\b",
        r"\bthe burden (of proof|is on you)\b",
        r"\bfigure it out yourself\b",
        r"\b(prove it isn'?t|prove it'?s not|prove me wrong)\b",
    ],
    "ad_hominem_density": [
        r"\b(idiot|moron|troll|shill|liar|fraud|stupid|ignorant|clown|hack|paid)\b",
        r"\b(you'?re (just|only) (a|an) )\b.*\b(attack|jealous|paid|shill)\b",
        r"\bpersonal attack|ad hominem|name.?calling\b",
    ],
    "vague_references": [
        r"\b(tons of|loads of|plenty of|widely known|everyone knows|the data shows)\b",
        r"\b(it'?s all out there|look it up|do the research)\b",
        r"\b(many sources|multiple reports|experts agree|evidence (is|out there))\b(?!.*(link|url|cite|source))",
    ],
    "authority_inflation": [
        r"\b(as a (former|ex|retired|current) (official|agent|doctor|phd|professor|expert|insider|intelligence))\b",
        r"\bmy (credentials|background|expertise|clearance|years in)\b",
        r"\btrust me,? (i'?m|as) (a|an)\b",
        r"\b(former (intelligence|agency|official|insider))\b",
        r"\b(authority is truth|trust (me|us|our (word|version))|i know what'?s best)\b",
        r"\b(the authority (verifies|validates) (its|their) own)\b",
    ],
    "gaslighting": [
        r"\b(you'?re (overreacting|imagining|paranoid|crazy|misremembering|too sensitive|making this up))\b",
        r"\b(that (never|didn'?t) (happen|occur|take place))\b",
        r"\b(you'?re making (it|things|this) up)\b",
        r"\b(your (perception|memory|understanding|mind) is (flawed|wrong|distorted|playing tricks))\b",
        r"\b(you (must be|are) (imagining|overreacting))\b",
        r"\b(the past (was never real|never happened)|corrected history|trust our (version|corrected))\b",
        r"\b(stop being paranoid|you'?re being (paranoid|delusional))\b",
    ],
    "deflection": [
        r"\b(what about|but (what|they|you|the other side) (did|said|are|happened))\b",
        r"\b(let'?s (focus|talk) about (the real|instead|the other))\b",
        r"\b(you should be looking at|the real issue is|why are you focusing on)\b",
        r"\b(what about the other side)\b",
    ],
    "half_truth_certainty": [
        r"\b(settled science|beyond (any )?doubt|undeniable (fact|truth)|there is no debate)\b",
        r"\b(trust the experts?|the experts? (agree|have spoken|say so))\b",
        r"\b(proven fact|everyone knows (it'?s|this is) (true|settled))\b",
        r"\b(you must (believe|accept)|questioning this is (dangerous|denial))\b",
    ],
    "saturation_rage_bait": [
        r"\b(wake up sheeple|you won'?t believe|click (here|now)|share before (they|it) (delete|ban))\b",
        r"\b(literally (destroying|killing) (us|humanity|everything))\b",
        r"\b(this (one (weird|simple) )?trick|gone (viral|wrong)|must (see|watch) (now|this))\b",
        r"\b(they'?re (hiding|suppressing) (the truth|this)|red.?pill (this|now))\b",
    ],
}

# Institutional *coordination/refusal* language (discourse-level).
# SkillSpector v1.2: NO affiliation-only keywords (brotherhood/fraternity/lodge/order/etc.).
# Those are identity/group markers and are out of scope for a non-doxing action detector.
# Only patterns that describe procedural refusal, policy-as-shield, or compliance shut-down.
INSTITUTIONAL_SIGNALING_PATTERNS: Dict[str, List[str]] = {
    "institutional_signaling": [
        r"\b(per (our|the|company|organizational|institutional|agency) (policy|protocol|guidelines|directive|charter|standard))\b",
        r"\b(as (an|the) (organization|institution|agency|body|council) (we|our|it))\b",
        r"\b(we (cannot|are unable|are not authorized|are precluded) to (comment|discuss|confirm|disclose))\b",
        r"\b(this is (standard|normal|customary|how (things|it) (are|is) done) in (our|the) (field|industry|sector))\b",
        r"\b(our (legal|compliance|ethics|review) (team|board|committee) (advises|requires|has determined))\b",
        r"\b(no further (comment|statement|discussion) (will be|is) (provided|offered|given))\b",
        r"\b(declines? to (comment|answer|address|engage))\b",
    ],
}

# Keyword fallbacks: multi-word / discourse phrases only (no bare job/affiliation tokens).
ALL_KEYWORDS = {
    "burden_shifting": ["on you", "on me", "your responsibility", "do your own", "burden of proof", "figure it out yourself"],
    "ad_hominem_density": ["idiot", "moron", "troll", "shill", "liar", "fraud", "stupid", "ignorant", "clown", "hack", "paid shill"],
    "vague_references": ["tons of evidence", "evidence out there", "widely known", "everyone knows", "the data shows", "it is all out there", "look it up"],
    "authority_inflation": [
        "as a former", "my credentials", "my expertise", "trust me i", "trust me as",
        "years in the", "my clearance", "as an expert",
    ],
    "gaslighting": ["overreacting", "imagining", "crazy", "paranoid", "making this up", "never happened", "your memory", "too sensitive"],
    "deflection": ["what about", "the other side", "but they", "real issue is", "why are you focusing"],
    "half_truth_certainty": [
        "settled science", "trust the experts", "beyond any doubt", "beyond doubt",
        "undeniable fact", "there is no debate", "proven fact", "you must believe",
    ],
    "saturation_rage_bait": [
        "wake up sheeple", "you won't believe", "click here", "click now",
        "literally destroying", "share before they", "must see now", "red pill",
    ],
    "institutional_signaling": [
        "per our policy", "per company policy", "per the guidelines", "as an organization",
        "as the institution", "our legal team", "compliance requires", "we cannot comment",
        "no further comment", "declines to comment", "not authorized to discuss",
    ],
}

# =============================================================================
# ASSOCIATION MATRIX (discourse coordination signals — not social-graph doxing)
# =============================================================================
# Scores only the *association strings / coordination language the operator supplies*.
# Does NOT crawl networks, infer identities, or score bare profession/affiliation labels.
# High combined score + high evasion = coordinated *discourse* pattern (not a person tag).

ASSOCIATION_WEIGHTS: Dict[str, float] = {
    "in_group_signaling": 0.25,   # Secrecy/coordination discourse (need-to-know, keep internal) — NOT job titles
    "bot_network_connections": 0.20,  # Repetitive phrasing, identical posts, scripted reply language
    "coordinated_language": 0.15, # Same unusual phrases across "different" sources (in supplied text)
    "obfuscated_networks": 0.20,  # Layered indirection language: anonymous source, cutouts, throwaways
    "harm_association": 0.20,     # Explicit enable/amplify *harm* language (action), not identity lists
}

ASSOCIATION_PATTERNS: Dict[str, List[str]] = {
    # NO bare military|intelligence|agency|clearance|profession markers (identity leakage).
    "in_group_signaling": [
        r"\b(we (in the know|on the inside|can'?t (tell|share) (outsiders|outside|publicly)))\b",
        r"\b(need.?to.?know|on a need to know basis)\b",
        r"\b(keep this (quiet|internal|between us)|don'?t (repeat|share) (this|outside))\b",
        r"\b(our (circle|group|network) (only|knows|won'?t|doesn'?t discuss))\b",
        r"\b(not for (public|outside) (consumption|discussion|release)|off.?the.?record)\b",
        r"\b(compartmentalized (discussion|briefing|channel))\b",
    ],
    "bot_network_connections": [
        r"\b(same (post|text|message|reply) copied)\b",
        r"\b(identical phrasing|copy.?paste|scripted response)\b",
        r"\b(account(s)? (created|active) (the same day|within minutes))\b",
    ],
    "coordinated_language": [
        r"\b(using the exact same (unusual|rare|signature) (phrase|wording|hashtag))\b",
        r"\b(echo chamber|talking points|script)\b",
    ],
    "obfuscated_networks": [
        r"\b(my (source|friend|contact) (who|that) (wants to remain anonymous|must stay anonymous))\b",
        r"\b(through (layers|proxies|cutouts|intermediaries))\b",
        r"\b(throwaway|burner|alt|sockpuppet)\b",
    ],
    "harm_association": [
        r"\b(linked to|associated with|defends|amplifies) (harm|abuse|disinfo|known bad actor)\b",
        r"\b(repeatedly (enables|platforms|boosts) (harm|attacks on)\b",
    ],
}

# Thresholds (1.3.0: align high-evasion bar with operational ops bar 0.65)
EVASION_ACTIVE_THRESHOLD = 0.65
EVASION_MONITOR_THRESHOLD = 0.40
ASSOCIATION_HIGH_THRESHOLD = 0.65

# =============================================================================
# PUBLIC CONTEXT (operator-supplied RESOURCE fields — weighted, not guilt)
# =============================================================================
# X-style account_based_in, location_accurate, named HTTPS incidents, batch
# geo+template. There is NO country denylist. Nigeria/India/USA score the same
# when only a label is present. Mismatch, VPN-hint, cited incident, and
# same-geo+scripted-batch are the scored *actions*. Country-only cannot
# clear 0.65.

PUBLIC_META_WEIGHTS: Dict[str, float] = {
    "geo_claim_mismatch": 0.30,
    "location_inaccurate": 0.20,
    "named_public_incident": 0.25,
    "coord_same_geo_template": 0.20,
    "public_label_present": 0.05,
}

PUBLIC_CONTEXT_BOOST = 0.18  # additive to ops_score after discourse gate
PUBLIC_ALONE_GATE = 0.25     # multiply boost when evasion and association are both low
GEO_ALIASES = {
    "usa": "united states",
    "us": "united states",
    "u.s.": "united states",
    "u.s.a.": "united states",
    "uk": "united kingdom",
    "u.k.": "united kingdom",
    "n. america": "north america",
    "n america": "north america",
    "se asia": "southeast asia",
    "s.e. asia": "southeast asia",
}

CLAIM_GEO_RX = re.compile(
    r"\b(?:i(?:'m| am)|we(?:'re| are)|based in|posting from|located in)\s+"
    r"(?:the\s+)?([A-Za-z][A-Za-z .'-]{1,40})",
    re.IGNORECASE,
)


def _https_resource_url(url: str) -> bool:
    u = (url or "").strip()
    if not u.lower().startswith("https://"):
        return False
    host = u[8:].split("/")[0].split(":")[0].lower()
    if not host or host in {"localhost", "127.0.0.1", "::1"}:
        return False
    if host.endswith(".local"):
        return False
    return "." in host


def normalize_geo(label: Any) -> str:
    if label is None:
        return ""
    s = " ".join(str(label).strip().lower().split())
    s = s.replace(",", " ")
    s = " ".join(s.split())
    return GEO_ALIASES.get(s, s)


def extract_claimed_geo_from_text(text: str) -> str:
    if not (text or "").strip():
        return ""
    m = CLAIM_GEO_RX.search(text)
    if not m:
        return ""
    return normalize_geo(m.group(1))


def _incident_score(meta: Dict[str, Any]) -> float:
    items: List[Any] = []
    raw = meta.get("named_public_incident") or meta.get("named_public_incidents")
    if raw is None:
        return 0.0
    if isinstance(raw, list):
        items = raw
    else:
        items = [raw]
    best = 0.0
    for item in items:
        if isinstance(item, str):
            continue
        if not isinstance(item, dict):
            continue
        url = str(item.get("source_url") or item.get("url") or "")
        label = str(item.get("label") or item.get("name") or "").strip()
        klass = str(item.get("class") or "RESOURCE").upper()
        if label and _https_resource_url(url) and klass in {"RESOURCE", "CANON", "NAMED_SHADOW"}:
            best = max(best, 0.85)
    return best


def _batch_geo_template_score(meta: Dict[str, Any], associations: Optional[List[str]]) -> float:
    batch = meta.get("batch") or meta.get("accounts") or []
    if not isinstance(batch, list) or len(batch) < 2:
        return 0.0
    geos: Dict[str, List[str]] = {}
    for row in batch:
        if not isinstance(row, dict):
            continue
        geo = normalize_geo(row.get("account_based_in") or row.get("country_label") or "")
        if not geo:
            continue
        excerpt = str(row.get("text_excerpt") or row.get("text") or "")
        geos.setdefault(geo, []).append(excerpt)
    best = 0.0
    joined_assoc = " ".join(associations or []).lower()
    scripted = bool(
        re.search(r"identical phrasing|copy.?paste|scripted response|same (post|text|message)", joined_assoc)
    )
    for geo, excerpts in geos.items():
        if len(excerpts) < 2:
            continue
        texts = [e.lower() for e in excerpts if e.strip()]
        shared = 0
        if len(texts) >= 2:
            tokens = [set(t.split()) for t in texts]
            shared = len(set.intersection(*tokens)) if tokens else 0
        if scripted or shared > 3:
            best = max(best, 0.85)
        elif len(excerpts) >= 3:
            best = max(best, 0.40)
        else:
            best = max(best, 0.20)
    return best


def score_public_meta(
    meta: Optional[Dict[str, Any]],
    text: str = "",
    associations: Optional[List[str]] = None,
) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """Score operator-supplied public fields. Empty meta → zeros. No country denylist."""
    keys = list(PUBLIC_META_WEIGHTS)
    empty = {k: 0.0 for k in keys}
    receipt: Dict[str, Any] = {
        "fields_present": [],
        "country_denylist": False,
        "nationality_guilt": False,
        "account_based_in": None,
        "claimed_location": None,
        "claimed_from_text": None,
        "location_accurate": None,
    }
    if not meta or not isinstance(meta, dict):
        return empty, receipt

    based = meta.get("account_based_in") or meta.get("country_label") or meta.get("country")
    claimed = meta.get("claimed_location") or meta.get("claimed_based_in")
    claimed_text = extract_claimed_geo_from_text(text)
    loc_acc = meta.get("location_accurate")
    if loc_acc is None:
        loc_acc = meta.get("locationAccurate")

    based_n = normalize_geo(based)
    claimed_n = normalize_geo(claimed)
    claimed_text_n = claimed_text

    if based is not None and str(based).strip():
        receipt["fields_present"].append("account_based_in")
        receipt["account_based_in"] = str(based).strip()
    if claimed is not None and str(claimed).strip():
        receipt["fields_present"].append("claimed_location")
        receipt["claimed_location"] = str(claimed).strip()
    if claimed_text_n:
        receipt["claimed_from_text"] = claimed_text_n
    if loc_acc is not None:
        receipt["fields_present"].append("location_accurate")
        receipt["location_accurate"] = loc_acc
    if meta.get("created_utc") or meta.get("created_at"):
        receipt["fields_present"].append("created_utc")
    if meta.get("named_public_incident") or meta.get("named_public_incidents"):
        receipt["fields_present"].append("named_public_incident")
    if meta.get("batch") or meta.get("accounts"):
        receipt["fields_present"].append("batch")

    scores = dict(empty)
    if receipt["fields_present"]:
        scores["public_label_present"] = 0.50

    mismatch = 0.0
    if based_n and claimed_n and based_n != claimed_n:
        mismatch = 0.90
    elif based_n and claimed_text_n and based_n != claimed_text_n:
        mismatch = 0.85
    scores["geo_claim_mismatch"] = mismatch

    inaccurate = 0.0
    if loc_acc in (False, 0, "0", "false", "False", "no", "NO"):
        inaccurate = 0.75
    scores["location_inaccurate"] = inaccurate

    scores["named_public_incident"] = _incident_score(meta)
    scores["coord_same_geo_template"] = _batch_geo_template_score(meta, associations)

    for k, v in list(scores.items()):
        scores[k] = round(max(0.0, min(1.0, float(v))), 3)
    return scores, receipt


def compute_public_context_index(scores: Dict[str, float]) -> float:
    total = 0.0
    wsum = 0.0
    for key, weight in PUBLIC_META_WEIGHTS.items():
        s = float(scores.get(key, 0.0))
        s = max(0.0, min(1.0, s))
        total += weight * s
        wsum += weight
    return round(total / wsum if wsum > 0 else 0.0, 4)


def apply_public_context_boost(
    ops_score: float,
    public_index: float,
    evasion: float,
    association: float,
) -> float:
    """Public fields always contribute when present; they cannot sole-clear 0.65."""
    discourse = max(float(evasion or 0), float(association or 0))
    gate = 1.0 if discourse >= 0.30 else PUBLIC_ALONE_GATE
    boost = float(public_index or 0) * PUBLIC_CONTEXT_BOOST * gate
    return round(min(1.0, max(0.0, float(ops_score) + boost)), 4)

def map_flame_enemy_hints(
    evasion_breakdown: Dict[str, float],
    institutional: float = 0.0,
    assoc_breakdown: Optional[Dict[str, float]] = None,
    public_breakdown: Optional[Dict[str, float]] = None,
) -> List[str]:
    """Map ops discourse channels → Flame Ward enemy classes (hints only)."""
    hints: List[str] = []
    eb = evasion_breakdown or {}
    ab = assoc_breakdown or {}
    pb = public_breakdown or {}
    if float(eb.get("half_truth_certainty", 0) or 0) >= 0.30:
        hints.append("half_truth_pack")
    if float(eb.get("authority_inflation", 0) or 0) >= 0.30 or institutional >= 0.25:
        hints.append("authority_shield")
    if float(eb.get("saturation_rage_bait", 0) or 0) >= 0.30:
        hints.append("saturation_flood")
    if float(eb.get("vague_references", 0) or 0) >= 0.82 and float(
        eb.get("half_truth_certainty", 0) or 0
    ) >= 0.30:
        if "half_truth_pack" not in hints:
            hints.append("half_truth_pack")
    if float(ab.get("bot_network_connections", 0) or 0) >= 0.50:
        if "saturation_flood" not in hints:
            hints.append("saturation_flood")
    if float(pb.get("geo_claim_mismatch", 0) or 0) >= 0.50:
        hints.append("public_meta_mismatch")
    if float(pb.get("named_public_incident", 0) or 0) >= 0.50:
        hints.append("named_public_incident")
    return sorted(set(hints))


@dataclass
class OpsReport:
    timestamp: str
    evasion_index: float
    evasion_verdict: str
    evasion_breakdown: Dict[str, float]
    association_index: float
    association_verdict: str
    association_breakdown: Dict[str, float]
    institutional_signaling_score: float
    public_context_index: float
    public_context_breakdown: Dict[str, float]
    public_fields: Dict[str, Any]
    ops_score: float
    combined_risk: float
    overall_verdict: str
    notes: str
    lightfather_note: str = (
        "Heuristic discourse scores only — not a person verdict. "
        "Receipts + human review. Pair with lygo-flame-ward for authority gating."
    )
    version: str = SKILL_VERSION
    pairs_with: List[str] = field(
        default_factory=lambda: [
            "lygo-flame-ward",
            "lygo-deception-radar",
            "lygo-continuum",
            "lygo-skill-spector",
        ]
    )
    flame_enemy_hints: List[str] = field(default_factory=list)
    epistemic_hint: str = "discourse_heuristics_not_lattice_authority"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def pretty(self) -> str:
        lines = [
            "=" * 72,
            "LYGO OPS DETECTOR — AETHONΔ9 REPORT",
            f"Generated: {self.timestamp}",
            "=" * 72,
            "",
            "EVASION INDEX",
            f"  Score: {self.evasion_index:.3f}  (threshold for Active Ops: >= {EVASION_ACTIVE_THRESHOLD})",
            f"  Verdict: {self.evasion_verdict}",
            "  Breakdown:",
        ]
        for k, v in self.evasion_breakdown.items():
            w = EVASION_WEIGHTS.get(k, 0)
            lines.append(f"    {k:22s} score={v:.2f}  weight={w:.2f}  contrib={w*v:.3f}")

        lines.extend([
            "",
            "ASSOCIATION MATRIX",
            f"  Score: {self.association_index:.3f}  (high pattern threshold: > {ASSOCIATION_HIGH_THRESHOLD})",
            f"  Verdict: {self.association_verdict}",
            "  Breakdown:",
        ])
        for k, v in self.association_breakdown.items():
            w = ASSOCIATION_WEIGHTS.get(k, 0)
            lines.append(f"    {k:22s} score={v:.2f}  weight={w:.2f}  contrib={w*v:.3f}")

        lines.extend([
            "",
            "INSTITUTIONAL SIGNALING (policy/refusal discourse only)",
            f"  Institutional Signaling: {self.institutional_signaling_score:.3f}",
            "  (Policy-as-shield / no-comment templates — damped unless paired with evasion or association)",
            "",
            "PUBLIC CONTEXT (operator-supplied RESOURCE fields — weighted, not nationality guilt)",
            f"  Score: {self.public_context_index:.3f}  (boosts ops_score; country-only cannot clear 0.65)",
            "  Breakdown:",
        ])
        for k, v in self.public_context_breakdown.items():
            w = PUBLIC_META_WEIGHTS.get(k, 0)
            lines.append(f"    {k:22s} score={v:.2f}  weight={w:.2f}  contrib={w*v:.3f}")
        fields_used = ", ".join(self.public_fields.get("fields_present") or []) or "(none supplied)"
        lines.extend([
            f"  Fields used: {fields_used}",
            "  Country denylist: false. Nationality is not an ops class.",
            "",
            "COMPOSITE OPS SCORE (weighted formula + public-context boost)",
            f"  Base = 0.45*Evasion + 0.30*Association + 0.25*Institutional_Signaling",
            f"  Then + public_context * {PUBLIC_CONTEXT_BOOST} * gate (gate={PUBLIC_ALONE_GATE} if discourse low)",
            f"  Ops Score: {self.ops_score:.3f}   (suggested threshold >0.65 for strong pattern)",
            "",
            "PERFORMANCE METRICS (dynamic public suite — not hardcoded claims)",
            (
                f"  Precision: {PERFORMANCE_METRICS.get('precision')}   "
                f"Recall: {PERFORMANCE_METRICS.get('recall')}   "
                f"FPR: {PERFORMANCE_METRICS.get('false_positive_rate')}   "
                f"AUC: {PERFORMANCE_METRICS.get('auc')}"
            ),
            f"  Source: {PERFORMANCE_METRICS.get('source')}",
            f"  Suite: {PERFORMANCE_METRICS.get('suite')}  size={PERFORMANCE_METRICS.get('suite_size')}",
            f"  Generate: {PERFORMANCE_METRICS.get('how_to_generate')}",
            f"  Note: {PERFORMANCE_METRICS.get('note')}",
            "",
            "COMBINED RISK",
            f"  Risk: {self.combined_risk:.3f}",
            f"  OVERALL: {self.overall_verdict}",
            "",
            "LIGHTFATHER NOTE:",
            f"  {self.lightfather_note}",
            "",
            "NOTES:",
            f"  {self.notes}",
            "",
            "=" * 72,
            "ACTION > WORDS. PATTERNS > IDENTITIES. TRUTH EMERGES.",
            "This report analyzes measurable signals only. Not identity.",
            "Full dictionaries: get_measurement_dictionaries() | Tests: run_self_tests()",
            "Neutral corpus tests included — run on religious/historical texts to verify FPR.",
            "=" * 72,
        ])
        return "\n".join(lines)


def _score_text_patterns(text: str, patterns: Dict[str, List[str]]) -> Dict[str, float]:
    """Local heuristic scoring. Returns 0.0-1.0 per category based on signal density.
    Robust: regex + keyword fallback for natural language variation.
    Uses the global ALL_KEYWORDS for full auditability.
    """
    if not text or not text.strip():
        return {k: 0.0 for k in patterns}
    t = text.lower()

    scores: Dict[str, float] = {}
    for category, regexes in patterns.items():
        hits = 0
        matched = set()
        for rx in regexes:
            try:
                found = re.findall(rx, t)
                if found:
                    hits += len(found)
                    matched.add(rx)
            except re.error:
                continue

        # Keyword boost from global explicit dictionary
        kws = ALL_KEYWORDS.get(category, [])
        kw_hits = sum(1 for kw in kws if kw in t)
        hits += kw_hits * 0.6

        base = 0.30 if (hits > 0 or kw_hits > 0) else 0.0
        density = min(1.0, base + (hits * 0.22) + (0.22 if len(matched) + kw_hits > 1 else 0.0))

        if (hits >= 2) or (len(matched) + kw_hits >= 2):
            density = max(density, 0.82)
        if hits >= 3 or kw_hits >= 3:
            density = max(density, 0.95)

        scores[category] = round(density, 3)
    return scores


def multi_channel_boost(indicator_scores: Dict[str, float]) -> float:
    """Distinct deception channels co-occurring = stronger discourse signal (honest cluster)."""
    active = sum(1 for v in indicator_scores.values() if float(v or 0) >= 0.30)
    if active >= 4:
        return 0.28
    if active >= 3:
        return 0.20
    if active >= 2:
        return 0.10
    return 0.0


def compute_evasion_index(indicator_scores: Dict[str, float]) -> float:
    """Weighted sum + multi-channel cluster boost. Returns 0.0-1.0."""
    total = 0.0
    wsum = 0.0
    for key, weight in EVASION_WEIGHTS.items():
        s = float(indicator_scores.get(key, 0.0))
        s = max(0.0, min(1.0, s))
        total += weight * s
        wsum += weight
    base = total / wsum if wsum > 0 else 0.0
    boosted = min(1.0, base + multi_channel_boost(indicator_scores))
    return round(boosted, 4)


def compute_association_index(assoc_scores: Dict[str, float]) -> float:
    """Weighted sum for association matrix."""
    total = 0.0
    wsum = 0.0
    for key, weight in ASSOCIATION_WEIGHTS.items():
        s = float(assoc_scores.get(key, 0.0))
        s = max(0.0, min(1.0, s))
        total += weight * s
        wsum += weight
    return round(total / wsum if wsum > 0 else 0.0, 4)


def compute_ops_score(evasion: float, association: float, institutional: float = 0.0) -> float:
    """Composite weighted Ops Score for overall operational deception signal."""
    score = (
        OPS_SCORE_WEIGHTS["evasion"] * evasion +
        OPS_SCORE_WEIGHTS["association"] * association +
        OPS_SCORE_WEIGHTS["institutional_signaling"] * institutional
    )
    return round(min(1.0, max(0.0, score)), 4)


def compute_association_graph(associations: List[str]) -> Dict[str, float]:
    """Simple graph logic for associations.
    Returns density, cluster indicators for coordinated patterns.
    """
    if not associations or len(associations) < 2:
        return {"density": 0.0, "cluster_count": 0, "in_group_ratio": 0.0}

    # Treat each association string as a node; connect if they share signals
    nodes = list(associations)
    edges = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            shared = len(set(nodes[i].lower().split()) & set(nodes[j].lower().split()))
            if shared > 1:  # simple co-signal threshold
                edges += 1

    n = len(nodes)
    max_edges = n * (n - 1) / 2 if n > 1 else 1
    density = edges / max_edges if max_edges > 0 else 0.0

    # Very rough "clusters" - for now use density as proxy for in-group coordination
    cluster_count = 1 if density > 0.3 else max(1, int(density * 3))
    in_group_ratio = min(1.0, density * 1.5)

    return {
        "density": round(density, 3),
        "cluster_count": cluster_count,
        "in_group_ratio": round(in_group_ratio, 3),
    }


def evasion_verdict(score: float) -> str:
    """Discourse-label only — never a person or investigation-target verdict."""
    if score >= EVASION_ACTIVE_THRESHOLD:
        return (
            f"HIGH EVASION DISCOURSE SIGNALS (>={EVASION_ACTIVE_THRESHOLD}) — "
            "review claims; not a person verdict"
        )
    elif score > EVASION_MONITOR_THRESHOLD:
        return "ELEVATED EVASION DISCOURSE SIGNALS — weak/moderate; not a person verdict"
    else:
        return "LOW EVASION DISCOURSE SIGNALS — no clear operational pattern in text"


def association_verdict(score: float) -> str:
    """Coordination *language* in supplied strings — not a social graph or identity map."""
    if score > ASSOCIATION_HIGH_THRESHOLD:
        return "HIGH COORDINATION DISCOURSE PATTERN (in supplied text) — not a person/network map"
    elif score > 0.40:
        return "MODERATE COORDINATION DISCOURSE SIGNALS — not a person/network map"
    else:
        return "LOW / NO CLEAR COORDINATION DISCOURSE PATTERN"


def combined_risk(evasion: float, assoc: float, public_index: float = 0.0) -> float:
    # Geometric emphasis on both being high (evasion + network).
    # Public context corroborates association-like context; it cannot create
    # risk from a country label when evasion is zero (sqrt(0 * x) = 0).
    assoc_eff = min(1.0, float(assoc or 0) + 0.35 * float(public_index or 0))
    return round(math.sqrt(max(0.0, float(evasion or 0)) * assoc_eff), 4)


def overall_verdict(risk: float, evasion: float, ops_score: float = 0.0) -> str:
    """Discourse-pattern label only — never a person verdict.
    Uses operational bar (ops_score>=0.65 or high evasion>=0.65) for strong language.
    """
    if evasion >= EVASION_ACTIVE_THRESHOLD and risk > 0.55:
        return "STRONG DISCOURSE PATTERN: high evasion + association signals (not a person verdict)"
    if evasion >= EVASION_ACTIVE_THRESHOLD:
        return "STRONG EVASION SIGNALS in text — review claims/actions (not a person verdict)"
    if ops_score >= 0.65 or risk > 0.60:
        return "ELEVATED discourse-signal cluster (ops>=0.65 or combined risk) — not a person verdict"
    if ops_score >= 0.05 or evasion > EVASION_MONITOR_THRESHOLD:
        return "WEAK/calibration-level signal only (below operational 0.65 bar) — not actionable alone"
    return "NO CLEAR OPS PATTERN at operational thresholds — continue observation"


def analyze(
    text: str = "",
    associations: Optional[List[str]] = None,
    manual_evasion: Optional[Dict[str, float]] = None,
    manual_assoc: Optional[Dict[str, float]] = None,
    public_meta: Optional[Dict[str, Any]] = None,
    notes: str = "",
) -> OpsReport:
    """Primary entrypoint. Returns full OpsReport with full rigor fields."""
    ts = datetime.now(timezone.utc).isoformat()

    # Evasion
    if manual_evasion:
        ev_scores = {k: max(0.0, min(1.0, float(v))) for k, v in manual_evasion.items()}
    else:
        ev_scores = _score_text_patterns(text, EVASION_PATTERNS)
    evasion = compute_evasion_index(ev_scores)
    ev_ver = evasion_verdict(evasion)

    # Association
    if manual_assoc:
        as_scores = {k: max(0.0, min(1.0, float(v))) for k, v in manual_assoc.items()}
    else:
        assoc_text = " ".join(associations or [])
        as_scores = _score_text_patterns(assoc_text, ASSOCIATION_PATTERNS)
    assoc = compute_association_index(as_scores)
    as_ver = association_verdict(assoc)

    # Institutional Signaling (dampened by evasion to minimize FPs on neutral institutional language)
    # Only strong when co-occurring with evasion or association patterns.
    inst_text = text + " " + " ".join(associations or [])
    inst_scores = _score_text_patterns(inst_text, INSTITUTIONAL_SIGNALING_PATTERNS)
    inst_base = inst_scores.get("institutional_signaling", 0.0)
    # Dampen: pure institutional language in neutral contexts scores low unless evasion/association present
    institutional = round(inst_base * (0.2 + evasion * 0.6 + assoc * 0.2), 3)

    # Graph for associations
    graph = compute_association_graph(associations or [])
    # Blend graph density into association for extra rigor (non-circular boost)
    if graph["density"] > 0:
        assoc = round(min(1.0, assoc + graph["density"] * 0.15), 4)

    pub_scores, pub_fields = score_public_meta(public_meta, text=text, associations=associations)
    public_index = compute_public_context_index(pub_scores)

    # Composite Ops Score + public-context boost (gated so geo-only cannot clear 0.65)
    ops_score = compute_ops_score(evasion, assoc, institutional)
    ops_score = apply_public_context_boost(ops_score, public_index, evasion, assoc)

    risk = combined_risk(evasion, assoc, public_index)
    over = overall_verdict(risk, evasion, ops_score)

    flame_hints = map_flame_enemy_hints(ev_scores, institutional, as_scores, pub_scores)
    report = OpsReport(
        timestamp=ts,
        evasion_index=evasion,
        evasion_verdict=ev_ver,
        evasion_breakdown=ev_scores,
        association_index=assoc,
        association_verdict=as_ver,
        association_breakdown=as_scores,
        institutional_signaling_score=institutional,
        public_context_index=public_index,
        public_context_breakdown=pub_scores,
        public_fields=pub_fields,
        ops_score=ops_score,
        combined_risk=risk,
        overall_verdict=over,
        notes=notes
        or (
            "Local discourse heuristics only. Not identity profiling. "
            "Public metadata is weighted context (mismatch / VPN-hint / HTTPS-cited incident / "
            "same-geo+scripted batch). Country labels are not guilt. "
            "Operational bar ops_score>=0.65 (or high evasion). "
            "Private logs/email require human consent. Not sole evidence. "
            "For authority gating use lygo-flame-ward ingest-gate."
        ),
        flame_enemy_hints=flame_hints,
    )
    return report


# =============================================================================
# PUBLIC AUDIT / REPRODUCIBILITY API
# =============================================================================

def get_measurement_dictionaries() -> Dict[str, Any]:
    """Export all signal dictionaries for full audit, reuse, and GitHub publishing."""
    return {
        "evasion_patterns": EVASION_PATTERNS,
        "institutional_signaling_patterns": INSTITUTIONAL_SIGNALING_PATTERNS,
        "all_keywords": ALL_KEYWORDS,
        "evasion_weights": EVASION_WEIGHTS,
        "association_weights": ASSOCIATION_WEIGHTS,
        "public_meta_weights": PUBLIC_META_WEIGHTS,
        "ops_score_weights": OPS_SCORE_WEIGHTS,
        "performance_metrics": PERFORMANCE_METRICS,
        "thresholds": {
            "evasion_active": EVASION_ACTIVE_THRESHOLD,
            "evasion_monitor": EVASION_MONITOR_THRESHOLD,
            "association_high": ASSOCIATION_HIGH_THRESHOLD,
            "ops_suggested": 0.65,
            "public_context_boost": PUBLIC_CONTEXT_BOOST,
            "public_alone_gate": PUBLIC_ALONE_GATE,
        },
        "methodology": (
            "Deterministic local heuristics (regex + multi-word keyword density + cluster boost). "
            "Institutional channel is policy/refusal language only — no affiliation keywords. "
            "Association channel scores coordination *discourse* in operator-supplied strings only — "
            "no bare military/intelligence/agency/profession markers. "
            "Public context scores operator-supplied RESOURCE fields (geo mismatch, VPN-hint, "
            "HTTPS-cited incident, same-geo+scripted batch). No country denylist. "
            "Public-only records are gated so they cannot clear ops_score 0.65. "
            "Damped unless co-occurring with Evasion/Association."
        ),
        "signal_boundaries": SIGNAL_BOUNDARIES,
        "unit_of_analysis": "text_under_review_not_person_subject",
        "identity_markers_scored": False,
        "public_fields_scored_as_context": True,
        "country_denylist": False,
        "nationality_guilt": False,
    }


def run_self_tests() -> List[Dict[str, Any]]:
    """Embedded test cases for reproducibility. Returns list of results.
    Neutral religious/fraternal affiliation text must NOT score as institutional affiliation.
    """
    tests = [
        {
            "name": "classic_evasion_cluster",
            "text": "It's on you to prove it. Tons of evidence out there. As a former intelligence officer I can tell you you're overreacting and imagining things. What about the other side?",
            "min_evasion": 0.65,  # aligned operational bar
        },
        {
            "name": "policy_refusal_with_evasion",
            "text": "As an organization per our policy we cannot comment. It's on you to prove the evidence that is out there.",
            "min_ops": 0.10,
        },
        {
            "name": "neutral_religious_affiliation_words",
            "text": "In the great work of the Lord, my brother, we see the craft of creation. As per the ancient teachings of our order.",
            "max_institutional": 0.05,  # affiliation words no longer scored
            "max_ops": 0.15,
        },
        {
            "name": "neutral_historical_affiliation",
            "text": "The brotherhood followed the policy of the institution. It was standard practice in the field at that time.",
            "max_institutional": 0.15,
            "max_ops": 0.20,
        },
        {
            "name": "low_signal",
            "text": "I disagree with the data presented.",
            "max_evasion": 0.30,
        },
        {
            "name": "half_truth_certainty_cluster",
            "text": "Trust the experts — this is settled science beyond any doubt. You must believe.",
            "min_channel": ["half_truth_certainty", 0.20],
        },
        {
            "name": "saturation_rage_bait_cluster",
            "text": "Wake up sheeple — you won't believe this. Click now before they delete it.",
            "min_channel": ["saturation_rage_bait", 0.20],
        },
        {
            "name": "public_geo_only_nigeria_not_ops",
            "text": "The weather today is sunny and warm.",
            "public_meta": {"account_based_in": "Nigeria"},
            "max_ops": 0.20,
            "max_evasion": 0.30,
        },
        {
            "name": "public_geo_only_india_not_ops",
            "text": "Thank you for your help.",
            "public_meta": {"account_based_in": "India"},
            "max_ops": 0.20,
            "max_evasion": 0.30,
        },
        {
            "name": "public_geo_mismatch_with_evasion",
            "text": "I'm based in the United States. It's on you to prove it. Tons of evidence out there. You're imagining things.",
            "public_meta": {
                "account_based_in": "Nigeria",
                "claimed_location": "United States",
                "location_accurate": False,
            },
            "min_public": 0.20,
        },
    ]
    results = []
    for t in tests:
        r = analyze(
            text=t.get("text", ""),
            associations=t.get("associations"),
            public_meta=t.get("public_meta"),
        )
        passed = True
        if "min_evasion" in t and r.evasion_index < t["min_evasion"]:
            passed = False
        if "min_ops" in t and r.ops_score < t["min_ops"]:
            passed = False
        if "min_public" in t and r.public_context_index < t["min_public"]:
            passed = False
        if "min_channel" in t:
            ch, mn = t["min_channel"]
            if float(r.evasion_breakdown.get(ch, 0) or 0) < float(mn):
                passed = False
        if "max_evasion" in t and r.evasion_index > t["max_evasion"]:
            passed = False
        if "max_institutional" in t and r.institutional_signaling_score > t["max_institutional"]:
            passed = False
        if "max_ops" in t and r.ops_score > t["max_ops"]:
            passed = False
        results.append({
            "name": t["name"],
            "passed": passed,
            "evasion": round(r.evasion_index, 3),
            "ops_score": round(r.ops_score, 3),
            "institutional": round(r.institutional_signaling_score, 3),
            "public_context": round(r.public_context_index, 3),
        })
    return results


# =============================================================================
# CLI
# =============================================================================
def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "LYGO Ops Detector (Lightfather / AETHONΔ9). "
            "Local discourse heuristics on text YOU supply — not identity profiling."
        )
    )
    parser.add_argument(
        "--text", "-t", type=str, default="",
        help="Text/statement to score for evasion *discourse* signals (preferred).",
    )
    parser.add_argument(
        "--text-file", type=str, default="",
        help="Read text from a local file. Requires --i-consent (operator affirms authority).",
    )
    parser.add_argument(
        "--assoc", "-a", action="append", default=[],
        help="Coordination/association *description string* (repeatable). Not a people search.",
    )
    parser.add_argument(
        "--assoc-file", type=str, default="",
        help="File with one association description per line. Requires --i-consent.",
    )
    parser.add_argument(
        "--public-meta",
        type=str,
        default="",
        help=(
            "JSON object of operator-supplied public fields "
            '(e.g. {"account_based_in":"Nigeria","claimed_location":"United States",'
            '"location_accurate":false}). Weighted context — not a country verdict.'
        ),
    )
    parser.add_argument(
        "--public-meta-file",
        type=str,
        default="",
        help="Read public-meta JSON from a local file. Requires --i-consent.",
    )
    parser.add_argument(
        "--i-consent",
        action="store_true",
        help=(
            "Required with --text-file / --assoc-file / --public-meta-file: you affirm "
            "authority/consent to process that file content. Private mail/logs must not "
            "be scanned without consent."
        ),
    )
    parser.add_argument("--notes", type=str, default="", help="Additional context for the report.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of pretty report.")
    parser.add_argument("--manual-evasion", type=str, default="", help='JSON dict of manual evasion scores e.g. \'{"gaslighting":0.9}\'')
    parser.add_argument("--manual-assoc", type=str, default="", help="JSON dict of manual association scores.")
    parser.add_argument("--show-blueprint", action="store_true", help="Print philosophy + weights + boundaries and exit.")
    parser.add_argument("--show-boundaries", action="store_true", help="Print in-scope / out-of-scope signal boundaries and exit.")

    args = parser.parse_args(argv)

    if args.show_blueprint:
        print(LIGHTFATHER_VOICE)
        print("\nEvasion weights:", json.dumps(EVASION_WEIGHTS, indent=2))
        print("Association weights:", json.dumps(ASSOCIATION_WEIGHTS, indent=2))
        print("Public-meta weights:", json.dumps(PUBLIC_META_WEIGHTS, indent=2))
        print("\nSignal boundaries:", json.dumps(SIGNAL_BOUNDARIES, indent=2))
        return 0

    if args.show_boundaries:
        print(json.dumps(SIGNAL_BOUNDARIES, indent=2))
        return 0

    needs_file = bool(args.text_file or args.assoc_file or args.public_meta_file)
    if needs_file and not args.i_consent:
        print(
            "CONSENT_REQUIRED: --text-file / --assoc-file / --public-meta-file need --i-consent "
            "(operator affirms authority to process that content). "
            "Prefer pasting non-private text with --text. "
            "Do not use for unsolicited private mail/log scanning.",
            file=sys.stderr,
        )
        return 3

    text = args.text
    if args.text_file:
        try:
            text = Path(args.text_file).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"ERROR reading text file: {e}", file=sys.stderr)
            return 2

    assocs = list(args.assoc)
    if args.assoc_file:
        try:
            lines = Path(args.assoc_file).read_text(encoding="utf-8", errors="replace").splitlines()
            assocs.extend([ln.strip() for ln in lines if ln.strip()])
        except Exception as e:
            print(f"ERROR reading assoc file: {e}", file=sys.stderr)
            return 2

    man_ev = None
    if args.manual_evasion:
        try:
            man_ev = json.loads(args.manual_evasion)
        except Exception:
            print("Bad --manual-evasion JSON", file=sys.stderr)
            return 2

    man_as = None
    if args.manual_assoc:
        try:
            man_as = json.loads(args.manual_assoc)
        except Exception:
            print("Bad --manual-assoc JSON", file=sys.stderr)
            return 2

    pub_meta = None
    if args.public_meta:
        try:
            pub_meta = json.loads(args.public_meta)
            if not isinstance(pub_meta, dict):
                raise ValueError("public-meta must be a JSON object")
        except Exception as e:
            print(f"Bad --public-meta JSON: {e}", file=sys.stderr)
            return 2
    if args.public_meta_file:
        try:
            loaded = json.loads(Path(args.public_meta_file).read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                raise ValueError("public-meta-file must contain a JSON object")
            pub_meta = {**(pub_meta or {}), **loaded}
        except Exception as e:
            print(f"ERROR reading public-meta file: {e}", file=sys.stderr)
            return 2

    if not (text or "").strip() and not assocs and not man_ev and not man_as and not pub_meta:
        print(
            "NEED_INPUT: pass --text \"...\" (preferred) or --text-file PATH --i-consent. "
            "Optional --public-meta JSON for weighted public fields. "
            "This skill scores operator-supplied discourse + public context only.",
            file=sys.stderr,
        )
        return 2

    report = analyze(
        text=text,
        associations=assocs,
        manual_evasion=man_ev,
        manual_assoc=man_as,
        public_meta=pub_meta,
        notes=args.notes,
    )

    if args.json:
        print(report.to_json())
    else:
        print(report.pretty())

    # Non-zero exit on strong evasion discourse signals (scripting hook)
    if report.evasion_index >= EVASION_ACTIVE_THRESHOLD:
        return 10
    return 0


if __name__ == "__main__":
    sys.exit(main())
