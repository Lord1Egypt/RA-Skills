---
name: "deepresearch"
description: "Deep research workflow for /deepresearch with sources, claims, synthesis, and resumable state."
---

# Deep Research

Use this for `/deepresearch <question>` and for any request that needs more than a quick sourced answer: literature mapping, market/technical due diligence, state-of-the-art reports, factual investigations, or research that should survive across several agent turns.

## Core rule

Do not answer from memory. Build an evidence ledger first, then synthesize. Prefer local/project sources when the question is about the user's workspace; otherwise use web and academic sources.

## When to delegate

Use existing skills as lanes when relevant:

- `00-web-grounded-answers` for factual web grounding and citations.
- `academic-research-hub` for PubMed, arXiv, Semantic Scholar, Google Scholar style work.
- `literature-search` for systematic-review methodology, PRISMA-like screening, inclusion/exclusion criteria.
- `researchclaw` only for full autonomous research pipelines with experiments/paper generation.
- OMOC/team when the research needs parallel lanes: scout, skeptic, verifier, synthesizer.

## Default workflow

1. Create or resume a ledger under `.deepresearch/<slug>/` using `scripts/deepresearch.py init`.
2. Restate the research question, expected output, known constraints, and stop condition.
3. Split the question into 3-7 research lanes. Typical lanes: background, strongest evidence, contrary evidence, current/latest status, implementation details, risks, open questions.
4. Search each lane. For unstable or recent facts, browse. For scientific/medical claims, prioritize papers/reviews and authoritative databases.
5. Record every useful source with `scripts/deepresearch.py source add`.
6. Record atomic claims with `scripts/deepresearch.py claim add`, linking each claim to at least one source id when possible.
7. Mark claims as `supported`, `weak`, `conflicting`, or `unverified` after cross-checking.
8. Write notes and interim summaries frequently with `scripts/deepresearch.py note add` so a crash or context reset does not lose the state.
9. Run `scripts/deepresearch.py brief` before final synthesis to inspect coverage and gaps.
10. Produce the answer with: direct conclusion, evidence map, important caveats, sources, and next actions if useful.

## Quality bar

- Important factual claims need citations.
- Separate evidence from inference.
- Include uncertainty when sources conflict or evidence is thin.
- Prefer primary sources for technical/scientific claims.
- For recommendations or decisions, include tradeoffs and what would change the conclusion.
- Keep raw source snippets short; summarize instead of copying.

## Output shapes

For a normal answer:

- Short answer.
- What I found.
- Evidence and caveats.
- Sources.

For a report:

- Executive summary.
- Method.
- Findings by lane.
- Evidence table or bullet ledger.
- Gaps and confidence.
- Sources.

For a long running investigation:

- State path: `.deepresearch/<slug>/`
- Current decision.
- Completed lanes.
- Open lanes.
- Next command or next research pass.

## Commands

Resolve `scripts/deepresearch.py` relative to this skill directory.

```bash
python3 scripts/deepresearch.py init --question "..." --slug optional-slug
python3 scripts/deepresearch.py lane add --slug optional-slug --name "contrary evidence" --question "What would falsify this?"
python3 scripts/deepresearch.py source add --slug optional-slug --title "..." --url "..." --kind paper --reliability high
python3 scripts/deepresearch.py claim add --slug optional-slug --text "..." --source S001 --status supported
python3 scripts/deepresearch.py note add --slug optional-slug --text "..."
python3 scripts/deepresearch.py brief --slug optional-slug
```

## Integration with OMOC

When OMOC is active, `/deepresearch` can be one lane inside a goal/team/ralph loop. Use the deepresearch ledger as durable evidence, then have OMOC verifier tasks consume the ledger before checkpointing the goal.

Suggested composition:

1. `/goal` defines the decision or report to ship.
2. `/deepresearch` builds evidence under `.deepresearch/<slug>/`.
3. `/team` splits lanes across workers/verifiers.
4. `/ralph` repeats bounded cycles until the ledger has enough evidence or the goal is blocked.

Never let a deepresearch loop run forever without a stop condition. Use explicit coverage criteria: minimum source count, minimum verifier pass, unresolved contradictions, or deadline.
