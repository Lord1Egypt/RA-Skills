#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Meta-analysis topic-report generation script

Input: JSON-formatted structured topic data (see generate_topic_report.example.json)
Output: Standardized Markdown or HTML topic report (11 sections)

Usage:
    # Markdown output (default by extension)
    python generate_topic_report.py input.json output.md

    # HTML output (auto-detected by extension, or explicit --format)
    python generate_topic_report.py input.json output.html
    python generate_topic_report.py input.json output.md --format html

    # No output path: default to same-name .md next to input.json
    python generate_topic_report.py input.json

Features:
- Python 3.8+ standard library only
- JSON schema validation (warn mode, does not fail)
- Missing fields print WARNING and are marked ⚠️ in the report
- Output format auto-detected (.md / .html)

Dependencies: Python 3.8+ standard library, no third-party deps.
"""

import argparse
import json
import os
import sys
from datetime import date
from html import escape
from pathlib import Path


# ---------- Assessment dimension config ----------

DIMENSIONS = [
    {
        "key": "clinical_value",
        "name": "Clinical value",
        "description": "Addresses controversial questions, affects clinical decisions, covers high-burden diseases, matters for subgroups, meets unmet needs",
    },
    {
        "key": "methodological_feasibility",
        "name": "Methodological feasibility",
        "description": "Question answerable by meta-analysis, mature effect size, identifiable heterogeneity sources, feasible special methods",
    },
    {
        "key": "data_availability",
        "name": "Data availability",
        "description": "Estimated included-study count, outcome-reporting consistency, IPD need, gray-literature need, language scope",
    },
    {
        "key": "novelty",
        "name": "Novelty",
        "description": "Innovation judgment and evidence increment after three-layer dedup search (PROSPERO/Cochrane/PubMed)",
    },
]


# ---------- Schema definition (for warn-level validation) ----------

REQUIRED_FIELDS = {
    "meta": ["researcher", "affiliation", "generated_date"],
    "topic": [
        "title_zh", "title_en", "research_field", "background",
        "pico", "meta_type", "outcomes",
    ],
    "topic.pico": ["population", "intervention", "comparator", "outcomes", "research_question"],
    "topic.meta_type": ["type", "rationale"],
    "topic.outcomes": ["primary", "secondary"],
    "assessment": ["clinical_value", "methodological_feasibility", "data_availability", "novelty"],
    "dedup": ["prospero", "cochrane", "pubmed", "novelty_judgment"],
    "presearch": ["databases", "pubmed_query", "date_range", "estimated_hits", "estimated_included", "languages"],
    "prisma": ["overall_risk"],
    "analyses": ["prespecified", "sensitivity"],
}

# Critical fields: when missing, the report prints WARNING and marks ⚠️
CRITICAL_FIELDS = [
    "topic.title_zh",
    "topic.background",
    "topic.pico.population",
    "topic.pico.research_question",
    "assessment.clinical_value.score",
    "assessment.methodological_feasibility.score",
    "assessment.data_availability.score",
    "assessment.novelty.score",
]


# ---------- Validation utilities ----------

def get_nested(d, path, default=None):
    """Get a nested value by 'a.b.c' path."""
    if not isinstance(d, dict):
        return default
    keys = path.split(".")
    cur = d
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def validate_schema(data):
    """Warn-level schema validation. Returns (warnings: list[str], critical_missing: list[str])."""
    warnings = []
    critical_missing = []

    if not isinstance(data, dict):
        warnings.append("Top level is not a JSON object")
        return warnings, critical_missing

    for section in REQUIRED_FIELDS:
        obj = get_nested(data, section)
        if obj is None:
            warnings.append(f"Missing section: {section}")
            continue
        if isinstance(obj, dict):
            for f in REQUIRED_FIELDS[section]:
                if f not in obj or obj[f] in (None, ""):
                    warnings.append(f"Missing field: {section}.{f}")

    for path in CRITICAL_FIELDS:
        v = get_nested(data, path)
        if v in (None, "", []):
            critical_missing.append(path)

    return warnings, critical_missing


def warn(message):
    """Print WARNING to stderr."""
    print(f"[WARNING] {message}", file=sys.stderr)


# ---------- Utility functions ----------

def safe_get(d, key, default="—", missing_marker=False):
    """Safe get; missing/empty returns default. If missing_marker=True and actually missing, return default with ⚠️."""
    v = d.get(key) if isinstance(d, dict) else None
    if v is None or v == "":
        if missing_marker:
            return f"{default} [!]"
        return default
    return v


def score_label(total):
    """Recommendation based on four-dim total."""
    if total >= 17:
        return "Strongly recommend proceeding — register PROSPERO and draft the protocol immediately"
    if total >= 14:
        return "Recommend proceeding — register PROSPERO after shoring up risk dimensions"
    if total >= 10:
        return "Hold — revise PICO or methodology and re-assess"
    return "Not recommended — re-pick the topic"


def run_cross_check(assessment):
    """Run cross-check rules R1-R6 (conservative style). Returns (triggers: list[dict], passed: bool)."""
    triggers = []
    if not isinstance(assessment, dict):
        return triggers, True

    def s(k):
        v = assessment.get(k, {})
        if isinstance(v, dict):
            score = v.get("score")
            return score if isinstance(score, (int, float)) else None
        return None

    cv = s("clinical_value")
    mf = s("methodological_feasibility")
    da = s("data_availability")
    nv = s("novelty")
    scores = [cv, mf, da, nv]

    # R1 all-5
    if all(x == 5 for x in scores if x is not None) and None not in scores:
        triggers.append({
            "rule": "R1 All-5",
            "action": "Forced re-review — usually means scoring was too lenient; at least one dimension should be lowered. Re-check against anchors",
        })

    # R2 high-clinical / low-novelty (tentative state): triggers at Stage 3 tentative; not after Stage 4 dedup
    if cv is not None and cv >= 4 and nv is not None and nv >= 4:
        nv_reason = (assessment.get("novelty", {}) or {}).get("reason", "")
        if not any(k in nv_reason.lower() for k in ["dedup", "search", "prospero", "increment"]):
            triggers.append({
                "rule": "R2 High-clinical / low-novelty (tentative)",
                "action": "Lower novelty to 3 (tentative); cannot raise until Stage 4 dedup confirms",
            })

    # R3 data vs feasibility contradiction
    if da is not None and da >= 4 and mf is not None and mf <= 2:
        triggers.append({
            "rule": "R3 Data vs feasibility contradiction",
            "action": "Re-review — abundant data but infeasible methodology usually means a key blocker was missed",
        })

    # R4 clinical vs data contradiction
    if cv is not None and cv >= 4 and da is not None and da <= 2:
        triggers.append({
            "rule": "R4 Clinical vs data contradiction",
            "action": "Re-review — clinically important but sparse data; consider adjusting PICO width",
        })

    # R5 any dimension ≤2
    low_dims = []
    dim_names = {
        "clinical_value": "Clinical value",
        "methodological_feasibility": "Methodological feasibility",
        "data_availability": "Data availability",
        "novelty": "Novelty",
    }
    for k, name in dim_names.items():
        v = s(k)
        if v is not None and v <= 2:
            low_dims.append(f"{name}={v}")
    if low_dims:
        triggers.append({
            "rule": "R5 Any dimension ≤2",
            "action": f"Even if total ≥14, hold; current low dimensions: {', '.join(low_dims)}",
        })

    return triggers, len(triggers) == 0


def format_pico(pico):
    """Format the PICO/PECO decomposition section."""
    if not pico:
        return "(PICO decomposition not provided) [!]"

    lines = []
    p_label = "P — Population"
    i_label = "I — Intervention"
    is_exposure = "exposure" in pico and pico.get("exposure")
    if is_exposure:
        i_label = "E — Exposure"

    lines.append(f"### {p_label}")
    lines.append("")
    lines.append(safe_get(pico, "population", missing_marker=True) if not is_exposure else safe_get(pico, "population"))
    lines.append("")
    lines.append(f"### {i_label}")
    lines.append("")
    iv = safe_get(pico, "intervention")
    if iv in ("—",):
        iv = safe_get(pico, "exposure", missing_marker=True)
    lines.append(iv)
    lines.append("")
    lines.append("### C — Comparator")
    lines.append("")
    lines.append(safe_get(pico, "comparator"))
    lines.append("")
    lines.append("### O — Outcome")
    lines.append("")
    outcomes = pico.get("outcomes") or []
    if outcomes and isinstance(outcomes, list):
        lines.append("| Type | Outcome name | Measurement tool/definition | Timepoint | Effect size |")
        lines.append("|---|---|---|---|---|")
        for o in outcomes:
            lines.append(
                f"| {safe_get(o, 'type')} | {safe_get(o, 'name')} | "
                f"{safe_get(o, 'measurement')} | {safe_get(o, 'timepoint')} | "
                f"{safe_get(o, 'effect_measure')} |"
            )
    else:
        lines.append(str(safe_get(pico, "outcomes")) + " [!]")

    lines.append("")
    lines.append("**Research-question statement**:")
    lines.append("")
    rq = safe_get(pico, "research_question", "(research-question statement not provided)")
    if rq == "(research-question statement not provided)":
        rq = rq + " [!]"
    lines.append(f"> {rq}")
    return "\n".join(lines)


def format_assessment(assessment):
    """Format the four-dim assessment table + cross-check result."""
    if not assessment:
        return "(assessment not provided) [!]"

    lines = ["| Dimension | Score (0-5) | Reason |", "|---|---|---|"]
    total = 0
    any_low = False
    for dim in DIMENSIONS:
        item = assessment.get(dim["key"], {}) if isinstance(assessment, dict) else {}
        score = item.get("score", "—") if isinstance(item, dict) else "—"
        reason = item.get("reason", "—") if isinstance(item, dict) else "—"
        if isinstance(score, (int, float)):
            total += score
            if score <= 2:
                any_low = True
        if isinstance(score, (int, float)) and reason in ("—", ""):
            reason = f"{reason} [!] (no reason given)"
        lines.append(f"| **{dim['name']}** | {score} | {reason} |")

    lines.append("")
    lines.append(f"**Total**: {total} / 20")
    lines.append("")

    # Cross-check first, because the recommendation depends on it
    triggers, passed = run_cross_check(assessment)

    # Recommendation (综合考虑 total, any_low, cross-check)
    if any_low:
        lines.append("**Recommendation**: [!] **Hold** — a dimension ≤2 triggers the R5 veto; even total ≥14 is held")
    elif not passed:
        lines.append(f"**Recommendation**: [!] **Hold** — {len(triggers)} cross-check rule(s) triggered; must re-review before proceeding")
    else:
        lines.append(f"**Recommendation**: {score_label(total)}")
    lines.append("")

    # Cross-check detail
    lines.append("**Cross-check result**:")
    lines.append("")
    if passed:
        lines.append("✅ None of the 6 cross-check rules triggered (R1-R6)")
    else:
        lines.append(f"[!] {len(triggers)} cross-check rule(s) triggered; forced re-review:")
        lines.append("")
        for t in triggers:
            lines.append(f"- **{t['rule']}**: {t['action']}")
    return "\n".join(lines)


def format_dedup(dedup):
    """Format the dedup search report."""
    if not dedup:
        return "(dedup search report not provided) [!]"

    lines = []
    # PROSPERO
    prospero = dedup.get("prospero", {}) if isinstance(dedup, dict) else {}
    lines.append("#### PROSPERO search")
    lines.append("")
    lines.append(f"- Query: `{safe_get(prospero, 'query')}`")
    lines.append(f"- Search date: {safe_get(prospero, 'search_date')}")
    lines.append(f"- Hits: {safe_get(prospero, 'hits')}")
    hits = prospero.get("key_hits", []) or []
    if hits:
        lines.append("- Key hits:")
        for h in hits[:3]:
            lines.append(f"  1. {safe_get(h, 'id')} — {safe_get(h, 'title')} — status: {safe_get(h, 'status')} — registered: {safe_get(h, 'date')}")
    lines.append("")

    # Cochrane
    cochrane = dedup.get("cochrane", {}) if isinstance(dedup, dict) else {}
    lines.append("#### Cochrane Library search")
    lines.append("")
    lines.append(f"- Query: `{safe_get(cochrane, 'query')}`")
    lines.append(f"- Search date: {safe_get(cochrane, 'search_date')}")
    lines.append(f"- Hits: {safe_get(cochrane, 'hits')}")
    hits = cochrane.get("key_hits", []) or []
    if hits:
        lines.append("- Key hits:")
        for h in hits[:3]:
            lines.append(f"  1. {safe_get(h, 'title')} — published: {safe_get(h, 'year')}")
    lines.append("")

    # PubMed
    pubmed = dedup.get("pubmed", {}) if isinstance(dedup, dict) else {}
    lines.append("#### PubMed published meta-analysis search")
    lines.append("")
    lines.append(f"- Query: `{safe_get(pubmed, 'query')}`")
    lines.append(f"- Search date: {safe_get(pubmed, 'search_date')}")
    lines.append(f"- Hits: {safe_get(pubmed, 'hits')}")
    hits = pubmed.get("key_hits", []) or []
    if hits:
        lines.append("- Key hits (by relevance):")
        for i, h in enumerate(hits[:5], 1):
            lines.append(f"  {i}. {safe_get(h, 'pmid')} — {safe_get(h, 'title')} — {safe_get(h, 'year')} — {safe_get(h, 'journal')}")
    lines.append("")

    # Non-English DB (optional)
    cn = dedup.get("chinese_db", {}) or dedup.get("non_english_db", {}) if isinstance(dedup, dict) else {}
    if cn:
        lines.append("#### Non-English database search")
        lines.append("")
        lines.append(f"- Databases: {safe_get(cn, 'databases')}")
        lines.append(f"- Query: `{safe_get(cn, 'query')}`")
        lines.append(f"- Search date: {safe_get(cn, 'search_date')}")
        lines.append(f"- Hits: {safe_get(cn, 'hits')}")
        hits = cn.get("key_hits", []) or []
        if hits:
            lines.append("- Key hits:")
            for h in hits[:3]:
                lines.append(f"  1. {safe_get(h, 'title')} — {safe_get(h, 'year')} — {safe_get(h, 'journal')}")
        lines.append("")

    # Near-duplicate judgment (optional)
    near = dedup.get("near_duplicates", []) if isinstance(dedup, dict) else []
    if near:
        lines.append("#### Near-duplicate judgment")
        lines.append("")
        lines.append("| Near type | Changed element | Counts as duplicate? | Proceed condition |")
        lines.append("|---|---|---|---|")
        for n in near:
            lines.append(
                f"| {safe_get(n, 'type')} | {safe_get(n, 'changed')} | "
                f"{safe_get(n, 'is_duplicate')} | {safe_get(n, 'condition')} |"
            )
        lines.append("")

    # Innovation judgment
    novelty = dedup.get("novelty_judgment", {}) if isinstance(dedup, dict) else {}
    lines.append("#### Innovation judgment")
    lines.append("")
    lines.append(f"- Relationship with existing work: {safe_get(novelty, 'relation')}")
    lines.append(f"- Evidence-increment type: {safe_get(novelty, 'increment_type')}")
    lines.append(f"- Increment sufficiency: {safe_get(novelty, 'increment_sufficiency')}")
    lines.append(f"- Recommendation: {safe_get(novelty, 'recommendation')}")
    return "\n".join(lines)


def format_prisma(prisma):
    """Format the PRISMA 2020 key-item preview."""
    if not prisma:
        return "(PRISMA preview not provided) [!]"

    lines = ["| Item | Content | Preview |", "|---|---|---|"]
    items = [
        ("#1", "1", "Title", "Identifiable as systematic review / meta-analysis"),
        ("#4", "4", "Objectives (PICO)", "PICO clear and operational"),
        ("#5", "5", "Eligibility", "Consistent with PICO and explicit"),
        ("#6", "6", "Information sources", "≥3 databases + gray literature"),
        ("#7", "7", "Search strategy", "Complete reproducible search string"),
        ("#8", "8", "Selection process", "Two independent reviewers + arbitration"),
        ("#10", "10", "Data items", "Standardized data-extraction form"),
        ("#11", "11", "Risk of bias", "RoB tool matched to study type"),
        ("#12", "12", "Effect measures", "Prespecified effect-size type and direction"),
        ("#13", "13", "Synthesis methods", "Prespecified synthesis, subgroups, sensitivity"),
        ("#13c", "13c", "Heterogeneity", "Prespecified I² threshold and analysis path"),
        ("#16", "16", "Study selection (flow diagram)", "Can draw a PRISMA 2020 flow diagram"),
        ("Equity", "equity", "Equity (PROGRESS-Plus)", "PROGRESS-Plus dimensions considered"),
    ]
    for _, key, name, desc in items:
        v = prisma.get(key, "—") if isinstance(prisma, dict) else "—"
        lines.append(f"| {name} | {desc} | {v} |")

    risk = prisma.get("overall_risk", "—") if isinstance(prisma, dict) else "—"
    lines.append("")
    lines.append(f"**Overall compliance risk**: {risk}")
    return "\n".join(lines)


def format_search(search):
    """Format the pre-search strategy."""
    if not search:
        return "(pre-search strategy not provided) [!]"

    lines = []
    lines.append(f"- Pre-search databases: {safe_get(search, 'databases')}")
    lines.append(f"- Pre-search query (PubMed): `{safe_get(search, 'pubmed_query')}`")
    lines.append(f"- Time range: {safe_get(search, 'date_range')}")
    lines.append(f"- Estimated total hits: {safe_get(search, 'estimated_hits')}")
    lines.append(f"- Estimated included studies: {safe_get(search, 'estimated_included')}")
    lines.append(f"- Language scope: {safe_get(search, 'languages')}")
    return "\n".join(lines)


def format_meta_type(meta_type):
    """Format the meta-analysis type and rationale."""
    if not meta_type:
        return "(meta type not provided) [!]"

    lines = []
    lines.append(f"**Type**: {safe_get(meta_type, 'type')}")
    lines.append("")
    lines.append(f"**Rationale**: {safe_get(meta_type, 'rationale')}")
    lines.append("")
    method = meta_type.get("methodological_details") or {}
    if method:
        lines.append("**Methodological details**:")
        lines.append("")
        for k, v in method.items():
            lines.append(f"- {k}: {v}")
    return "\n".join(lines)


def format_outcomes(outcomes):
    """Format primary/secondary outcomes and effect sizes."""
    if not outcomes:
        return "(outcome definitions not provided) [!]"

    lines = []
    primary = outcomes.get("primary", []) or []
    secondary = outcomes.get("secondary", []) or []
    if primary:
        lines.append("### Primary outcomes")
        lines.append("")
        lines.append("| Name | Measurement tool | Timepoint | Effect size | Model |")
        lines.append("|---|---|---|---|---|")
        for o in primary:
            lines.append(
                f"| {safe_get(o, 'name')} | {safe_get(o, 'measurement')} | "
                f"{safe_get(o, 'timepoint')} | {safe_get(o, 'effect_measure')} | "
                f"{safe_get(o, 'model')} |"
            )
        lines.append("")

    if secondary:
        lines.append("### Secondary outcomes")
        lines.append("")
        lines.append("| Name | Type | Effect size |")
        lines.append("|---|---|---|")
        for o in secondary:
            lines.append(f"| {safe_get(o, 'name')} | {safe_get(o, 'type')} | {safe_get(o, 'effect_measure')} |")
    return "\n".join(lines)


def format_subgroups(subgroups):
    """Format prespecified subgroups and sensitivity analyses."""
    if not subgroups:
        return "(not provided) [!]"

    lines = []
    prespecified = subgroups.get("prespecified", []) or []
    sensitivity = subgroups.get("sensitivity", []) or []
    if prespecified:
        lines.append("### Prespecified subgroup analyses")
        lines.append("")
        if len(prespecified) < 3:
            lines.append(f"[!] Fewer than 3 prespecified subgroups (current {len(prespecified)}); per AMSTAR-2 item 11, insufficient")
            lines.append("")
        for i, s in enumerate(prespecified, 1):
            lines.append(f"{i}. **{safe_get(s, 'variable')}** — {safe_get(s, 'rationale')}")
        lines.append("")
    else:
        lines.append("### Prespecified subgroup analyses")
        lines.append("")
        lines.append("[!] No prespecified subgroups — not compliant (PRISMA #11 + AMSTAR-2 item 11)")
        lines.append("")

    if sensitivity:
        lines.append("### Sensitivity analyses")
        lines.append("")
        for i, s in enumerate(sensitivity, 1):
            lines.append(f"{i}. {s}")
    return "\n".join(lines)


def format_risks(risks):
    """Format potential risks and mitigations."""
    if not risks:
        return "(risk analysis not provided) [!]"

    lines = ["| Risk | Level | Mitigation |", "|---|---|---|"]
    if isinstance(risks, list):
        for r in risks:
            lines.append(f"| {safe_get(r, 'risk')} | {safe_get(r, 'level')} | {safe_get(r, 'mitigation')} |")
    return "\n".join(lines)


# ---------- Markdown main render ----------

def render_report_md(data):
    """Render structured data into a Markdown report."""
    meta = data.get("meta", {}) or {}
    topic = data.get("topic", {}) or {}

    lines = []
    lines.append(f"# {safe_get(topic, 'title_zh', '(title not provided)', missing_marker=True)}")
    lines.append("")
    lines.append(f"**English Title**: {safe_get(topic, 'title_en')}")
    lines.append("")
    lines.append(f"- **Generated**: {safe_get(meta, 'generated_date', date.today().isoformat())}")
    lines.append(f"- **Researcher**: {safe_get(meta, 'researcher')}")
    lines.append(f"- **Affiliation**: {safe_get(meta, 'affiliation')}")
    lines.append(f"- **Research field**: {safe_get(topic, 'research_field')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Background
    lines.append("## 1. Background and rationale")
    lines.append("")
    bg = safe_get(topic, "background", "(background not provided)", missing_marker=True)
    lines.append(bg)
    lines.append("")

    # 2. PICO
    lines.append("## 2. PICO/PECO decomposition")
    lines.append("")
    lines.append(format_pico(topic.get("pico")))
    lines.append("")

    # 3. Meta type
    lines.append("## 3. Meta-analysis type and rationale")
    lines.append("")
    lines.append(format_meta_type(topic.get("meta_type")))
    lines.append("")

    # 4. Four-dim assessment
    lines.append("## 4. Four-dimension topic assessment")
    lines.append("")
    lines.append(format_assessment(data.get("assessment")))
    lines.append("")

    # 5. Dedup
    lines.append("## 5. Dedup search report")
    lines.append("")
    lines.append(format_dedup(data.get("dedup")))
    lines.append("")

    # 6. Pre-search
    lines.append("## 6. Pre-search strategy and estimated inclusions")
    lines.append("")
    lines.append(format_search(data.get("presearch")))
    lines.append("")

    # 7. PRISMA
    lines.append("## 7. PRISMA 2020 key-item compliance preview")
    lines.append("")
    lines.append(format_prisma(data.get("prisma")))
    lines.append("")

    # 8. Outcomes
    lines.append("## 8. Primary outcomes and effect measures")
    lines.append("")
    lines.append(format_outcomes(topic.get("outcomes")))
    lines.append("")

    # 9. Subgroups
    lines.append("## 9. Prespecified subgroup and sensitivity analyses")
    lines.append("")
    lines.append(format_subgroups(data.get("analyses")))
    lines.append("")

    # 10. Risks
    lines.append("## 10. Potential risks and mitigations")
    lines.append("")
    lines.append(format_risks(data.get("risks")))
    lines.append("")

    # 11. Next steps
    lines.append("## 11. Recommended next steps")
    lines.append("")
    next_steps = data.get("next_steps", []) or []
    if next_steps:
        for i, s in enumerate(next_steps, 1):
            lines.append(f"{i}. {s}")
    else:
        lines.append("(not provided) [!]")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This report was auto-generated by the meta-analysis-topic-selector skill. All assessment conclusions are for topic-stage reference only; final methodological decisions should follow the full protocol.*")
    return "\n".join(lines)


# ---------- HTML render ----------

def md_table_to_html(md_text):
    """Convert a single Markdown table segment to an HTML table. Returns HTML string."""
    rows = [r for r in md_text.strip().split("\n") if r.strip()]
    if len(rows) < 2:
        return f"<p>{escape(md_text)}</p>"
    headers = [c.strip() for c in rows[0].split("|") if c.strip()]
    html = ['<table class="rpt">']
    html.append("<thead><tr>")
    for h in headers:
        html.append(f"<th>{escape(h)}</th>")
    html.append("</tr></thead><tbody>")
    for row in rows[2:]:  # skip separator
        cells = [c.strip() for c in row.split("|") if c.strip()]
        html.append("<tr>")
        for c in cells:
            html.append(f"<td>{escape(c)}</td>")
        html.append("</tr>")
    html.append("</tbody></table>")
    return "\n".join(html)


def md_to_html(md):
    """Convert the Markdown report to styled HTML (lightweight; supports only the format produced by this script)."""
    lines = md.split("\n")
    html_lines = []
    in_table = False
    table_buf = []
    in_list = False
    in_blockquote = False

    def flush_table():
        nonlocal in_table, table_buf
        if table_buf:
            html_lines.append(md_table_to_html("\n".join(table_buf)))
            table_buf = []
        in_table = False

    def flush_list():
        nonlocal in_list
        if in_list:
            html_lines.append("</ul>")
        in_list = False

    def flush_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            html_lines.append("</blockquote>")
        in_blockquote = False

    for raw in lines:
        line = raw.rstrip()

        # Table row
        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                flush_list()
                flush_blockquote()
                in_table = True
                table_buf = []
            table_buf.append(line)
            continue
        else:
            if in_table:
                flush_table()

        # Empty line
        if not line.strip():
            flush_list()
            flush_blockquote()
            html_lines.append("")
            continue

        # Headings
        if line.startswith("# "):
            flush_list()
            flush_blockquote()
            html_lines.append(f"<h1>{escape(line[2:])}</h1>")
            continue
        if line.startswith("## "):
            flush_list()
            flush_blockquote()
            html_lines.append(f"<h2>{escape(line[3:])}</h2>")
            continue
        if line.startswith("### "):
            flush_list()
            flush_blockquote()
            html_lines.append(f"<h3>{escape(line[4:])}</h3>")
            continue
        if line.startswith("#### "):
            flush_list()
            flush_blockquote()
            html_lines.append(f"<h4>{escape(line[5:])}</h4>")
            continue

        # HR
        if line.strip() in ("---", "***"):
            flush_list()
            flush_blockquote()
            html_lines.append("<hr/>")
            continue

        # Blockquote
        if line.startswith("> "):
            flush_list()
            if not in_blockquote:
                html_lines.append("<blockquote>")
                in_blockquote = True
            html_lines.append(f"<p>{escape(line[2:])}</p>")
            continue
        else:
            if in_blockquote:
                flush_blockquote()

        # List item
        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{escape(line[2:])}</li>")
            continue
        elif len(line) > 2 and line[0].isdigit() and line[1] == ".":
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{escape(line[3:])}</li>")
            continue
        else:
            if in_list:
                flush_list()

        # Plain paragraph
        html_lines.append(f"<p>{escape(line)}</p>")

    flush_table()
    flush_list()
    flush_blockquote()

    body = "\n".join(html_lines)
    title = "Meta-analysis topic report"
    if "<h1>" in body:
        start = body.find("<h1>") + 4
        end = body.find("</h1>", start)
        title = body[start:end]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>{escape(title)}</title>
<style>
  body {{
    font-family: -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    max-width: 920px;
    margin: 32px auto;
    padding: 0 24px;
    color: #1f2328;
    line-height: 1.7;
    background: #ffffff;
  }}
  h1 {{ font-size: 1.6em; border-bottom: 2px solid #d0d7de; padding-bottom: 8px; }}
  h2 {{ font-size: 1.3em; border-bottom: 1px solid #d0d7de; padding-bottom: 4px; margin-top: 32px; }}
  h3 {{ font-size: 1.1em; margin-top: 24px; }}
  h4 {{ font-size: 1em; margin-top: 18px; color: #57606a; }}
  blockquote {{
    border-left: 4px solid #0969da;
    padding: 8px 16px;
    margin: 12px 0;
    background: #f6f8fa;
    color: #24292f;
  }}
  table.rpt {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 0.95em;
  }}
  table.rpt th, table.rpt td {{
    border: 1px solid #d0d7de;
    padding: 6px 10px;
    text-align: left;
    vertical-align: top;
  }}
  table.rpt th {{ background: #f6f8fa; font-weight: 600; }}
  table.rpt tr:nth-child(even) td {{ background: #fbfdff; }}
  code {{
    background: #f6f8fa;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "SF Mono", "Consolas", monospace;
    font-size: 0.92em;
  }}
  hr {{ border: none; border-top: 1px solid #d0d7de; margin: 24px 0; }}
  ul {{ padding-left: 24px; }}
  li {{ margin: 4px 0; }}
  p {{ margin: 8px 0; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def render_report_html(data):
    """Render an HTML report."""
    md = render_report_md(data)
    return md_to_html(md)


# ---------- Entry ----------

def main():
    parser = argparse.ArgumentParser(
        description="Meta-analysis topic-report generator",
        usage="python generate_topic_report.py <input.json> [output] [--format md|html]",
    )
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument("output", nargs="?", help="Output file path (defaults to same-name .md next to input)")
    parser.add_argument(
        "--format",
        choices=["md", "html"],
        help="Output format (default: by output extension; otherwise md)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Write the example JSON to the current directory (skip input)",
    )
    args = parser.parse_args()

    if args.demo:
        out = Path.cwd() / "generate_topic_report.example.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(EXAMPLE_INPUT, f, ensure_ascii=False, indent=2)
        print(f"OK: example input written to {out}")
        return

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: JSON parse failed: {e}", file=sys.stderr)
            sys.exit(1)

    # Schema validation
    warnings, critical_missing = validate_schema(data)
    if warnings:
        print(f"[INFO] Schema validation: {len(warnings)} missing/warning item(s) (warn mode, continuing)", file=sys.stderr)
        for w in warnings:
            warn(w)
    if critical_missing:
        print(f"[WARNING] {len(critical_missing)} critical field(s) missing; the report will mark them with [!]:", file=sys.stderr)
        for c in critical_missing:
            warn(f"critical field missing: {c}")

    # Decide output format and path
    if args.output:
        output_path = Path(args.output).resolve()
        if args.format:
            fmt = args.format
        else:
            ext = output_path.suffix.lower()
            fmt = "html" if ext in (".html", ".htm") else "md"
    else:
        output_path = input_path.with_suffix(".md")
        fmt = args.format or "md"

    # Render
    if fmt == "html":
        content = render_report_html(data)
    else:
        content = render_report_md(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK: {fmt} report written to {output_path}")


# ---------- Example input (also serves as the schema doc) ----------

EXAMPLE_INPUT = {
    "meta": {
        "researcher": "John Doe",
        "affiliation": "XX Medical School",
        "generated_date": "2026-06-22",
    },
    "topic": {
        "title_zh": "PD-1 Inhibitors Plus Lenvatinib Versus Lenvatinib Alone for Unresectable Hepatocellular Carcinoma: A Systematic Review and Meta-Analysis",
        "title_en": "PD-1 Inhibitors Plus Lenvatinib Versus Lenvatinib Alone for Unresectable HCC: A Systematic Review and Meta-Analysis",
        "research_field": "Hepatocellular carcinoma immunotherapy",
        "background": "Unresectable hepatocellular carcinoma (HCC) has a poor prognosis; lenvatinib monotherapy is one standard first-line option. In recent years, multiple RCTs have explored PD-1 inhibitors combined with lenvatinib, but their conclusions are inconsistent; evidence synthesis is needed to guide clinical decision-making.",
        "pico": {
            "population": "Adults (>=18 years) with histologically or radiologically confirmed unresectable HCC, BCLC stage B-C, Child-Pugh A, no prior systemic therapy; exclude active HBV/HCV, HIV, other malignancy history.",
            "intervention": "PD-1 inhibitor (pembrolizumab 200 mg q3w / nivolumab 240 mg q2w / tislelizumab 200 mg q3w) combined with lenvatinib (>=60 kg: 12 mg qd; <60 kg: 8 mg qd), treated until PD/toxicity/24 months.",
            "comparator": "Lenvatinib monotherapy (same dose), or sorafenib 400 mg bid.",
            "outcomes": [
                {"type": "Primary", "name": "OS", "measurement": "Date of death", "timepoint": ">=12 months follow-up", "effect_measure": "HR"},
                {"type": "Primary", "name": "PFS", "measurement": "RECIST 1.1", "timepoint": ">=12 months follow-up", "effect_measure": "HR"},
            ],
            "research_question": "In adults with unresectable HCC (BCLC B-C, Child-Pugh A, treatment-naive), does PD-1 inhibitor combined with lenvatinib compared with lenvatinib monotherapy improve OS and PFS?",
        },
        "meta_type": {
            "type": "Traditional pairwise meta-analysis",
            "rationale": "Intervention and comparator are both fixed two-arm comparisons with a simple evidence network; no NMA needed; all data are aggregate; no IPD needed.",
            "methodological_details": {
                "Effect size": "Time-to-event outcomes use HR + 95% CI; binary outcomes use RR + 95% CI",
                "Synthesis model": "Random-effects model (DerSimonian-Laird), due to expected high heterogeneity",
                "Heterogeneity assessment": "I2, tau2, Q test; I2 > 50% triggers subgroup analysis",
                "Publication bias": "When >=10 studies are included, Egger test + funnel plot + Trim-and-fill",
            },
        },
        "outcomes": {
            "primary": [
                {"name": "OS", "measurement": "Date of death", "timepoint": "Minimum 12 months", "effect_measure": "HR", "model": "Random effects"},
                {"name": "PFS", "measurement": "RECIST 1.1", "timepoint": "Minimum 12 months", "effect_measure": "HR", "model": "Random effects"},
            ],
            "secondary": [
                {"name": "ORR", "type": "Binary", "effect_measure": "RR"},
                {"name": "DCR", "type": "Binary", "effect_measure": "RR"},
                {"name": "SAE", "type": "Binary", "effect_measure": "RR"},
                {"name": "Grade 3-4 TRAE", "type": "Binary", "effect_measure": "RR"},
            ],
        },
    },
    "assessment": {
        "clinical_value": {"score": 5, "reason": "Directly addresses first-line treatment controversy; may change NCCN/CSCO guideline recommendations. Matches anchor 5: directly addresses a guideline-level controversy; expected to change clinical practice"},
        "methodological_feasibility": {"score": 4, "reason": "Standard methods directly applicable; note potential heterogeneity across PD-1 inhibitors. Matches anchor 4: light methodological adaptation needed, but mature toolchain"},
        "data_availability": {"score": 4, "reason": "Pre-search estimates 6-8 RCTs; outcomes mostly consistently reported. Matches anchor 4: 6-10 studies; outcomes mostly consistent"},
        "novelty": {"score": 3, "reason": "A same-topic meta-analysis was published in 2024; must clearly state the new-study increment. Matches anchor 3: prior meta-analysis <3 years old, but with a clear evidence increment (pending Stage 4 dedup confirmation)"},
    },
    "dedup": {
        "prospero": {
            "query": "PD-1 AND lenvatinib AND HCC",
            "search_date": "2026-06-22",
            "hits": 2,
            "key_hits": [
                {"id": "CRD42024567890", "title": "Immunotherapy + Lenvatinib in HCC", "status": "Ongoing", "date": "2024-09-01"},
            ],
        },
        "cochrane": {"query": "PD-1 AND lenvatinib", "search_date": "2026-06-22", "hits": 0, "key_hits": []},
        "pubmed": {
            "query": "(PD-1[Title/Abstract]) AND (lenvatinib[Title/Abstract]) AND (HCC[Title/Abstract]) AND (meta-analysis[Publication Type])",
            "search_date": "2026-06-22",
            "hits": 3,
            "key_hits": [
                {"pmid": "38512345", "title": "PD-1 + Lenvatinib in HCC: A Meta-analysis", "year": "2024", "journal": "J Hepatol"},
            ],
        },
        "non_english_db": {
            "databases": "CNKI, Wanfang, SinoMed",
            "query": "(PD-1 OR pembrolizumab OR sintilimab) AND (lenvatinib) AND (HCC OR hepatocellular carcinoma) AND ('Meta' OR 'systematic review')",
            "search_date": "2026-06-22",
            "hits": 1,
            "key_hits": [
                {"title": "PD-1 + lenvatinib for advanced HCC: a Meta-analysis", "year": "2024", "journal": "Chinese Journal of Hepatobiliary Surgery"},
            ],
        },
        "near_duplicates": [
            {"type": "Switch within-class intervention", "changed": "I: PD-1 -> PD-L1", "is_duplicate": "No", "condition": "Justify within-class substitution clinically + subgroup by PD-1/PD-L1 type"},
        ],
        "novelty_judgment": {
            "relation": "Update type",
            "increment_type": "New-study increment + new-subgroup increment",
            "increment_sufficiency": "Sufficient (>=2 new phase III RCTs added after 2024)",
            "recommendation": "Proceed",
        },
    },
    "presearch": {
        "databases": "PubMed, Embase, Cochrane CENTRAL, CNKI",
        "pubmed_query": "(PD-1 OR pembrolizumab OR nivolumab OR tislelizumab) AND lenvatinib AND (HCC OR hepatocellular carcinoma)",
        "date_range": "Inception to 2026-06",
        "estimated_hits": 280,
        "estimated_included": 7,
        "languages": "English + Chinese",
    },
    "prisma": {
        "1": "PASS",
        "4": "PASS",
        "5": "PASS",
        "6": "PASS",
        "7": "PASS",
        "8": "WARN",
        "10": "PASS",
        "11": "PASS",
        "12": "PASS",
        "13": "PASS",
        "13c": "PASS",
        "16": "PASS",
        "equity": "WARN",
        "overall_risk": "MEDIUM (two-reviewer screening and equity dimension need shoring up)",
    },
    "analyses": {
        "prespecified": [
            {"variable": "PD-1 inhibitor type", "rationale": "Different PD-1 inhibitors may differ in efficacy"},
            {"variable": "BCLC stage", "rationale": "Stage B vs stage C populations may benefit differently"},
            {"variable": "Region (Asia vs non-Asia)", "rationale": "HBV-dominant vs HCV-dominant populations may differ"},
        ],
        "sensitivity": [
            "Re-pool after excluding high-risk-of-bias studies",
            "Re-pool including only phase III RCTs",
            "Re-pool using a fixed-effect model",
        ],
    },
    "risks": [
        {"risk": "High heterogeneity across PD-1 inhibitors", "level": "Medium", "mitigation": "Subgroup by PD-1 type; pool separately if needed"},
        {"risk": "Fewer than 5 included studies", "level": "Low", "mitigation": "Extend gray-literature search; wait for new RCTs if needed"},
        {"risk": "Two-reviewer screening not guaranteed", "level": "Medium", "mitigation": "Bring in a methodologist or a second reviewer"},
    ],
    "next_steps": [
        "Finalize the search strategy and have a methodologist review it",
        "Complete PROSPERO registration (within 2 weeks)",
        "Draft the full protocol and have the team review it",
        "Execute the three-database search and two-reviewer screening",
    ],
}


if __name__ == "__main__":
    main()
