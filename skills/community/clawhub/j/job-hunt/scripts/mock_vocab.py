"""Interview-mode vocabularies — the single source of truth for what this mode alone owns.

`references/interview-shapes.md` documents these tables for the model;
`scripts/tests/test_interview_shapes_doc.py` asserts the document and this module
cannot drift apart. Nothing in the mode may invent a tag: a tag outside these sets is
a finding no one can audit, and an unauditable finding is indistinguishable from an
opinion.

Anything the whole skill shares — the defect tags, the bands, the non-band flag, the
market keys — is DEFINED IN scripts/vocab.py and only re-exported here. Two modules in
one flat scripts/ namespace exporting the same name with different contents is a
guaranteed drift, and the drift is silent: both files keep importing, both test suites
keep passing, and the two halves of the skill quietly disagree about what a market is.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vocab

# The contract's four, from the shared module. Do not extend and do not restate —
# three of them force a walk-back and the fourth routes to claims.yaml, so adding a
# fifth here would silently change what the gate demands without touching vocab.py.
DEFECT_TAGS = vocab.DEFECT_TAGS

# Pass 2 holds claims.yaml and interview-brief.md, so it is the only pass that can
# decide these three.
PROVENANCE_TAGS = ("UNSOURCED-FACT", "OVER-CLAIM", "CONTRADICTED")

# Firing any of these makes a "## Walk-back list" section mandatory (spec 5.4 gate).
# UNSOURCED-FACT is deliberately NOT here: its honest route is usually claims.yaml
# ("true, just not on my CV"), not a change to the CV.
WALKBACK_TAGS = ("PROBE-COLLAPSE", "OVER-CLAIM", "CONTRADICTED")

# Answer-shape observations. Facts about the shape of an answer, never about the
# person. Second closed set, its own column; see the plan's "Two closed vocabularies".
SHAPE_TAGS = (
    "NO-INSTANCE",
    "NO-OUTCOME",
    "VAGUE-OUTCOME",
    "NO-ACTOR",
    "PREAMBLE-HEAVY",
    "DRIFT",
    "NO-REFLECTION",
    "NO-TRADEOFF",
    "JARGON-UNGLOSSED",
    "NO-NEXT-STEP",
    "CLINICAL-DRIFT",
)

# PROBE-COLLAPSE is visible in the transcript alone, so pass 1 owns it.
TRANSCRIPT_TAGS = SHAPE_TAGS + ("PROBE-COLLAPSE",)
ALL_TAGS = DEFECT_TAGS + SHAPE_TAGS

# Unnumbered on purpose: a numbered band would be averaged, and an average of four
# observations about four different answers is a number with no referent. Defined in
# vocab.py because check_assessment (Plan 2) and this gate must agree on them.
BANDS = vocab.BANDS
NON_BAND_FLAG = vocab.CONTRADICTED

# Pass 1 bands five dimensions. The sixth dimension in the design research
# (provenance) is NOT here: pass 1 does not hold interview-brief.md or claims.yaml,
# so it cannot decide provenance. Pass 2's three tags are the provenance dimension.
DIMENSIONS = ("instance", "completeness", "ownership", "outcome", "probe")

ROUND_TYPES = ("behavioural", "technical", "design", "hr")

# A documented SUPERSET of vocab.MARKET_KEYS, and the only place in the skill that
# needs one: a mock round has to be run for a target that has no market convention
# table, and the assessment block's MARKET header must be able to say so. It is NOT
# named MARKET_KEYS — that name is vocab's, and shadowing it here is exactly the drift
# this module refuses to create.
MOCK_MARKET_KEYS = vocab.MARKET_KEYS + (vocab.NO_MARKET,)

COVERAGE_STATUS = ("evidenced", "asked_thin", "not_asked")
SHAPE_STATUS = ("rehearsed", "partial", "not_attempted", "cannot_simulate")

QUESTION_SOURCES = ("generated", "scraped", "judge-supplementary", "user-provided")
REJECT_REASONS = (
    "wrong_country",
    "stale_specific",
    "advertising",
    "needs_login",
    "answer_included",
)

# Conditional tags: firing one outside its market/family is a miscalibrated mock, not
# a finding. NO-REFLECTION is Dutch STARR (carrieretijger, [F]) — it is not a defect
# in a US loop.
MARKET_CONDITIONAL = {"NO-REFLECTION": ("nl",)}
FAMILY_CONDITIONAL = {"NO-NEXT-STEP": ("sales",), "CLINICAL-DRIFT": ("clinical",)}

# Scraped material older than this may set SHAPE only, never be quoted as a specific
# technical question. Measured need: one nowcoder result set held posts 3 days and
# 9.5 months old, and `search` has no date parameter at all.
SCRAPED_SPECIFIC_MAX_AGE_DAYS = 365
