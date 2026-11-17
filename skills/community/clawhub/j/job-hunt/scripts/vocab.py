#!/usr/bin/env python3
"""Every closed vocabulary in job-hunt, in one module.

A closed set spelled out twice is a closed set that will drift, and the drift
is silent because both copies are individually valid Python. Before this
module existed the five verdicts were hard-coded in five places across the
four mode plans, `MARKET_KEYS` was declared twice with different contents, and
the "no market table" token was `none` in one plan and `other` in two others —
three separate ways for two modules to disagree about a set the design calls
"these exact strings, everywhere".

Import from here. Do not re-declare. If a set genuinely needs to grow, it grows
in this file, and test_vocab.py is what tells you which callers you changed.
"""
from __future__ import annotations

# ── advice levels (spec D3, §10) ──────────────────────────────────────────
# Ordinal, in order. Deliberately unnumbered everywhere downstream: a number
# invites an average, and averaging "worth_applying" with "blocked" is
# arithmetic performed on words.
VERDICTS = ("strong_apply", "worth_applying", "stretch", "likely_screen_out",
            "blocked")

# A refusal is not a sixth level. "The input does not support a conclusion" is
# not a point on the scale from apply to blocked, so it is kept orthogonal —
# otherwise a run that could not read the posting sorts as a weak recommendation.
REFUSAL = "insufficient_evidence"

VERDICT_ZH = {
    "strong_apply": "强烈建议投",
    "worth_applying": "值得投",
    "stretch": "可以冲刺",
    "likely_screen_out": "大概率被筛掉",
    "blocked": "硬性阻断",
    "insufficient_evidence": "证据不足—不出结论",
}

# ── markets (spec §10) ────────────────────────────────────────────────────
MARKET_KEYS = ("cn", "nl", "de", "uk", "us")
# The ONE token for "this market has no convention table". Never "none": in
# YAML an unquoted `none` is easy to read back as a null, and the row then
# silently becomes untyped instead of explicitly out of scope.
NO_MARKET = "other"

# ── requirement rows (spec 5.2 step 6) ────────────────────────────────────
LEVELS = ("required", "preferred", "unclear")
SCREENING = ("knockout", "weighted", "nice_to_have")
MATCH = ("strong", "partial", "gap", "no_evidence")
RECENCY = ("current", "recent", "dated", "undated")
EFFORT = ("quick", "evening", "multi_day", "not_closable")

# ── top-level fit-assessment.yaml fields (spec 5.2, the schema in
#    modes/assess.md §6) ────────────────────────────────────────────────────
# `effort` above is BOTH axes: per row it prices closing that row, at the top
# level it prices closing the remaining gaps as a whole. One set, deliberately,
# because a card that priced the two on different scales would be unreadable.
#
# LEVEL_DIRECTION was spelled in no module at all for as long as the coverage
# card printed it. count_coverage.py filled the hole with `.get(..., "unclear")`
# and the zh label map filled it again with 「不明」, so an assessment that judged
# neither still shipped a card stating both as facts. A closed set has to exist
# somewhere before a script can tell "nobody assessed this" from "assessed as
# unclear" — those are different claims and only one of them is honest.
LEVEL_DIRECTION = ("step_up", "lateral", "step_down", "unclear")

# The role family's relationship to the candidate's evidenced background.  This
# is deliberately a qualitative classification, not a proxy probability: it
# tells discovery whether a full-JD match may be a default recommendation or
# should remain a user-reviewed stretch.
DOMAIN_FIT = ("same_domain", "adjacent", "cross_over", "unclear")

# The candidate's own statement about their right to work, self-reported and
# never inferred. `unknown` is IN the set on purpose: consistency.py must be
# able to read "we asked and could not establish it" without that reading as a
# downgrade, and a field the model may not write at all is a field it omits.
WORK_STATUS = ("authorized", "needs_sponsorship", "student_or_graduate",
               "temporary_route", "unknown")

# Work-authorization-style conditions read off the posting, and what the posting
# does about each. consistency.py compares a `stance` against a WORK_STATUS; a
# value outside these sets makes that comparison return None, which looks exactly
# like "the two agree".
CONDITION_TYPES = ("sponsorship", "work_authorization", "citizenship", "clearance",
                   "licence", "onsite_location", "other")
STANCE = ("requires_existing", "offers_support", "unclear")

# ── mock-interview bands (spec 5.4) ───────────────────────────────────────
# "held_under_probe" is the ceiling on purpose: a higher band would require
# knowing what this level's expectations are, and this skill does not.
BANDS = ("not_present", "asserted", "instanced", "held_under_probe")
CONTRADICTED = "contradicted"
DEFECT_TAGS = ("UNSOURCED-FACT", "OVER-CLAIM", "CONTRADICTED", "PROBE-COLLAPSE")
