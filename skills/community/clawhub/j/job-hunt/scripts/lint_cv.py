#!/usr/bin/env python3
"""Gate: the mechanically decidable half of the CV quality pass.

Nothing downstream scores voice — the ATS judge is a literal text matcher, the
recruiter judge scores readability not phrasing — so a grammatical,
keyword-complete, utterly templated CV passes all three judges and loses at the
real human recruiter, outside every loop this skill can observe. What a program
can decide goes here; dimensions 3 and 4 of the AI-uniformity check (voice,
specificity) cannot be decided by a program and stay inline in SKILL.md.

Exit 0 = clean. Exit 1 = findings. Exit 2 = no cv.md.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal

import prose_tells

GATE = "lint_cv"

# Bare "leverage" is also a financial noun. Match the generic action verb,
# not debt metrics; financial adjectives remain local exceptions, not a waiver
# for every occurrence elsewhere in the same sentence.
CLICHES = [
    ("results-driven", re.compile(r"\bresults[- ]driven\b", re.I)),
    ("proven track record", re.compile(r"\bproven track record\b", re.I)),
    ("synergy", re.compile(r"\bsynerg(y|ies|istic)\b", re.I)),
    ("leveraged", re.compile(
        r"\bleverag(?:ed|es|ing)\b(?![\s-]+(?:buyouts?|finance|loans?|lending)\b)"
        r"|\b(?:to|we|I|can|could|will|would|should)\s+leverage\b"
        r"|\bleverage\s+(?:data|technology|tools|synerg(?:y|ies)|expertise|skills|insights|resources)\b", re.I)),
    ("excellent communicator", re.compile(r"\bexcellent communicator\b", re.I)),
    ("team player", re.compile(r"\bteam player\b", re.I)),
    ("passionate about technology", re.compile(r"\bpassionate about technology\b", re.I)),
    ("references available on request",
     re.compile(r"\breferences available (up)?on request\b", re.I)),
]
# The weak-opener list in the languages this skill writes CVs in. English-only,
# four bullets opening `负责…` ("responsible for") and three opening `Führte…`
# produced NOTHING, while `Verantwortlich` ×3 did fire — because it happens to be
# pure ASCII. The lint was enforcing a style rule on one alphabet.
WEAK_OPENERS = ("responsible for", "worked on", "helped with", "assisted in",
                "was involved in",
                "verantwortlich für", "zuständig für", "mitgearbeitet an",
                "verantwoordelijk voor", "meegewerkt aan", "betrokken bij",
                "responsable de", "chargé de", "participé à",
                "responsable de la", "encargado de", "colaboré en",
                "responsabile di", "collaborato a",
                "负责", "参与", "协助", "参加了", "配合",
                "負責", "參與", "協助",
                "担当", "携わった", "参加した",
                "담당", "참여", "보조")
# ~120 characters is one rendered line at CV widths; two is the stated ceiling.
MAX_BULLET_CHARS = 240
# Two bullets sharing an opening verb is variation; three is a template.
REPEAT_VERB_THRESHOLD = 3

_BULLET_RE = re.compile(r"^\s*[-*]\s+(?P<text>.+?)\s*$")
# `[A-Za-z]` truncated at the first non-ASCII letter, so REPEATED_VERB compared
# the string "F" for every bullet opening `Führte` — three identical openers
# read as three different ones. `\w` is Unicode-aware; the `\d_` exclusion keeps
# it to letters, and the CJK branch below stops a whole Chinese clause counting
# as one enormous "word".
_WORD_RE = re.compile(r"[^\W\d_][\w'-]*", re.UNICODE)
# Two characters plus an optional aspect marker. A HEURISTIC, and the length is
# the whole of it: most Chinese and Japanese verbs are two characters, and a
# greedy {2,4} window swallowed the difference — `构建了训`, `优化了推`, `撰写了技`
# read as three different openers when the verb repeated three times.
_CJK_OPENER = re.compile(
    r"^[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]{2}[了過过着]?")

# Japanese and Korean put the verb LAST. A bullet there opens with its object
# (`データ基盤をBigQueryへ移行し…`, `Kubernetes 클러스터를 구축…`), so its first
# characters are a noun, and three bullets about the same system read as one
# verb repeated three times: `デー` opens 3 bullets, on a CV that varies its
# verbs (移行 / 削減 / 主導). Chinese is verb-first, which is what the opener
# check was built and calibrated on, so only these two are exempt. Hiragana or
# Hangul marks the language; katakana alone is a name inside another
# language's bullet. Not replaced by a sentence-final check: the endings
# inflect (した / しました / 했습니다), and an uncalibrated rule here would cry
# wolf on correct CVs.
_VERB_FINAL = re.compile(r"[\u3040-\u309f\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]")


# A heading, or the contact line. Neither is prose the candidate wrote about
# themselves, and a company legitimately called "Robust Systems" should not be
# reported as a cliche on the line that merely names it.
_NOT_PROSE = re.compile(r"^\s*(#|\||!\[|\s*$)|@|https?://")
# render_cv's entry header, `**<title>**, <org>` (education: `**<degree>**,
# <institution>`). The rule above, applied to the shape the renderer really
# writes: `**Software Engineer**, Pivotal Software` named a real employer and
# was reported as AI vocabulary. A project header is `**<name>** — <role> —
# <description>`, with no comma after the bold, and its description is prose,
# so it stays scanned.
_ENTRY_HEADER = re.compile(r"^\s*\*\*[^*]+\*\*,\s")

# Sections whose lines NAME things instead of describing the candidate's work.
# A skills line lists products (`Pivotal Cloud Foundry`, `MongoDB Realm`); a
# certification is its issuer's title (`Pivotal Certified Spring Professional`);
# a publication is a citation (`Robust Motion-Corrected MRI Reconstruction`).
# AI_VOCABULARY there exited 1, blocked check_apply, and left one "fix":
# falsifying a product name or a citation. The summary, experience and project
# lines are scanned exactly as before.
_NAME_SECTIONS = ("skills", "certifications")
# A citation is quoted whole, so no lexical or opener rule applies to it: its
# title may say "Leveraging", and three first-author papers open three bullets
# with the candidate's own surname, which REPEATED_VERB read as a verb.
_CITATION_SECTIONS = ("publications",)
# Spellings a hand-edited CV uses that render_cv's tables do not, matched like
# the tables' own labels: equal to the heading, or contained in it.
_SECTION_ALIASES = {
    "skills": ("tools", "技能", "技术栈", "技術", "역량"),
    "publications": ("papers", "论文", "著作", "논문", "発表"),
    "certifications": ("certificates", "licenses", "资格", "자격"),
}
_HEADING_LINE = re.compile(r"^\s{0,3}(?P<hashes>#{1,6})\s+(?P<title>.*?)\s*#*\s*$")


def section_labels(profile=None) -> dict:
    """{casefolded heading label: section key} for the exempt sections.

    From render_cv's own heading tables, every language, so a label the
    renderer writes is recognised whatever language the CV is in; then the
    aliases; then `meta.headings`, the profile's override for a language the
    tables do not cover.
    """
    from render_cv import HEADINGS

    keys = _NAME_SECTIONS + _CITATION_SECTIONS
    labels = {}
    for table in HEADINGS.values():
        for key in keys:
            if table.get(key):
                labels[str(table[key]).strip().casefold()] = key
    for key, words in _SECTION_ALIASES.items():
        for word in words:
            labels.setdefault(word.casefold(), key)
    override = ((profile or {}).get("meta") or {}).get("headings")
    if isinstance(override, dict):
        for key in keys:
            if isinstance(override.get(key), str) and override[key].strip():
                labels[override[key].strip().casefold()] = key
    return labels


def _section_key(title: str, labels: dict):
    text = re.sub(r"[*_`]", "", title).strip().casefold()
    if text in labels:
        return labels[text]
    for label, key in labels.items():
        # Whole words for Latin labels ("Technical Skills", not "Skillset
        # Projects" matching "skills" inside a word); substring for CJK, which
        # has no spaces to bound a word with.
        if label.isascii():
            if re.search(r"(?<![^\W_])" + re.escape(label) + r"(?![^\W_])", text):
                return key
        elif label in text:
            return key
    return None


def line_sections(text: str, labels: dict) -> list:
    """The exempt section key each line sits in, or None, one per line.

    A section runs to the next heading of the same or a higher level, so a
    `### Journal articles` under `## Publications` stays a publication.
    """
    kinds, current = [], None
    for line in text.split("\n"):
        m = _HEADING_LINE.match(line)
        if m:
            level = len(m.group("hashes"))
            if current is None or level <= current[0]:
                key = _section_key(m.group("title"), labels)
                current = (level, key) if key else None
            kinds.append(None)
        else:
            kinds.append(current[1] if current else None)
    return kinds


def _lexical_findings(text: str, name: str, kinds=None) -> list:
    """Cliches and the 2026 AI vocabulary, over the WHOLE document.

    The bullet-only scan misses the summary, and the summary is the line a
    recruiter reads first. Measured: "Results-driven professional with a proven
    track record of leveraging synergy" produced ZERO findings as a summary and
    one as a bullet -- the same three cliches, invisible in the more damaging
    place.
    """
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        kind = kinds[n - 1] if kinds else None
        if (_NOT_PROSE.search(line) or _BULLET_RE.match(line)
                or _ENTRY_HEADER.match(line) or kind in _CITATION_SECTIONS):
            continue          # bullets are covered below, with their own message
        hits = [label for label, rx in CLICHES if rx.search(line)]
        if hits:
            out.append(f"CLICHE: {name}:{n} contains "
                       f"{', '.join(repr(h) for h in hits)} — say the specific "
                       f"thing instead")
        if kind not in _NAME_SECTIONS:
            out += prose_tells.vocabulary_findings(line, f"{name}:{n}")
    return out


def findings_for(text: str, name: str = "cv.md", profile=None) -> list:
    """Every finding for one CV. `profile` (the tailored profile, optional)
    only contributes its `meta.headings` labels to section recognition."""
    kinds = line_sections(text, section_labels(profile))
    out, openers = _lexical_findings(text, name, kinds), {}
    for n, line in enumerate(text.split("\n"), 1):
        m = _BULLET_RE.match(line)
        if not m:
            continue
        kind = kinds[n - 1]
        body = m.group("text")
        citation = kind in _CITATION_SECTIONS
        hits = [] if citation else [label for label, rx in CLICHES if rx.search(body)]
        if hits:
            out.append(f"CLICHE: {name}:{n} contains {', '.join(repr(h) for h in hits)} "
                       f"— say the specific thing instead")
        # The 2026 set applies to a bullet as much as to the summary. Wiring it
        # only into the whole-document pass, which SKIPS bullets to avoid
        # double-reporting, left every bullet exempt from it.
        if kind not in _NAME_SECTIONS + _CITATION_SECTIONS:
            out += prose_tells.vocabulary_findings(body, f"{name}:{n}")
        low = body.lower()
        for opener in () if citation else WEAK_OPENERS:
            if low.startswith(opener):
                out.append(f"WEAK_OPENER: {name}:{n} opens with "
                           f"{body[:len(opener)]!r} — open with an action verb and "
                           f"the result")
                break
        if len(body) > MAX_BULLET_CHARS:
            out.append(f"LONG_BULLET: {name}:{n} is {len(body)} characters "
                       f"(limit {MAX_BULLET_CHARS} ≈ two rendered lines) — it is "
                       f"either two bullets or it is padded")
        if citation or _VERB_FINAL.search(body):
            continue
        # CJK first: a Chinese bullet has no spaces, so the Latin matcher would
        # take the whole clause and never repeat. Two to four characters is the
        # length of a verb phrase there, which is what REPEATED_VERB is about.
        cjk_first = _CJK_OPENER.match(body)
        if cjk_first:
            openers.setdefault(cjk_first.group(0), []).append(n)
            continue
        first = _WORD_RE.match(body)
        if first and len(first.group(0)) >= 4:
            openers.setdefault(first.group(0).lower(), []).append(n)
    for verb, lines in sorted(openers.items()):
        if len(lines) >= REPEAT_VERB_THRESHOLD:
            out.append(f"REPEATED_VERB: {verb!r} opens {len(lines)} bullets (lines "
                       f"{', '.join(str(x) for x in lines)}) — vary the verb; "
                       f"repetition is the first thing that reads as generated")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--cv", default=None, help="default: <workspace>/cv.md")
    args = ap.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    path = pathlib.Path(args.cv) if args.cv else ws / "cv.md"
    if not path.exists():
        journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {path}"])
        print(f"cannot run {GATE}: {path} does not exist", file=sys.stderr)
        return 2
    # Only for `meta.headings`, the section labels of a language render_cv has
    # no table for. Absent or unreadable is not a reason to stop linting: the
    # built-in labels still apply, and the profile's own gates report its state.
    profile = None
    if (ws / "tailored-profile.yaml").is_file():
        try:
            profile = journal.load_yaml(ws / "tailored-profile.yaml")
        except journal.YamlUnreadable:
            profile = None
    findings = findings_for(path.read_text(encoding="utf-8"), path.name, profile)
    for f in findings:
        print(f)
    journal.receipt(ws, GATE, {path.name: journal.sha256_file(path)},
                    "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
