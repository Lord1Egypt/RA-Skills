# Promotional Blurb Notes

This example exercises all five passes of the upgraded skill workflow. The draft is a one-paragraph product blurb. The voice sample is a product marketer who has been writing customer-facing copy for six years. The draft is short, so the depth of the example is in *every sentence* — there is no room to hide the AI tells in a long piece.

This is also the example that explicitly uses the same draft as `blader/humanizer`'s public demo, so the comparison is direct: the humanize-skill output is what the workflow produces when the soul pass, the fact-check pass, the deep voice profile, and the five-layer pattern catalog all run on a blader-style input.

## 1. Scope (SKILL.md step 1)

- **Audience**: prospective customers of a small SaaS, addressed as individuals.
- **Format**: a short product blurb, single paragraph, no bullets, no headings.
- **Length**: very short — three to four sentences.
- **Personality**: yes. The user writes like a person, not a brochure.
- **Factual support**: this is a product blurb, not a medical product. The fact-check pass is lighter here, but `wrong` claims (300%, "experts say") still get removed.
- **Detector evasion request**: no. The user asked for a quality rewrite.

The voice profile and the soul pass do most of the work on this surface. The pattern catalog does less because the draft is short, but the patterns that *are* present are concentrated — almost every clause carries a tell.

## 2. Voice Profile (SKILL.md step 2 and `docs/voice-profile-deep.md`)

Built from `sample.txt`.

Surface:
- short sentences, period-heavy
- no em dashes (executive team preference)
- no bullet lists in customer emails
- signs with the actual name
- one paragraph at a time

Deep:
- **concrete-first**: numbers when available, plain verbs, no vocabulary inflation
- **first-person perspective**: "I write product copy for..."
- **strong stance on evidence**: "I never quote a study I have not read"
- **stated dislikes**: a long list of "things I avoid" — this is part of the voice
- **signature tell**: ends with the next step
- **low tolerance for hype**: every "things I avoid" item is a hype or AI-vocabulary word

The user has supplied a strong anti-vocabulary list. The rewrite is in good part a vocabulary filter against that list.

## 3. AI-pattern Audit (SKILL.md step 3 and `docs/anti-ai-patterns.md`)

Five layers, condensed because the draft is one paragraph.

### Lexical (1.x)

- 1.1 significance inflation: "pivotal", "testament", "excellence" → remove
- 1.2 promotional vocabulary: "groundbreaking", "cutting-edge", "seamless", "world-class" (not present, but listed) → remove the ones present
- 1.4 approval and enthusiasm: implicit in "Great question!" → remove
- 1.7 corporate and product-noun drift: "ecosystem", "platform", "solution" → "ecosystem" is the worst hit; replace with a specific noun

### Phrasal (2.x)

- 2.1 negative parallelism: "Not just a tool, but a complete ecosystem" → rewrite as a complete thought
- 2.3 universal-audience opener: not present, but the implied audience is "modern teams" which is a universal-audience stand-in → cut or specify
- 2.5 throat-clearing opener: not present
- 2.7 superficial participles: "showcasing how they can unlock" → cut
- 2.8 chatbot residue: "Great question!" → cut
- 2.9 filler: "In order to achieve optimal results" → "to get the result you want" or simply cut
- 2.10 generic conclusions: "the future of work" → cut

### Syntactic (3.x)

- 3.1 balanced parallelism: "showcasing how they can unlock seamless collaboration" — a three-clause rhythm hidden in one clause. Cut.
- 3.2 em dash dependency: not present in the draft. (If it were, the user has explicitly said no em dashes, which lines up with the hard default in `docs/anti-ai-patterns.md` 3.2.)
- 3.3 rule-of-three rhythm: "voice profiling, AI-pattern cleanup, and claim review" — the actual product spec *is* three features, so the rule-of-three is not a problem here. The rule-of-three would be a problem only if the rewrite artificially padded the list to three. Keep the three.
- 3.4 nominalization: not present.
- 3.5 clean sentence boundaries: the draft has fragments and clauses, but in an overstuffed way. The rewrite will be cleaner.
- 3.6 uniform sentence length: the draft is one long sentence with a few clauses. The rewrite will be three or four short sentences, matching the voice profile.

### Structural (4.x)

- 4.2 bullet list as default: not present in the draft. The voice profile explicitly avoids bullets in customer emails. Keep the prose form.
- 4.4 decorative formatting: not present.
- 4.5 TL;DR before the content: not present.

### Cognitive (5.x) — the deepest layer

