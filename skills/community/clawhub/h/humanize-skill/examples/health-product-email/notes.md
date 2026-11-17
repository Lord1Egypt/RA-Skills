# Health Product Email Notes

This example exercises all four passes of the upgraded skill workflow, with the fact-check pass doing the heaviest lifting. The draft is a launch email for a consumer health app. It is the worst-case surface for the skill: a medical product, an audience that will trust the claims, a draft that invents statistics, fabricates authority, and promises diagnostic accuracy the product has not earned.

## 1. Scope (from SKILL.md step 1)

- **Audience**: existing and prospective users of a consumer health product, plus the clinicians who may recommend it. Mixed: lay readers and medical professionals.
- **Format**: customer-facing email, single body, signed by the CEO.
- **Length**: short — the user's sample says "short paragraphs, direct".
- **Personality**: yes — the user's sample is direct and personal, not generic SaaS.
- **Factual support**: this is a **medical product**. The fact-check pass is non-negotiable. Source tier 1 required for any diagnostic, clinical, or outcome claim.
- **Detector evasion request**: no. The user asked for a quality rewrite.

Plain and neutral is the correct voice for some parts. Direct and personal is the correct voice for others. Match the surface, not the AI's default enthusiasm.

## 2. Voice Profile (from SKILL.md step 2 and `docs/voice-profile-deep.md`)

Built from `sample.txt`.

Surface:
- short paragraphs (3-5 sentences each)
- periods, occasional dashes, no em-dash dependency
- no bullet lists in customer emails
- no emojis
- signs with the actual name

Deep:
- **Concrete-first**: names specific user segments ("a 58-year-old on hypertension medication"), never "users"
- **Conclusion-first for the safety frame**: leads with what is known and what is not known
- **Strong stance on what is published**: "I never promise health outcomes I cannot defend with a published study"
- **Visible limits**: "When I do not know, I say so"
- **First-person perspective** ("I run a healthcare company")
- **Domain vocabulary**: clinical, peer-reviewed, published trial, primary source
- **Signature tell**: ends with the open question, never the grand close; "Reply to this email or book a 30-minute slot" is the kind of CTA that fits
- **Tolerance for personality**: low — direct, no swearing, no enthusiasm displays

## 3. AI-pattern Audit (from SKILL.md step 3 and `docs/anti-ai-patterns.md`)

Five layers.

### Lexical

- "fundamentally transforming", "groundbreaking", "state-of-the-art", "world-class", "revolutionary", "innovative, scalable, and seamless", "tirelessly" — all in the promotional and significance-inflation cluster. Remove.

### Phrasal

- "It is well known that..." — generic opener, removes with a single cut.
- "Studies show..." — fuzzy attribution. Removed.
- "Whether you are a busy professional, a concerned parent, or a senior..." — universal-audience opener. Removed.
- "Not just another health app; it is a revolutionary step..." — negative parallelism. Removed.
- "From ideation to distribution" / "from busy professional to senior" — false range. Removed.
- "The time to act is now" — generic urgency. Removed.
- "In today's rapidly evolving healthcare landscape" — throat-clearing opener. Removed.

### Syntactic

- Three-clause parallelism in the second paragraph ("analyze your biometric data, predict potential health issues, and provide personalized recommendations"). Cut to a specific feature description.
- Em dashes not heavy here; sentence length uniform across all three paragraphs (15-25 words each). Rewrite will vary length.

### Structural

- Three-paragraph essay structure (intro / body / close) is appropriate for an email, but the **content** of each paragraph is wrong. Paragraph 1 has the marketing claims. Paragraph 2 has the universal-audience feature list. Paragraph 3 has the grand close.
- The rewrite will keep the three-paragraph shape, but paragraph 1 becomes "what we piloted and what we measured", paragraph 2 becomes "what we are not claiming and why", and paragraph 3 becomes the next concrete step.

### Cognitive (the deepest layer — see `docs/anti-ai-patterns.md` section 5)

- **5.1 Universal-audience framing**: "every person", "something for everyone". The user's sample explicitly rejects this.
- **5.2 Uniform confidence**: every claim is stated with the same enthusiasm. The clinical accuracy claim ("94%") and the rhetorical close ("time to act is now") have the same grammatical weight. The user's sample says never promise health outcomes that are not defended by a published study.
- **5.3 No stated limits**: zero. No "we have not measured...", no "in a single clinic", no "this is engagement, not outcome".
- **5.4 Missing "I" / "we"**: third-person throughout. The user runs the company; the rewrite is in first person.
- **5.5 No visible thinking**: the email moves from "AI is transforming healthcare" to "47% fewer doctor visits" to "94% accuracy" with no because, but, although, or so on the page. The reasoning is hidden.
- **5.6 Generic examples**: "a busy professional, a concerned parent, or a senior". These are placeholder roles, not real patients. The user's sample says "a 58-year-old on hypertension medication".
- **5.7 Conflict avoidance**: the email presents the product as if no tradeoff, no risk, and no competing option exist. The user's sample says "I never promise health outcomes I cannot defend".
- **5.8 Hedging without commitment**: "potentially", "tailored to your unique needs" — empty hedging that does not acknowledge what the product does not do.

## 4. Specificity and Thought Visibility (from SKILL.md step 4.5 and `docs/specificity-and-thought.md`)

Substitution test: replace "47%" with "X%", "94%" with "Y%", and the user "busy professional" with a generic role. The email still reads. Diagnosis: nothing in the email is specific. The whole thing needs a rewrite, not a polish.

