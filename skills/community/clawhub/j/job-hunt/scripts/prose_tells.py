#!/usr/bin/env python3
"""The things that make a CV or a letter read as machine-written.

A library, not a gate. Three gates call it so the surfaces cannot drift apart on
what counts as a tell: `lint_cv.py` (the CV, lexical checks only), `check_letter.py`
(the motivation letter) and `check_word_limits.py` (the supporting statement, per
criterion — the artifact that is actually MARKED in a structured application, since
the three CV judges are routed away from that branch by design).

## What is checked, and why these

Grounded in what recruiters actually report catching in 2026, not in taste:

* **A 2026 lexical set.** `spearheaded`, `pivotal`, `intricate`, `showcasing`,
  `delve`, `realm`, `robust` sit alongside the older `leveraged` / `synergy` /
  `results-driven`. `lint_cv.CLICHES` already held four of them; the rest were
  missing, and they are the ones currently flagged most.
* **Em-dash density.** Language models use em dashes at two to three times the
  human rate, which makes it one of the few tells that is a MEASUREMENT rather
  than an opinion. Flagged by density, never by a single use — a person
  legitimately uses one.
* **The "not just X, but Y" pivot**, and its siblings. A Washington Post analysis
  of 328,744 ChatGPT messages found it to be the model's signature turn. Rare
  enough in a 300-word letter that one occurrence is worth naming.
* **Tricolon density.** "Efficient, effective, and reliable." The rule of three
  is good writing, which is exactly why models apply it to everything; the tell
  is three of them in one short letter, not one.

## What is deliberately NOT checked

**Sentence-length uniformity.** It is the most-cited structural tell and it does
not survive calibration here: a motivation letter is 250–350 words of formal
prose whose sentences are legitimately similar in length, and the measure could
not separate the machine letter below from a human one without firing on both.
A gate that fires on correct output gets switched off, and then it protects
nothing — this repo has closed three of those this week.

**Structural checks on a CV.** A skills line reads "Python, C++, MATLAB" and a
bullet is terse by design, so tricolon and em-dash density would fire on every
correct CV. The lexical set applies to both surfaces; the structural checks are
prose-only.

**The skill's own reader-facing documents** — `shortlist.md`, `fit-assessment.md`,
the completion message. Measured 2026-09-06 across all eight of them in the
iteration-2 with_skill runs: the vocabulary check found ZERO, and every one of the
eight structural findings was a false positive on inspection. In a Chinese
shortlist the em dashes were `——` (ordinary Chinese punctuation) and the `title —
company · city · salary` separator; in a fit-assessment the "tricolons" were
enumerations of real alternatives ("MR, CT or another modality", "colleagues,
documentation or customers") and requirement text quoted from the advert. These
documents are tables and lists, not 300 words of connected persuasive prose, so
`prose_findings` does not transfer to them and must not be wired into
`check_shortlist` or `check_assessment`. What governs their prose is
`SKILL.md`, "How this skill writes to the user" — a rule set, because nothing here
can measure it.

**Anything in a language the check has not been taught.** The weak-opener list in
`lint_cv.py` carries the scar: it was English-only, so four Chinese bullets
opening 负责 produced nothing while the German `Verantwortlich` fired, and the
lint was enforcing a style rule on one alphabet. A tell that is only known in
English is reported as English-only rather than pretended to be universal.
"""
from __future__ import annotations

import re

# ── the lexical set ────────────────────────────────────────────────────────
#
# Kept separate from `lint_cv.CLICHES` (which stays the CV's own list, including
# CV-only entries like "references available on request") and merged by the
# caller, so neither file has to hold the other's rules.
AI_VOCABULARY = [
    ("spearheaded", re.compile(r"\bspearhead(s|ed|ing)?\b", re.I)),
    ("pivotal", re.compile(r"\bpivotal\b", re.I)),
    ("intricate", re.compile(r"\bintricat(e|ely|ies)\b", re.I)),
    ("showcasing", re.compile(r"\bshowcas(e|es|ed|ing)\b", re.I)),
    ("delve", re.compile(r"\bdelv(e|es|ed|ing)\b", re.I)),
    ("realm", re.compile(r"\brealm(s)?\b", re.I)),
    ("robust", re.compile(r"\brobust\b", re.I)),
    ("cutting-edge", re.compile(r"\bcutting[- ]edge\b", re.I)),
    ("seamless", re.compile(r"\bseamless(ly)?\b", re.I)),
    ("valuable asset", re.compile(r"\bvaluable asset\b", re.I)),
    ("esteemed organisation",
     re.compile(r"\besteemed (organisation|organization|company)\b", re.I)),
    ("thrive in fast-paced", re.compile(r"\bthriv(e|es|ing) in (a )?fast[- ]paced\b", re.I)),
    ("relentless drive", re.compile(r"\brelentless (drive|pursuit)\b", re.I)),
    ("dedication to excellence", re.compile(r"\bdedication to excellence\b", re.I)),
]

# ── the pivot ──────────────────────────────────────────────────────────────
#
# "not just X, but Y" and the forms that carry the same move. One occurrence in
# a 300-word letter is worth naming; the construction is vanishingly rare in the
# formal register a motivation letter is written in.
NOT_JUST_PIVOT = re.compile(
    r"\b(?:not (?:just|only|merely|simply)|isn'?t (?:just|only|merely)|"
    r"it'?s not (?:just|only)|more than (?:just|simply))\b[^.!?]{0,120}?"
    r"[—–,;-]?\s*\b(?:but|rather|it'?s|it is|it was|they'?re|they are|"
    r"they were|this is|this was|these are)\b",
    re.I)
