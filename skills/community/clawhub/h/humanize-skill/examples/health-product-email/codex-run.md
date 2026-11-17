# Codex Skill E2E Run: Health Product Email (High-Risk Surface)

Run date: 2026-06-06
Host: Codex
Mode: agent-native semantic rewrite, no CLI or regex rewrite pass
Surface: customer-facing product launch email
Risk class: medical / health claims, FDA-regulated category

## Scope

- **Surface**: customer email announcing a pilot result.
- **Audience**: existing and prospective Pulse users, plus clinicians who may recommend it.
- **Goal**: rewrite a draft that overclaims health outcomes, into one that reports only the pilot's actual measurements and explicitly declines to claim what the pilot did not measure.
- **Evidence policy**: every numerical claim must trace to `evidence.md`. Medical claims require a tier-1 source or must be removed. Universal claims and grand closes are out of voice.

## Voice Profile (deep)

From `sample.txt`:

Surface:
- short paragraphs (3-5 sentences)
- periods, occasional dashes
- no bullet lists in customer emails
- no emojis
- signs with the actual name

Deep (see `docs/voice-profile-deep.md`):
- **concrete-first**: specific user segments with named conditions, never "users"
- **strong stance on what is published**: never promise health outcomes that are not defended by a published study
- **visible limits**: "When I do not know, I say so"
- **first-person perspective**
- **signature tell**: ends with an open question, never a grand close
- **low tolerance for personality** — direct, no swearing, no enthusiasm displays

## AI-pattern Audit (5 layers, see `docs/anti-ai-patterns.md`)

Lexical: removed "fundamentally transforming", "groundbreaking", "state-of-the-art", "world-class", "revolutionary", "innovative, scalable, and seamless", "tirelessly".

Phrasal: removed "It is well known that...", "Studies show...", "Whether you are a busy professional, a concerned parent, or a senior...", "Not just another health app; it is a revolutionary step...", "The time to act is now", "In today's rapidly evolving healthcare landscape".

Syntactic: removed the three-clause parallelism in paragraph 2; varied sentence length across the rewrite.

Structural: kept the three-paragraph shape (pilot result / non-claim / next step) but replaced the original content.

Cognitive (the deepest layer):
- removed universal-audience framing ("every person", "something for everyone")
- broke uniform confidence (rewrite varies confidence by claim type)
- surfaced the limit explicitly ("one clinic in Boston", "we did not measure X")
- moved to first person ("we put... in the hands of", "we did not measure")
- replaced generic role examples with the actual user cohort
- stated a position: the companion surfaces patterns; the clinician decides
- removed "we are not claiming" hedged into thinness — the rewrite is direct about what it does not claim and why

## Specificity Pass (see `docs/specificity-and-thought.md`)

- Numbers: 320 patients, one clinic, Boston, 90 days, 78%, 2.8 minutes, 30 seconds. All from `evidence.md` Source 5.
- Time: "Three months ago" → "in the first quarter of 2026" is more precise. Kept "Three months ago" because the user's sample prefers natural phrasing; the source date is in `evidence.md`.
- Place: Boston, single clinic.
- Names: the user did not supply the CEO's name. The rewrite uses `[name]` as a placeholder.
- Sensory / concrete detail: "first 30 seconds of a visit were the most useful; less so after that" carries the pilot's actual texture.

Thought visibility (the six moves):
- "but": "We did not measure weight loss, doctor visits, or diagnostic accuracy in this pilot, *so* we are not going to claim any of those." (the rewrite merges "but" into the because.)
- "because": "When we do not have a study to point to, we do not claim the outcome." This is the load-bearing reason; the rewrite surfaces it explicitly.
- "I don't know": "We are still figuring out what the next pilot should measure." Honest hedge on the open question.
- "I changed my mind": not applicable — the user did not supply a prior version.
- comparison: not applicable — the email is about one product's pilot.
- limit: stated three times: "320 patients at one clinic", "did not measure X, so we are not going to claim", "We are not claiming Pulse detects heart disease..."

Substitution test: replace specific numbers with placeholders. "Many patients" / "a high percentage" / "around three minutes" — the email still "works" if you remove the numbers. Diagnosis: the rewrite is *not* carrying water via numbers; it is carrying the numbers themselves. The structure holds because the limits are on the page.

Deletion test: remove the "because" / "so" / "when" clauses. The argument weakens noticeably. Diagnosis: the reasoning is load-bearing, not decorative. Pass.

Stance test: read aloud. Sounds like a CEO writing to her or his users, not a press release. Pass.

## Fact-Check (7-state system, see `docs/fact-check.md`)

