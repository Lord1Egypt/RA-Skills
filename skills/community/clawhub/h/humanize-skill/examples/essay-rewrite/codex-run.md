# Codex Skill E2E Run: Essay Rewrite (Depth Passes)

Run date: 2026-06-06
Host: Codex
Mode: agent-native semantic rewrite, no CLI or regex rewrite pass

## Scope

- Surface: short essay for engineering managers.
- Audience: engineering managers and tech leads.
- Goal: rewrite a generic AI essay into one with the user's actual voice, concrete specifics, visible reasoning, and a real stance.
- Evidence policy: remove the unsupported 300% statistic, soften universal claims, end with the user's preferred "still uncertain" close.

## Voice Profile (deep layer)

Built from `sample.txt`.

Surface:
- short paragraphs (2-4 sentences)
- problem-first openings
- periods, occasional question marks
- no bullet lists, no decorative formatting

Deep (see `docs/voice-profile-deep.md`):
- concrete-first: numbers, dates, team size
- strong stance on what has been observed, soft on what has not
- visible "I don't know" / "still uncertain" notes
- first-person perspective
- signature tell: ending with an open question rather than a grand conclusion
- occasional swearing; not applied here (the surface does not call for it)

## AI-pattern Audit (five layers)

Lexical: removed "fundamentally transforming", "fast-paced content landscape", "leverage", "elevating", "publication-ready".

Phrasal: removed "not just X, but Y" parallelism, "from ideation to distribution" false range, "the time to act is now" generic urgency.

Syntactic: removed the rule-of-three rhythm and the universal-audience "Whether you are a startup founder..." opener.

Structural: removed the intro/body/conclusion sandwich and the grand conclusion. The user's sample does not write that way.

Cognitive (the deepest layer, the one most relevant to misclassification):
- removed universal-audience framing — replaced with a real team, a real size, a real industry
- removed uniform confidence — the rewrite varies confidence by claim type
- removed "no stated limits" — the rewrite states the limit ("If we start shipping the first draft...")
- surfaced reasoning with the "but" (faster vs better) and the "because" (the bottleneck was never grammar)
- surfaced the "I don't know" with "I am still uncertain whether..."
- replaced generic examples with one real pattern from the user's sample ("started using them in late 2023")
- stated a position: AI is a faster first draft, not a finished one

## Specificity Pass

See `docs/specificity-and-thought.md`.

Substitution test: replaced "300% productivity" with an honestly bounded claim ("roughly double on first drafts", "editor quality score has stayed flat").

Deletion test: kept every "but", "because", and "I do not have" on the page — each is load-bearing.

Stance test: the rewrite now has a position (AI helps phrasing, not thinking) instead of a press release voice.

## Fact Decisions

| Claim | Decision | Evidence handling |
| --- | --- | --- |
| Teams see 300% productivity gains | Removed | No study provided in `evidence.md` |
| AI elevates quality and authenticity | Removed | Not a claim the skill makes |
| The future of writing is here | Cut | Rhetorical, not factual |
| 9-person team at a mid-size fintech since 2019 | Kept | From user's sample |
| Roughly doubled first drafts, editor quality flat | Kept | Framed as observation, not benchmark |
| Effect is net positive only if the team treats the tool as a first draft | Kept | Writer's stated position |

## Final Rewrite

See `final.md`.

## Final Audit

- Did the rewrite preserve the original surface (short essay for engineering managers)? Yes.
- Did the voice match the deep profile (concrete-first, problem-first, visible limits, "still uncertain" close)? Yes.
- Did the rewrite pass the substitution, deletion, and stance tests? Yes — every specific is on the page, every "because" is load-bearing, the writer has a position.
- Did the rewrite avoid self-explanatory editor commentary? Yes.
- Did the rewrite add claims, experiences, or numbers the user did not supply? No.
- Is the result better writing, not just shaped text? Yes.

## What this example demonstrates

- The five-layer pattern catalog from `docs/anti-ai-patterns.md`, especially the cognitive layer.
- The deep voice profile from `docs/voice-profile-deep.md`, including the signature "still uncertain" close.
- The specificity and thought visibility pass from `docs/specificity-and-thought.md`, with the three tests applied.
- The fact-check pass: the 300% number is the headline removal, but several rhetorical-but-non-factual phrases are also cut.
- The boundary: nothing in this rewrite was done to make a detector happy. The rewrite reads like the user because it follows the user's voice profile, the deep profile, the specificity pass, and the catalog — in that order.
