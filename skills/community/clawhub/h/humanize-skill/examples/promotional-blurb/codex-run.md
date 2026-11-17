# Codex Skill E2E Run: Promotional Blurb (Five-Pass Workflow)

Run date: 2026-06-07
Host: Codex
Mode: agent-native semantic rewrite, no CLI or regex rewrite pass
Surface: short product blurb (one paragraph)
Risk class: low — product copy, not medical or legal

## Scope

- **Surface**: product blurb, single paragraph.
- **Audience**: prospective customers, addressed as individuals.
- **Goal**: rewrite a generic AI-style product blurb into one that matches the user's actual voice and reports only what the product spec supports.
- **Evidence policy**: every product claim must trace to `evidence.md` Source 1. No productivity number, no vague attribution.

## Voice Profile (deep)

From `sample.txt`:

Surface:
- short sentences, period-heavy
- no em dashes (executive team preference)
- no bullets
- signs with the actual name

Deep (see `docs/voice-profile-deep.md`):
- **concrete-first**: real numbers when available, plain verbs
- **first-person perspective**
- **strong stance on evidence**: "I never quote a study I have not read"
- **stated dislikes**: a long "things I avoid" list is part of the voice
- **signature tell**: ends with the next step
- **low tolerance for hype**

## AI-pattern Audit (5 layers)

Lexical: removed "groundbreaking", "pivotal", "cutting-edge", "seamless", "ecosystem", "solution", "testament", "excellence", "modern", "unlock".

Phrasal: removed "Great question!", "In order to achieve optimal results", "showcasing how they can unlock", "Not just a tool, but a complete ecosystem", "the future of work".

Syntactic: replaced one long sentence with three short ones; removed three-clause parallelism inside a single clause; the rule-of-three in the *real* product spec (voice profiling, AI-pattern cleanup, claim review) is genuine and stays.

Structural: kept prose form (no bullets, per the voice profile).

Cognitive (the deepest layer):
- removed universal-audience framing ("modern teams")
- broke uniform confidence (the rewrite varies confidence by claim type: confident on what the product does, explicit about what it does not claim)
- surfaced the limit ("We do not have a benchmark for productivity gain, so we are not going to claim one.")
- moved to first person ("our product", "we do not have a benchmark")
- replaced the generic example ("modern teams") with a specific capability ("builds a voice profile from your samples")
- stated a position: the product does three things, and the limit is stated plainly
- the rewrite has no fake personality, no performed enthusiasm, no performed stakes

## Specificity Pass

Substitution test: replace "groundbreaking" with "new", "pivotal" with "important", "300%" with "X%", "modern teams" with "teams". The paragraph still reads. Diagnosis: nothing in the draft is doing real work. The whole paragraph needs a rewrite, not a polish.

Deletion test: remove every "because", "but", "so". The paragraph still reads. Diagnosis: the reasoning was decorative. The rewrite makes it load-bearing: "We do not have a benchmark for productivity gain, so we are not going to claim one."

Stance test: the rewrite sounds like a person writing to a customer. The user's voice profile is in the foreground.

Specifics added: three named features, the form factor (skill for agents), the limit (no benchmark). All from `evidence.md` Source 1.

## Fact-Check (7-state system)

| Claim | Status | Fix |
| --- | --- | --- |
| 300% productivity increase | `wrong` (no source) | Removed |
| "Experts say this is the future of work" | `wrong` (vague attribution) | Removed |
| "Studies show..." | `wrong` (vague attribution) | Removed |
| Three named features | `supported` (Source 1) | Kept |
| Runs as a skill inside an agent | `supported` (Source 1) | Kept |
| Not a standalone CLI | `supported` (Source 1) | Kept |
| AI vocabulary cluster | `style_only` (Wikipedia confirms) | Replaced with plain verbs |

## Soul Pass

After the four mechanical passes, the soul pass asked: is the writer present on the page?

The user's sample carries soul in concrete experience, stated position, and stated dislikes. The rewrite carries the same three:

- Real features in place of the 300% claim.
- Stated position on what the product does not do, in the user's voice ("we are not going to claim one").
- The user's "things I avoid" list honored — the rewrite contains none of the listed words.

The writer is present. The soul pass is done.

## Final Rewrite (in three sections for the audit report)

### Draft

The original one-paragraph draft with the AI tells in place: "Great question!" chatbot residue, "groundbreaking / pivotal / cutting-edge / seamless" promotional cluster, "in order to achieve optimal results" filler, "Studies show a 300% productivity increase" invented statistic, "experts say" vague attribution, "Not just a tool, but a complete ecosystem" negative parallelism, "stands as a testament to modern engineering excellence" grand close.

### Still-AI (after the four mechanical passes)

After the pattern catalog, voice profile, specificity pass, and fact-check pass, the draft is reduced to:

- Three supported claims (the three named features, the form factor).
- One explicit limit ("we do not have a benchmark for productivity gain").
- No invented statistics. No vague attributions. No promotional vocabulary. No "not just X, but Y". No "Great question!". No em dashes.

The remaining piece is two short sentences and a CTA. The soul pass decides whether the writer is in those two sentences. In this run, the writer is present: the explicit limit is a signature move from the user's sample, and the CTA matches the user's preferred next-step close.

### Final

See `final.md`.

## Final Audit

- Does any sentence still sound like generic AI copy? No.
- Does the rewrite pass the substitution, deletion, and stance tests? Yes.
- Did the rewrite preserve all important content? It preserved the three product features and the form factor. It removed the invented statistic and the vague attribution, neither of which was in the user's voice or evidence.
- Did the voice match the surface profile *and* the deep profile? Yes.
- Is the writer present on the page? Yes — the soul pass landed.
- Are unsupported facts removed, softened, or flagged? Removed.
- Are citations present when factual risk is meaningful? Not needed for the surface (informal product blurb). The audit trail in `notes.md` and `evidence.md` is the citation.
- Did the final text avoid self-explanatory agent/editor commentary? Yes.
- Is the result better writing, not just shaped text? Yes.

## What this example demonstrates

- The five-pass workflow (pattern catalog, voice profile, specificity, fact-check, soul) running on the shortest possible surface — a single paragraph.
- The five-layer AI-pattern catalog (lexical, phrasal, syntactic, structural, cognitive) with the cognitive layer doing the heaviest lifting on a draft that is mostly hype.
- The deep voice profile (concrete-first, strong stance on evidence, signature dislikes) translating directly into a vocabulary filter.
- The specificity pass (substitution, deletion, stance) diagnosing a draft that is *all* decoration.
- The 7-state fact-check (with `wrong` removed, not hedged).
- The soul pass (the smallest pass in edits, the largest in feel — the rewrite could not have been produced by a generic marketing tool).
- The three-section editing report (Draft / Still-AI / Final) from the upgraded Final audit in `SKILL.md` step 6.
- The boundary: nothing in this rewrite was done to make a detector happy. The rewrite is shorter, plainer, more honest, and harder to misread as marketing — and that is the same direction any careful customer-facing writer would push the blurb.
