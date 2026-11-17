# Essay Rewrite Notes

This example shows the new depth passes in action: cognitive-layer pattern removal, specificity pass, and deep voice matching. The draft is a generic AI essay about AI writing. The sample is a real engineering manager who has been writing essays for engineers since 2019.

## Voice Profile (deep)

Built from `sample.txt` plus project context.

Surface:
- avg sentence: ~14 words, short paragraphs (2-4 sentences each)
- punctuation: periods, occasional question marks, no em-dash dependency
- openings: problem-first, often "I" or a verb

Deep:
- concrete-first: numbers, dates, names (9-person team, mid-size fintech, 2019)
- conclusion-first for the problem, setup-first for the solution
- stance: strong on what they have seen, soft on what they have not
- repair visible: "I don't know" and "still uncertain" appear in the sample
- perspective: first person ("I"), team context ("we" only when naming a specific team)
- domain vocabulary: infra, fintech, "engineering managers", "tech leads"
- signature tells: occasional swearing when it fits, ends with the open question
- tolerance: low for hype, high for honesty about limits

## Cognitive-layer AI patterns diagnosed

The draft fails on the deepest layer even after the lexical layer is clean. Diagnosis from `docs/anti-ai-patterns.md` section 5:

- **5.1 Universal-audience framing**: "any forward-thinking organization", "every team member", "from startup founder to enterprise content strategist"
- **5.2 Uniform confidence**: every claim stated with the same enthusiasm, no variation
- **5.3 No stated limits**: "from ideation to distribution", "something for everyone" — no scope, no tradeoff
- **5.5 No visible thinking**: jumps from "AI transforms writing" to "300% gains" to "the future is here" with no "because" or "but" on the page
- **5.6 Generic examples**: "startup founder, marketing director, or enterprise content strategist" — anonymized audience, no actual person
- **5.7 Conflict avoidance**: the only tension mentioned is "those who hesitate risk being left behind" — pure sales framing, not real disagreement

## Specificity pass (from `docs/specificity-and-thought.md`)

Substitution test: replace every number with a vague one and every name with a generic one. The draft still "works". Diagnosis: the draft is not saying anything specific. The whole essay needs a rewrite, not a polish.

Deletion test: remove every "because" and "but". The draft still reads. Diagnosis: the reasoning is decorative, not load-bearing.

Stance test: read aloud. It sounds like a press release. The writer's actual position is invisible.

## Fact-check

- 300% productivity gain: unsupported. `evidence.md` says no study provided. Remove.
- "Elevate quality and authenticity": not a claim the skill makes. Remove the framing.
- "The future of writing is here": rhetorical, not factual. Cut.
- "Define the next decade of content creation": not supported. Cut.

## Rewrite plan

1. Lead with the actual problem the user has seen (per the sample): "I have run a 9-person infra team for six years. AI tools have made our writing faster, but not better."
2. Replace the 300% number with a real or honestly bounded claim.
3. Name one specific thing the team tried, with a result.
4. Surface a tradeoff the user has actually seen.
5. End with the open question, not the grand conclusion (per sample preference).
6. Allow one mild signature tell from the sample: ending with a "still uncertain" note.
7. Match the sample's short-paragraph rhythm. No bullet list — the user does not write that way.

## What this example does not do

- It does not invent the user's specific anecdote. The sample says "I run a 9-person infra team at a mid-size fintech" — that is the only first-person fact available. Everything else stays in third-person observations.
- It does not add swearing just to feel authentic. The sample says swearing is occasional, not constant.
- It does not remove the AI's structural scaffold to "feel different" — it removes it because it was empty, which is the same reason the user would have removed it.
