# Architecture Boundary

This reference explains the current Mom AI Agent content split so the skill does not over-claim coverage.

## Current Model

There are three relevant content layers:

1. `KB answer layer`
2. `Evidence-qualified insight layer`
3. `Website article layer`

The skill currently uses the public `KB answer layer` plus the public `insights` layer plus `topics` for navigation.

## KB Answer Layer

Current public surfaces:

- `/api/kb/query`
- `/api/kb/feed`
- `/api/kb/rules`
- `/api/kb/guides`
- `/api/kb/foods`
- `/api/kb/topics`
- `/api/kb/faqs`

These surfaces expose structured, read-only objects intended for retrieval and agent use.

Important implication:

- This is a smaller high-certainty layer, not the whole content system.

## Evidence-Qualified Insight Layer

Current public surface:

- `/api/kb/insights`

This layer is derived from published `articles + citations`, but only exposes the subset that passes the current public evidence filter.

Important implications:

- The `insights` surface is public and skill-eligible.
- It is one of the main public coverage layers when structured KB coverage is sparse.
- It is still a filtered evidence subset, not a replacement for all structured KB objects.
- Not every website article is insight-eligible.

## Website Article Layer

The broader website content system is centered on `articles + citations`.

Important implications:

- `articles + citations` is the real source-of-truth content layer.
- The website may contain relevant pages that are not exposed through `/api/kb/*`.
- A relevant article is not automatically a skill-eligible evidence object.
- The skill must not imply that the full article corpus has been searched when only `/api/kb/*` was used.

## Current Answering Rule

Use this language model:

- `Strong authority KB match found`: answer from KB and cite KB evidence.
- `KB sparse or weaker but insight strong`: answer from the evidence-qualified insight layer and say that explicitly.
- `No strong direct answer but topic fit exists`: route through topics rather than pretending there is a source-linked answer.
- `No strong public match`: say the current public KB plus insight surfaces do not show a strong source-linked match.
- `Do not infer site-wide absence`: lack of KB match is not proof the topic is absent from the entire website.

## Why This Boundary Exists

The current site architecture mixes:

- structured answer objects
- editorial or explainer content
- article pages with varying citation density

For a parenting evidence skill, these should not all be treated as equivalent evidence objects.

## Future Direction

The current public API already exposes the first article-derived evidence layer without introducing a new table.

The expected next step is still not a new table by default. Prefer:

1. keep `articles + citations` as the source-of-truth content layer
2. keep `kb_*` as the high-certainty answer layer
3. continue improving the article-derived evidence surface through public API filters and ranking

That future surface should:

- filter article eligibility
- preserve source and freshness metadata
- avoid treating all editorial content as evidence

## Practical Guidance For The Skill

- Be explicit about current limits.
- Prefer precision over completeness.
- Do not blur the line between `structured evidence answer`, `evidence-qualified insight`, and `related article`.
- When coverage is limited, route the user toward the closest KB or insight path rather than pretending broader evidence was retrieved.
- Do not mix a generic LLM fallback into the authoritative answer layer. If another product surface adds one, label it as non-authoritative exploratory guidance.
