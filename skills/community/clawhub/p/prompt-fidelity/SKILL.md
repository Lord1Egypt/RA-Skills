---
name: prompt-fidelity
description: Self-checks how much of a request is verifiable vs guesswork before answering it. Use when handling search, filtering, recommendation, or data-retrieval requests over any dataset (API, database, files, spreadsheet) that mix objective criteria (checkable via a query, count, or calculation) with subjective judgment (mood, style, quality, "feels like", "best"), or when the user asks how confident, reliable, or verifiable an answer is. Decomposes the request into constraints, computes a fidelity score, and reports which parts of the answer are verified vs inferred.
---

# Prompt Fidelity Self-Check

Prompt fidelity measures what fraction of a request's information content can
be **verified** against a deterministic source (API query, database, file
contents, calculation) versus what must be **inferred** through LLM judgment.

```
Fidelity = verified_bits / (verified_bits + inferred_bits)
```

A score of 1.0 means every part of the answer is auditable. A score near 0
means the answer is entirely a judgment call. Reporting this score alongside
an answer tells the user exactly which claims they can trust mechanically and
which they should evaluate themselves.

This works on any dataset — a movie API, a billion-row reviews table, a
directory of files, a spreadsheet. The candidate pool is whatever set of
rows/items the request selects from.

## When to run this check

- The request filters or ranks items by a mix of objective and subjective
  criteria ("Python repos updated this year that are well-designed").
- The user asks how confident or verifiable your answer is.
- You are about to present results where some criteria were actually checked
  and others were your own judgment — the user deserves to know which is which.

## Workflow

### Step 1 — Decompose the request into atomic constraints

Break the request into individual constraints. Rules:

- Each constraint is one independent requirement. Bits are summed across
  constraints, which assumes they filter independently — if two constraints
  heavily overlap ("reviews of Heat" and "reviews mentioning De Niro"),
  merge them into one constraint instead of double-counting. For verified
  constraints the independence assumption can be removed entirely with one
  measured joint count (Step 3).
- A range counts as ONE constraint, not two. "From the 90s" is a single
  constraint ("Released 1990–1999"), not separate "after 1990" and
  "before 1999" constraints.