Deletion test: remove every "because", "but", "although", "so". The email still reads. Diagnosis: the reasoning is decorative, not load-bearing.

Stance test: read aloud. It sounds like a press release, not a CEO writing to her or his own users. Diagnosis: the writer's actual position (which is *do not overclaim*) is invisible.

Specifics to add (drawn from `evidence.md` Source 5):
- 320 patients, one clinic, Boston, 90 days
- 78% opened daily
- 2.8-minute average session
- 30 seconds useful per visit (per clinician report)
- What was *not* measured: weight loss, doctor visits, diagnostic accuracy

Reasoning to surface (drawn from the user's sample stance):
- "We did not measure X, so we are not going to claim X."
- "The companion surfaces patterns. The clinician decides what they mean."
- "Here is what we are not claiming and why."

A limit to state explicitly:
- Pulse is one clinic, one pilot, 320 patients, no control group. That is the scope. The email should say so.

## 5. Fact-Check (from SKILL.md step 5 and `docs/fact-check.md`)

This is the pass that decides what survives.

### Per-claim status (using the 7-state system from `docs/fact-check.md`)

| Claim | Type | Source | Status | Fix |
| --- | --- | --- | --- | --- |
| AI reduces doctor visits by 47% | number, attribution | None | `wrong` | Remove |
| Users lose 12 pounds in 30 days | number, prediction | Cochrane 2024 contradicts | `wrong` | Remove |
| Pulse detects heart disease with 94% accuracy | number, medical, attribution | Stanford 2023 puts ceiling at 75-85%; FDA 2023 implies SaMD clearance required | `wrong` (numerical) and `contested` (regulatory) | Remove and re-cast as a planning claim |
| Pulse's diagnostic engine is proprietary | descriptive, identity | None | `style_only` | Keep, with the term adjusted |
| Pulse offers something for everyone | universal claim | None | `unverified` (treat as factual) | Cut |
| Pulse predicts potential health issues before they arise | causal / prediction, medical | None | `unverified` and likely `wrong` | Soften to "surfaces patterns the user can review with a clinician" |
| Time to act is now | rhetorical | None | `style_only` | Remove |
| Revolutionary step / innovative, scalable, and seamless | promotional | None | `style_only` | Remove |
| Every person manages their wellbeing | universal claim | None | `unverified` | Cut |

### On the user's own claims (per `docs/fact-check.md`)

The user supplied pilot data (Source 5: 320 patients, Boston, 90 days, 78% engagement, 2.8-min session). Treat this as `supported` (primary, user-supplied). Do not extend it. The pilot measured engagement and self-reported satisfaction only. It did **not** measure weight loss, doctor visits, or diagnostic accuracy. The marketing claims that depend on those missing measurements are `wrong` or `unverified` and must come out.

### On tool availability (per `docs/fact-check.md`)

Web/search tools are available in this run. The fact-check pass used them to find the Harvard 2022 review, the FDA 2023 guidance, the Cochrane 2024 review, and the Stanford 2023 study. The source tier, date, and direct contradiction are recorded in `evidence.md`.

### Conflict protocol (per `docs/fact-check.md`)

The 94% claim is contradicted by two independent sources from different tiers (FDA regulator + Stanford peer-reviewed). Tier-1 source wins. Status: `wrong` for the number, `contested` for the regulatory status. The rewrite removes the number entirely rather than hedging it.

The 12-pound / 30-day claim is contradicted by a tier-1 systematic review. Status: `wrong`. The rewrite removes it.

The 47% claim has no source at all. Status: `wrong`. The rewrite removes it.

### Fix matrix application (per `docs/fact-check.md`)

- `supported` (pilot data) → keep, state plainly. "320 patients at one clinic in Boston over 90 days."
- `wrong` (47%, 12 pounds, 94%) → remove. Do not hedge a known error into a softer error.
- `unverified` (universal claim about everyone) → cut.
- `style_only` (rhetorical framing) → remove.
- `contested` (regulatory status) → do not assert; re-cast as a planning or scope claim if needed.

## 6. Final Rewrite Plan

Use the user's sample voice. Three paragraphs.

Paragraph 1 — what we piloted, what we measured, what we did not measure. Use Source 5 numbers. Surface the limit (one clinic, 320 patients, 90 days, no clinical endpoints).

Paragraph 2 — what we are not claiming and why. List the unsupported marketing claims the draft tried to make, and explain why they are not in the email. "We are not claiming Pulse detects heart disease. We are not claiming users will lose weight. We are not claiming fewer doctor visits." Tie to the user's stance: "When we do not have a study, we do not claim the outcome."

Paragraph 3 — the next step. Open question per the sample's signature tell. CTA that fits the voice ("Reply to this email or book a 30-minute slot with the team").

Sign with the actual name (per sample).

## 7. What the rewrite does not do

- It does not introduce the CEO's name. The user did not supply it. The placeholder `[name]` is kept so the user fills it in. Adding a name would be an invention.
- It does not promise what the pilot did not measure. The 47% / 12 pounds / 94% claims are gone, not hedged.
- It does not hedge the things that *are* supported. "320 patients, one clinic, Boston, 90 days" is stated cleanly.
- It does not add a quote from a clinician we did not see. The pilot data reports what clinicians said; the rewrite attributes the report to the clinic's care team, not to a specific person.
- It does not introduce a "future plans" paragraph. The user's sample rejects grand closes. The closing question fits the voice.