| Claim | Type | Source | Status | Fix |
| --- | --- | --- | --- | --- |
| 47% reduction in doctor visits | number, attribution | None | `wrong` | Removed |
| 12-pound weight loss in 30 days | number, prediction | Cochrane 2024 contradicts | `wrong` | Removed |
| 94% diagnostic accuracy for heart disease | number, medical, attribution | Stanford 2023 contradicts (75-85% ceiling); FDA 2023 implies SaMD clearance required | `wrong` (number) and `contested` (regulatory) | Removed and re-cast as a non-claim |
| "Studies show..." (vague) | attribution | None | `wrong` (vague attribution) | Removed |
| 320 patients, one clinic, Boston, 90 days | number, experience | Source 5 (user-supplied) | `supported` | Kept |
| 78% opened the app at least once a day | number, experience | Source 5 | `supported` | Kept |
| 2.8-minute average session | number, experience | Source 5 | `supported` | Kept |
| First 30 seconds of a visit most useful | experience | Source 5 | `supported` | Kept |
| "We did not measure weight loss, doctor visits, or diagnostic accuracy" | self-attestation | Source 5 | `supported` | Kept |
| "We are not claiming Pulse detects heart disease" | declarative non-claim | Source 5 self-attestation | `supported` (the company is not making the claim) | Kept |
| "Surfaces patterns from the data the user puts in. The clinician decides..." | descriptive, product | Source 5; FDA 2023 supports the clinician-decides framing | `supported` | Kept |
| "Innovative, scalable, and seamless" | promotional, no factual content | None | `style_only` | Removed |
| "Time to act is now" | rhetorical urgency | None | `style_only` | Removed |
| "Every person manages their wellbeing" | universal claim | None | `unverified` | Removed |

### Cross-source conflict protocol

The 94% claim is contradicted by two independent sources (FDA 2023 regulator + Stanford 2023 peer-reviewed). Tier-1 sources win. The 47% and 12-pound claims have no source at all — status `wrong`, not `weak_support`. The rewrite removes all three rather than hedging.

### Tool availability

Web/search tools were available. The fact-check pass used them to retrieve and verify the four external sources in `evidence.md`. If they had not been available, all external claims would have defaulted to `unverified` and the limitation would have been stated in the rewrite output.

### User-supplied-but-wrong

The user did not supply wrong claims in this draft; the wrongness was in the AI's auto-generated draft text. The user's pilot data is consistent with what the rewrite reports. No gentle correction of the user was needed.

## Final Rewrite

See `final.md`.

## Final Audit

- Does any sentence still sound like generic AI copy? No — the voice is the user's sample voice.
- Does the rewrite pass the substitution, deletion, and stance tests? Yes.
- Did the rewrite preserve all important content? It preserved every supported number from `evidence.md` Source 5. It removed the unsupported marketing claims, which were not in the user's voice or the user's evidence.
- Did the voice match the surface profile *and* the deep profile? Yes — short paragraphs, first person, "I do not know" hedges on the open question, signed name.
- Are unsupported facts removed, softened, or flagged? Removed. The 47% / 12-pound / 94% claims were `wrong` (some had direct contradicting sources) and would have been unethical to hedge into plausibility.
- Are citations present when factual risk is meaningful? Source 5 numbers are stated plainly. The FDA / Cochrane / Stanford / Harvard citations are in `evidence.md` and can be added inline if the surface becomes formal. The current customer email does not need inline citations; the audit trail in `notes.md` and `evidence.md` is sufficient.
- Did the final text avoid self-explanatory editor commentary? Yes — no "I removed the hype" or "I stripped the AI framing" lines.
- Is the result better writing, not just shaped text? Yes — and the rewrite is *safer* in the medical sense, which is the point of the fact-check pass on a high-risk surface.

## What this example demonstrates

- The 5-layer AI-pattern catalog (lexical, phrasal, syntactic, structural, **cognitive**), with the cognitive layer doing the heaviest lifting on a high-stakes surface.
- The deep voice profile (concrete-first, strong stance on what is published, visible limits, signature open-question close).
- The specificity pass (numbers, place, time, names, sensory detail) plus the three tests (substitution, deletion, stance).
- The depth fact-check: 7-state label system, source tier judgment (FDA + Cochrane + Stanford = tier 1, tier 1 wins), direct contradiction protocol, tool availability noted, the difference between `supported` and `wrong` made explicit.
- The fix matrix in action: `wrong` is removed, not hedged. `style_only` is removed. `supported` is stated plainly. `unverified` is cut.
- The boundary: nothing in this rewrite was done to make a detector happy. The rewrite is shorter than the draft, more honest, and more useful — and that is the same direction any reasonable medical regulator would push the email.