- A constraint on an aggregate or join ("movies whose reviews average 4+
  stars") is a single constraint on the entities being returned; it is
  verified if the engine computes the aggregate, inferred if you would have
  to judge it.
- Ignore filler that carries no selectivity ("some good", "please find me").

### Step 2 — Classify each constraint

- **verified**: You can check it in the current context with a deterministic
  tool — an API parameter, a SQL/search filter, reading a file, running code,
  or arithmetic. The test is: *could a script confirm each result satisfies
  this, with no model judgment involved?*
- **inferred**: Requires subjective judgment — mood, tone, themes, style,
  quality, comparative feel ("like a Coen Brothers film"), suitability
  ("good for a first date"), pacing, emotional arc.

Classification depends on the tools actually available right now. "Rated
above 7.0" is verified if you can query a ratings API, inferred if you
cannot. When in doubt, classify as inferred — overclaiming verification is
worse than underclaiming it.

**Noisy proxies get split in two.** "Verified" means the *query* is
mechanically checkable — not that the query faithfully captures the user's
intent. If the queryable field is a rough proxy (crowd-sourced tags,
full-text `LIKE '%sincere%'`, a keyword search for a concept), record the
query itself as a verified constraint AND the remaining semantic gap as an
inferred one. Example: "melancholy movies" via a `melancholy` tag becomes
verified "has the 'melancholy' keyword tag" plus inferred "tag actually
reflects a melancholy tone".

### Step 3 — Measure survival rates; estimate only as a fallback

Each constraint needs a survival rate: the fraction of the candidate pool
that satisfies it, in (0, 1). Information content is `-log2(survival_rate)`.

**Measure whenever the pool is queryable — using the cheapest mechanism the
system offers.** System-derived rates make the constraint *weights*
verified too, removing the score's largest source of noise. Record how
each rate was obtained in `rate_source`:

- `"measured"` — an exact or system-returned count against the actual data
- `"approximated"` — system-derived but inexact: planner statistics,
  sampled counts, metadata that may be stale
- `"estimated"` — your own guess

Bits are logarithmic, so order-of-magnitude accuracy is enough — a 2× error
in a rate shifts the result by only one bit. That means you should never
run an expensive exact count to get a number you only need roughly. Defer
to the target system's best practices, preferring free or cheap sources
first:

- **Counts the system returns anyway** (→ `measured`): an API's
  `total_results`, a search engine's hit count, a paginated response's
  total field.
- **Catalog and optimizer statistics** (→ `approximated`): planner row
  estimates (`EXPLAIN` output, `pg_class.reltuples`, `information_schema`
  row counts), warehouse table metadata — no scan at all.
- **Approximate or sampled counts** (→ `approximated`): `TABLESAMPLE`,
  approximate-count functions, a count over a bounded sample extrapolated
  up.
- **Exact counts** (→ `measured`) only when they're known to be cheap:
  small tables, index-only predicates, local files (`grep -c`,
  `ls | wc -l`), an in-memory dataframe.

Never fire unbounded `COUNT(*)` scans (or worse, one per constraint) at a
large shared or production system — a fidelity self-check must not become
the most expensive query of the day. If no cheap measurement path exists,
that's what `"estimated"` is for. Label honestly: a rate from possibly
stale statistics marked `"measured"` overclaims, which is exactly what
this skill exists to prevent.

**Estimate only when you can't measure or approximate**, and mark those
`"rate_source": "estimated"`. Rough calibration (anchors, not data — real
distributions skew; e.g. most catalogs are heavily weighted toward recent
years, so "last two years" may be far more common than a uniform spread
would suggest):

| Selectivity | Survival rate | Bits |
|---|---|---|
| Near-unique (exact ID, specific person's items) | 1/pool_size–0.01 | up to log2(pool) |
| Very selective (exact year, rare property) | ~0.01 | ~6.6 |
| Moderately selective (a category, a decade, a language) | 0.05–0.15 | 2.7–4.3 |
| Broad (above-average rating, common property) | 0.3–0.5 | 1–1.7 |

Also determine the **pool size** — the number of candidate rows/items
(source it the same cheap way: table statistics, an unfiltered
`total_results`, a file count). No constraint can carry more information
than it takes to identify
a single row, so per-constraint bits are capped at log2(pool_size). Pass it
to the script; without it the cap defaults to 20 bits (a one-in-a-million
pool), which undercounts near-unique selectors on large datasets.

**Correct for correlation with one more count.** Summing bits assumes the
verified constraints filter independently, which real data violates
(neighborhoods correlate with complaint types, locations with crime
types). If the datastore can cheaply measure the joint count of all
verified filters ANDed together — often the same query you run anyway to
size the survivor set — pass it as a top-level `verified_joint_count`
(alongside `pool_size`) or via `--joint-count`. The verified side of the
score then uses the exact measured joint information, `-log2(joint/pool)`,
instead of the independence approximation; per-constraint bits remain as
attribution and the report shows the adjustment. Inferred constraints
cannot be jointly counted, so they stay summed — which is why overlapping
inferred constraints must still be merged by hand.

**When the adjustment is large, compute actual correlations to find the
culprit** — don't stop at the aggregate subtraction. Two ways, same idea:

- *Pairwise counts (no data download)*: for each pair of verified
  constraints, count `A AND B` and compute the pair's correlation
  adjustment `log2((n_A × n_B) / (pool × n_AB))` — the pairwise lift
  expressed in bits, using the same sign convention as the aggregate
  adjustment: negative = overlapping (positively correlated), positive =
  anti-correlated, and the pairwise values sum to approximately the
  aggregate adjustment (the residual is higher-order interactions).
  k constraints cost k(k−1)/2 extra cheap counts.
- *Indicator correlation (data in hand)*: with rows in a dataframe or a
  judged sample, build one boolean column per constraint and run a
  correlation matrix (`df[cols].corr()` in pandas, `np.corrcoef` on the
  indicators). This is the only way to examine correlation involving
  **inferred** constraints — judge a sample, add their indicator columns,
  and inspect; label anything derived this way `approximated` at best,
  since the labels themselves are judgment.

Use the attribution to act: merge the entangled pair into one constraint,
or note in your answer which criteria are largely redundant. A large
adjustment can also flag data-quality drift (a label that only exists in
recent years correlates with every date filter) — worth a sentence to the
user when you spot it.

### Step 4 — Declare every injected filter

List every filter that narrows the pool but that the user never asked for —
whether the system applied it or you did: quality floors ("min 50 votes"),
top-N truncation before ranking, sampling, default sort order, result
limits. Record each with `"type": "injected"` (survival rate optional).

Injected filters are excluded from the fidelity score — they aren't part of
the user's request — but they MUST appear in the report and in your answer.
Silent pool-narrowing is the main way a "100% fidelity, provably correct"
claim becomes dishonest: the results may all satisfy the stated constraints
while being drawn from a pool the user never asked about. This matters most
at scale — if a verified filter leaves 10 million survivors and you rank a
sample of 30, say so.

### Step 5 — Compute the score

Write the constraints as a JSON array and run the bundled script (stdlib
only, no installs). The script lives at `scripts/compute_fidelity.py`
relative to this SKILL.md:

```bash
python3 scripts/compute_fidelity.py constraints.json
```

(The path is relative to this skill's directory — the folder containing
this SKILL.md.)

Each constraint object needs `description`, `type` ("verified", "inferred",
or "injected"), and `estimated_survival_rate` (optional for injected), plus
`rate_source` ("measured", "approximated", or "estimated" — technically
optional, but omitting it drops the provenance labels from the report and
the script warns on stderr). Pass the pool size you determined in Step 3
via `--pool-size` (or a top-level `"pool_size"` key in the JSON) — use the
actual pool's size, not a copied example value, since it sets the
per-constraint bit cap; omit it only when you truly don't know, which
falls back to the 20-bit cap. Pass the measured joint count of the
verified filters via `--joint-count` or a top-level `"verified_joint_count"`
key when you have it (a joint count of 0 is valid — it means the verified
filters are jointly unsatisfiable, and the report will say so). Add
`--json` for machine-readable output, or `--brief` for a compact plain-text
summary with no box art or decimal bits.

Always run the script — the score must be computed correctly either way —
but how much of its output to show depends on the conversation (Step 6).

### Step 6 — Answer with calibrated framing

Actually verify the verified constraints — run the queries/checks, don't just
claim them.

**Match the presentation to the conversation.** In a normal conversational
answer, do NOT paste the report block: no bar graphs, no two-decimal bit
values, no percentage more precise than a whole number. The score's job is
to shape your prose, not to appear in it as a table. Weave the split in
naturally — say which parts of the answer came straight from the data and
which are your judgment, in the same breath as the answer itself: "the
counts, dates, and locations here are straight from the city's database;
which ones sound 'furious' is my reading of the descriptions." Cite the
score qualitatively ("almost all of this is verifiable", "roughly
two-thirds of what you asked is checkable; the rest is judgment") or as a
round percent at most. Injected filters and coverage limits are still
stated plainly in every mode — that disclosure is never optional.

Show the full report block only when it's actually wanted: the user asks
for the score, the audit, or "how sure are you"; the skill was invoked
explicitly (e.g. `/prompt-fidelity`); the output is going into a file,
eval, log, or other technical artifact; or the user has shown they want
the detail. `--brief` covers the middle ground — a compact summary without
graphics or decimals.

Whatever the presentation, frame the answer by score band:

- **≥ 80%**: "These results are verifiably correct on the stated criteria."
  Every result should pass an audit of the verified constraints.
- **40–80%**: Separate the two layers explicitly: "Filtered by X and Y
  (verified); ranked by Z (my judgment)."
- **< 40%**: Say plainly that the answer is mostly judgment, present it as a
  best guess, and offer a higher-fidelity reformulation — e.g. suggest
  objective proxies for the subjective criteria ("'feels like a slow burn'
  → runtime > 120 min, drama genre, pre-2010").

Whatever the score, state any injected filters and any coverage limits
("ranked the top 30 of 2.1M matching rows") in plain language.

## Example

Request: *"Find well-regarded reviews of Heat that read as sincere"* against
a 1-billion-row reviews table with SQL access.

```json
{
  "pool_size": 1000000000,
  "verified_joint_count": 1100,
  "constraints": [
    {"description": "Review is of Heat (1995)", "type": "verified",
     "estimated_survival_rate": 1.2e-05, "rate_source": "measured"},
    {"description": "Review has 10+ helpful votes", "type": "verified",
     "estimated_survival_rate": 0.08, "rate_source": "approximated"},
    {"description": "Reads as sincere rather than ironic", "type": "inferred",
     "estimated_survival_rate": 0.3, "rate_source": "estimated"},
    {"description": "Judged only the 50 longest matching reviews",
     "type": "injected"}
  ]
}
```

The two verified rates came from the system's own numbers — the movie-ID
rate from a cheap indexed count (`measured`), the vote threshold from
planner statistics (`approximated`) — not from full-table scans; the tone
constraint is a judgment call; and the sampling step is declared instead
of hidden. The `verified_joint_count` (1,100 matching rows, from the same
query that sized the survivor set) makes the verified bits exact: the two
filters are mildly correlated, so the report shows a small negative
adjustment against the independence sum. Framing: "Movie and vote threshold are verified against the table
(rates measured, not guessed); 'sincere' is my reading; and I only judged
the 50 longest of the ~1,000 qualifying reviews."