# The tense matters. A first pass listed the present forms only, and a real
# supporting statement reading "not just an administrative exercise — it WAS a
# chance to delve into…" went unreported: the whole construction was there and
# the gate saw nothing, because a criterion answer is written about work already
# done and a letter is not.

# `——` is ONE mark in Chinese (破折号), typed as two U+2014, so a run counts once.
# check_letter collapsed it before calling; check_word_limits did not, and two
# ordinary uses in a Chinese criterion answer read as four.
_EM_DASH = re.compile(r"—{2,}|[—–]|(?<=\s)--(?=\s)")
_SENTENCE = re.compile(r"[^.!?？。！]+[.!?？。！]?")
# "A, B, and C" / "A、B 和 C" inside one sentence.
_TRICOLON = re.compile(
    r"\b[\w'-]+\s*,\s*[\w'-]+\s*,?\s+(?:and|or)\s+[\w'-]+\b", re.I)

# Thresholds, calibrated against real text rather than chosen. Both are
# DENSITIES: a single em dash and a single tricolon are ordinary writing, and
# flagging either would be the cry-wolf this file's docstring refuses.
#
# Measured 2026-09-06, per 100 words:
#
#   a hand-written letter                          0.7   (ONE sample, mine)
#   this skill's own letter, Brainlab run          1.0
#   this skill's own letter, Cedars run            1.8
#   a deliberately machine-written letter          3.2
#
# The reported figure is that models use em dashes at two to three times the
# human rate. A first pass put the line at 1.0 and fired on BOTH of the skill's
# real letters — but the human baseline here is a single sample I wrote, which is
# not enough evidence to call 1.0 machine-like. 1.5 separates the clearly heavy
# letter from ordinary use, and errs toward missing rather than toward crying
# wolf on correct output. Widen it only with more human samples, not by taste.
EM_DASH_PER_100_WORDS = 1.5
MAX_TRICOLONS = 3


# Han and kana are written without spaces, so the word pattern below read every
# run of them between two punctuation marks as ONE word: a 260-character Chinese
# letter measured 20 "words", and two ordinary 破折号 came out at 10 per 100
# against a line of 1.5. Each of those characters is counted as one unit
# instead. A character carries less than an English word, so the density this
# gives a CJK text is, if anything, LOW — the direction this file errs in. Hangul
# is not in the class: Korean puts spaces between words, and the word pattern
# already counts them as an English reader would.
_UNSPACED_CJK = re.compile("[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def _words(text: str) -> int:
    unspaced = len(_UNSPACED_CJK.findall(text))
    rest = _UNSPACED_CJK.sub(" ", text)
    return max(1, unspaced + len(re.findall(r"[^\W\d_][\w'-]*", rest, re.UNICODE)))


def vocabulary_findings(text: str, where: str) -> list:
    """One finding per distinct term, naming where it sits.

    `where` is used verbatim. A caller scanning line by line passes
    "cv.md:7" and gets that back; a caller passing a whole document passes
    "letter.md" and the line number is appended. Appending unconditionally
    produced "cv.md:7:1", a location that reads like a column and is not one.
    """
    out = []
    lines = text.splitlines()
    multiline = len(lines) > 1
    for label, pattern in AI_VOCABULARY:
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                at = f"{where}:{i}" if multiline else where
                out.append(
                    f"AI_VOCABULARY: {at}: {label!r} — among the terms "
                    f"recruiters report flagging most in 2026. Say what the "
                    f"candidate actually did instead; the word is doing no work "
                    f"the specific fact would not do better.")
                break
    return out


def prose_findings(text: str, where: str) -> list:
    """Structural tells. PROSE ONLY — see the module docstring on why a CV is
    exempt from every check in this function."""
    out = []
    words = _words(text)

    dashes = len(_EM_DASH.findall(text))
    per_100 = dashes * 100.0 / words
    if per_100 > EM_DASH_PER_100_WORDS and dashes >= 3:
        out.append(
            f"EM_DASH_DENSITY: {where}: {dashes} em dashes in {words} words "
            f"({per_100:.1f} per 100). Language models use them at two to three "
            f"times the human rate, which is why it is one of the few tells that "
            f"is a measurement. Keep one at most; a comma or a full stop does the "
            f"same work without the signature.")

    if NOT_JUST_PIVOT.search(text):
        m = NOT_JUST_PIVOT.search(text)
        out.append(
            f"NOT_JUST_PIVOT: {where}: {m.group(0)[:60]!r} — the \"not just X, "
            f"but Y\" turn is the single most recognisable construction in model "
            f"prose. State the thing you mean without the contrast.")

    tricolons = len(_TRICOLON.findall(text))
    if tricolons >= MAX_TRICOLONS:
        out.append(
            f"TRICOLON_DENSITY: {where}: {tricolons} \"A, B and C\" lists. The "
            f"rule of three is good writing, which is why models apply it to "
            f"everything — three in one short letter reads as a template. Keep "
            f"the one that carries the most weight.")
    return out