- 5.1 universal-audience framing: "modern teams" is a vague stand-in for "everyone". Replace with a specific user or remove the framing.
- 5.2 uniform confidence: every claim is stated with the same enthusiasm. The 300% number and the rhetorical close ("future of work") have the same grammatical weight.
- 5.3 no stated limits: the rewrite will state the limit — "we do not have a benchmark for productivity gain."
- 5.4 missing "I" / "we": the draft is in third person. The user's voice is first person. The rewrite uses "we" and "I" appropriately.
- 5.5 no visible thinking: the draft jumps from "great question" to "300% productivity" to "the future of work" with no because, but, although, or so on the page. The rewrite surfaces the reasoning: "we have not measured a number, so we are not going to claim one."
- 5.6 generic examples: "modern teams" with no scale, no segment, no specific use. The rewrite can either name a segment or skip the framing.
- 5.7 conflict avoidance: the draft does not admit any tradeoff or limit. The rewrite admits the limit (no benchmark).
- 5.8 hedging without commitment: not present in the draft; the rewrite will hedge the unsupported claims and commit on the supported ones.

## 4. Specificity and Thought Visibility (SKILL.md step 4.5 and `docs/specificity-and-thought.md`)

Substitution test: replace "pivotal" with "important", "groundbreaking" with "new", "seamless" with "easy", "300%" with "X%". The paragraph still reads. Diagnosis: nothing in the draft is doing real work. The whole paragraph needs a rewrite, not a polish.

Deletion test: remove every "because", "but", "although", "so". The paragraph still reads. Diagnosis: the reasoning is decorative, not load-bearing. The rewrite needs to make the reasoning load-bearing.

Stance test: read aloud. It sounds like a press release, not a person writing to a customer. Diagnosis: the writer's actual position (which is "no hype, cite what you have, sign your name") is invisible. The rewrite puts it on the page.

Specifics to add (from `evidence.md` Source 1):
- three named features: voice profiling, AI-pattern cleanup, claim review
- it runs as a skill inside an agent
- it is not a standalone CLI
- what is *not* measured: a productivity gain

Reasoning to surface:
- "We do not have a benchmark for productivity gain, so we are not going to claim one."
- "We can name the three things the product does. We can name what it does not do."

A limit to state:
- the rewrite states the limit explicitly. This is a feature, not a hedge. The user's voice profile rewards honesty about limits.

## 5. Fact-Check (SKILL.md step 5 and `docs/fact-check.md`)

Per-claim status (using the 7-state system):

| Claim | Type | Source | Status | Fix |
| --- | --- | --- | --- | --- |
| 300% productivity increase | number, attribution | None | `wrong` | Remove |
| Experts say this is the future of work | attribution | None | `wrong` (vague attribution) | Remove |
| Studies show (vague) | attribution | None | `wrong` (vague attribution) | Remove |
| The product is groundbreaking / cutting-edge / seamless | promotional | None needed (Wikipedia confirms the cluster) | `style_only` | Rewrite in plain verbs |
| The product has three named features | descriptive, product | Source 1 (user spec) | `supported` | Keep |
| It runs as a skill inside an agent | descriptive, product | Source 1 | `supported` | Keep |
| It is not a standalone CLI | descriptive, product | Source 1 | `supported` | Keep |

### On the user's own claims (per `docs/fact-check.md`)

The user supplied a product spec (Source 1) with three concrete features. Treat these as `supported`. The user did not supply a productivity number. The draft's 300% claim is the AI's invention, not a fact-check error from the user. The rewrite does not need to gently correct the user — there is no user error here.

### On tool availability

Web/search tools are available. The fact-check pass used them to verify the canonical AI-vocabulary cluster in the Wikipedia article, and to confirm that no source in the user's environment supports the 300% claim. If they had not been available, the external claims would have defaulted to `unverified`.

### Fix matrix application

- `supported` (three named features, runs as a skill, not a CLI) → keep, stated plainly
- `wrong` (300%, "experts say", "studies show") → remove, do not hedge
- `style_only` (the AI vocabulary cluster) → rewrite in plain language

## 6. Soul Pass (SKILL.md step 5 of 5 and `docs/personality-and-soul.md`)

After the four mechanical passes, the soul pass asks: is the writer present on the page?

The user's sample carries soul in three places:

- **Concrete experience**: "I have been doing this for six years" — a real tenure, not a generic "I am passionate about writing."
- **Stated position**: "I never quote a study I have not read" — a position with consequences, not a hedge.
- **Visible dislikes**: the long "things I avoid" list is a signature. It is the user's voice, in negative space.

The rewrite carries the same three signals:

- A real number or specific feature in place of the 300% claim.
- A stated position on what the product does not do, in the user's voice.
- The user's dislikes (the "I never use" list) honored in the rewrite's vocabulary.

If the writer's voice is in the rewrite, the soul pass is done. If the rewrite could have been produced by any generic marketing tool, the soul pass failed and the rewrite should be re-done with the voice profile stronger in the foreground.

## 7. Final Rewrite Plan

Single paragraph, three to four short sentences, plain verbs, no em dashes, no bullets, no hype vocabulary, signed with the user's name. State what the product does (three named features, the form factor, what is not measured). End with the next step.

## 8. What the rewrite does not do

- It does not invent a productivity number, a study, or a named expert.
- It does not use any word from the user's "things I avoid" list.
- It does not introduce an em dash. The voice profile forbids it; the catalog default removes it.
- It does not pad the list of features to look more impressive.
- It does not include the user's name — they did not supply it. The placeholder `[name]` is kept.
