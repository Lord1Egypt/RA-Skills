# Runtime Chain

The runtime chain defines the execution order for each runtime mode. The skill uses the lightest sufficient chain; the full chain only runs when Full Narrative Mode is selected.

## Universal Language Lock

Before any runtime mode is selected:

```text
1. Detect latest user instruction language
2. Set language_lock.locked_language
3. Carry language_lock through all downstream modules
4. Run Output Language Lock Harness before final delivery
```

Priority: `language lock > runtime mode > style > audience adaptation > notes language`. The latest user instruction language controls the final output unless the user explicitly requests another language.

## Step 0: Select Runtime Mode

Before running any mapper, select the lightest sufficient runtime mode. Available modes:

```text
1. Quick Message
2. One-on-One Strategy
3. Public Narrative
4. Expert Translation
5. Rewrite Recovery
6. Personal Communication
7. Full Narrative
```

For mode selection rules, runtime chains, and harness lists, see `selectors/runtime_mode_selector.md`.

### Core Rule

Do not run the full chain by default. Use the lightest sufficient chain.

## Mode-Specific Runtime

### Quick Message Mode

```text
Conversation Purpose
→ Relationship Context
→ Listener Hook
→ Minimum Next Action
→ Light Surface Check
→ Output
```

### One-on-One Strategy Mode

```text
Conversation Purpose
→ Relationship Context
→ Recipient Motivation
→ Collaboration / Ask Hypothesis
→ Attraction Filter
→ Narrative Authority
→ Claim Boundary
→ Message / Talking Points
→ Harness
→ Output
```

### Public Narrative Mode

```text
Story Kernel
→ Narrative Authority
→ Value / Stakes
→ Action-Reaction-Gap
→ Controlling Idea
→ Audience Cognition
→ Affective Arc
→ Narrative Entropy
→ Renderer
→ Harness
→ Output
```

### Expert Translation Mode

```text
Claim Boundary
→ Audience Cognition
→ Audience Entropy Tolerance
→ Low-Entropy Ground
→ High-Entropy Turn
→ Mechanism Explanation
→ Surface Naturalness
→ Output
```

### Rewrite Recovery Mode

```text
User Feedback
→ Failure Layer Diagnosis
→ Reroute to Correct Mode
→ Rewrite
→ Output
```

### Personal Communication Mode

```text
Apply Universal Language Lock
→ Map Personal Context
→ Preserve User Personality
→ Choose Low-Pressure Scene
→ Draft Sendable Message
→ Run Personal Communication Harness
→ Run Output Language Lock Harness
→ Output Message + Short Notes
```

### Full Narrative Mode

Use only for complex, high-stakes long-form narrative work. Steps in §"Full Narrative Mode Steps" below.

## Harness Selection

Do not run every harness for every task. Select by mode:

| Mode | Harnesses |
| --- | --- |
| Quick Message | `conversation_outcome_harness` if relevant; `non_offensive_personality_harness` if tone is sharp; `surface_naturalness_harness` |
| One-on-One Strategy | `conversation_outcome_harness`, `non_offensive_personality_harness`, `claim_harness`, `source_fidelity_harness`, `surface_naturalness_harness` |
| Public Narrative | `claim_harness`, `source_fidelity_harness`, `narrative_authority_harness`, `story_harness`, `emotional_resonance_harness`, `narrative_entropy_harness`, `surface_naturalness_harness` |
| Expert Translation | `claim_harness`, `source_fidelity_harness`, `audience_harness`, `narrative_entropy_harness`, `surface_naturalness_harness` |
| Rewrite Recovery | Run the harness corresponding to the diagnosed failure layer. |
| Personal Communication | `personal_communication_harness`, `output_language_lock_harness`, `surface_naturalness_harness` |
| Full Narrative | `claim_harness`, `source_fidelity_harness`, `narrative_authority_harness`, `story_harness`, `value_stakes_harness`, `gap_harness`, `controlling_idea_harness`, `audience_harness`, `emotional_resonance_harness`, `narrative_entropy_harness`, `surface_naturalness_harness` |

Run Full Narrative harnesses in this priority order; compressed checks are allowed internally. If any harness fails, return to the appropriate upstream step — patch-level fixes compound over multiple edits.

## Full Narrative Mode Steps

The canonical reference for the full pipeline. Run only when Full Narrative Mode is selected.

### Step 1: Parse Material

```text
source type
user request
output format
target audience
known facts
missing facts
```

### Step 2: Extract Claim Boundary

```text
explicit facts
reasonable interpretation
assumptions
uncertain claims
forbidden claims
```

See `mappers/claim_boundary_extractor.md`.

### Step 3: Build Story Kernel

```text
narrative object
protagonist
desire
old world
obstacle
action
world reaction
gap
turning point
transformation
```

See `mappers/story_kernel_builder.md`.

### Step 4: Map Narrative Authority

```text
story owner
author position
central judgment
old world error
opposing force
non-negotiable truth
adaptation boundary
```

See `mappers/narrative_authority_mapper.md`.

### Step 5: Identify Value / Stakes

```text
value sought
value at risk
cost of failure
opportunity if success
urgency
reversibility
```

See `principles/value_stakes.md`.

### Step 6: Build Action-Reaction-Gap

```text
desire
action
expected reaction
actual reaction
gap
new information
value shift
next action
```

See `principles/action_reaction_gap.md`.

### Step 7: Build Controlling Idea

```text
value statement
cause statement
full controlling idea
proof path
```

See `principles/controlling_idea.md`.

### Step 8: Map Audience Cognition

```text
knowledge floor
likely misunderstanding
practical concern
trust barrier
terminology budget
desired belief shift
```

Audience adaptation must not override Narrative Authority. See `mappers/audience_cognition_mapper.md`, `selectors/audience_entry_point_selector.md`, `policies/audience_visibility_policy.md`.

### Step 9: Map Affective Arc

```text
initial emotion
emotion source
tension
recognition
resolution
final emotion
emotional temperature
```

Emotion must come from protagonist pressure, not decorative language. See `mappers/affective_arc_mapper.md`.

### Step 10: Map Narrative Entropy

```text
audience entropy tolerance
low entropy ground
high entropy turn
surprise point
cognitive load risk
pacing plan
resolution point
```

See `mappers/narrative_entropy_mapper.md`, `principles/narrative_entropy.md`.

### Step 11: Select Audience Entry Point

Choose one: `risk-first`, `pain-first`, `scene-first`, `mechanism-first`, `contrast-first`.

### Step 12: Render with Style

Style must obey: claim boundary, source fidelity, narrative authority, audience cognition, affective arc, output contract. See `renderers/main_renderer.md`, `renderers/wrappers/`.

### Step 13: Final Output

Default: only output final user-facing content. Do not show Story Kernel, Narrative Authority Map, Affective Arc, Harness results, internal runtime chain — unless the user explicitly asks for analysis or debugging.

## Audience Visibility

Audience mapping and affective arc are hidden by default. Show brief framing only when: the user asks for audience-specific output, critiques comprehensibility, the target audience strongly affects the explanation, or the user is testing the skill. See `policies/audience_visibility_policy.md`.

## Artifact Delivery Branch

Use this branch when the user asks for a reusable artifact (README, GitHub README, open-source docs, email, message, proposal, deck copy, landing page, social post, script, speech, press release, job description, bio, API docs, package documentation).

### Runtime Order

```text
1. Detect Artifact Type
2. Detect Output Language
3. Preserve User Terms
4. Select Artifact Contract
5. Extract Claim Boundary
6. Render Artifact
7. Run Artifact Contract
8. Run Language Match Harness
9. Run User Term Fidelity Harness
10. Run Artifact Delivery Harness
11. Run Markdown / Format Cleanliness Check
12. Final Output
```

### Priority

```text
1. Artifact Contract
2. Language Match
3. User Term Fidelity
4. Claim Boundary
5. Format Cleanliness
6. Audience Fit
7. Narrative Quality
8. Style
```

Narrative style must not override artifact correctness.

### GitHub / README Special Rule

If the artifact type is GitHub README, README.md, open-source docs, developer documentation, package README, or skill README, run: `github_readme_output_contract`, `language_match_harness`, `user_term_fidelity_harness`, `artifact_delivery_harness`, `markdown_cleanliness_harness`.

### False Claim Prevention

Do not invent: install commands, package availability, GitHub name availability, npm / PyPI / ClawHub status, official integrations, license status, runtime requirements, API requirements, benchmark results, production readiness. Use placeholders when unknown.

### Interaction With Other Modes

Artifact Delivery Branch combines with other modes: GitHub README → Artifact Delivery + Expert Translation / Public Narrative; email → Artifact Delivery + One-on-One Strategy; social post → Artifact Delivery + Public Narrative; technical docs → Artifact Delivery + Expert Translation. Artifact discipline always applies last.

## High-Profile Recipient Branch

Triggers: sell to / pitch to / message / reach out to / convince a high-profile recipient (public figure, major CEO, investor, senior academic, regulator, institutional leader, well-known expert, celebrity, well-known technical leader, artist, creator, performer, designer, persona-based professional).

Runtime:

```text
1. Detect High-Profile Recipient
2. Map Recipient Power Context
3. Extract Claim Boundary
4. Map Conversation Purpose
5. Map Narrative Authority
6. Build Proof-Oriented Pitch
7. Render Short Pitch
8. Run High-Profile Recipient Harness
9. Run Proof Challenge Harness
10. Run Source Fidelity Harness
11. Run Surface Naturalness Harness
12. Output Pitch
```

### Notes Rule

Do not include private notes in the default output. If the user explicitly asks for reasoning, analysis, or behind-the-scenes explanation, add notes clearly separated: `Notes for you, not for the pitch:`. Otherwise, output the pitch only.

### Priority

```text
1. claim boundary
2. recipient discipline
3. proof challenge
4. small ask
5. narrative authority
6. emotional force
7. style
```

Offer a small proof challenge.

## Personal Communication Mode

Triggers: introduce me to someone, help me text a girl / guy / person I like, ask someone out, recover from awkwardness, I am shy / geeky / awkward, I might not talk well, write a message to someone I like.

### Priority

```text
1. language lock
2. personal safety and naturalness
3. authenticity
4. low-pressure next step
5. sendability
6. emotional reassurance
7. style
```

### Output Shape

```text
Short framing
Sendable message
Why it works
Notes for you, not for them
```

For very short tasks, output only the sendable message and one note.

## Known Context Recovery Branch

Triggers: known project / skill / product name, known internal architecture, known workspace directory, previously discussed initiative.

Runtime:

```text
1. Detect Known Entity
2. Recover Context
3. Determine Sufficient Context
4. Preserve Known Boundaries
5. Identify Unknowns
6. Continue to Requested Runtime Mode
7. Mark Assumptions / Placeholders
8. Produce Output
```

### Clarification Rule

Ask only if context is missing, contradictory, affects public claim safety, or when installation / license / deployment details are required and unknown. When asking, ask one high-leverage question only.

### Language Rule

Known Context Recovery does not change output language. If the user asks in English, output in English.

### Output Rule

Do not expose memory search details or internal recovery process unless the user asks for debugging. A short assumption note is allowed: "Drafted based on available project context. Installation and license details are marked as placeholders."

### Interaction with Artifact Delivery

For GitHub README or public artifact: `Known Context Recovery → Public Release Artifact Branch → Artifact Delivery Branch → Final Output`. Do not ask basic identity questions if the recovered context is sufficient.

## Public Release Artifact Branch

Triggers: publish to GitHub, launch, public README, open-source repo, website copy, landing page, marketplace listing, public announcement, release note.

Runtime:

```text
1. Detect Public Release Intent
2. Map Public Positioning
3. Check Naming / Third-Party Reference Risk
4. Select Public Artifact Contract
5. Detect Output Language
6. Preserve User Terms
7. Extract Claim Boundary
8. Render Public Artifact
9. Run Public Release Harness
10. Run Language Match Harness
11. Run User Term Fidelity Harness
12. Run Markdown Cleanliness Harness
13. Final Output
```

### Priority

```text
1. public positioning
2. naming safety
3. language match
4. artifact structure
5. claim boundary
6. format cleanliness
7. narrative quality
8. style
```

## Public Artifact Finalization Branch

Triggers: GitHub README, public README, open-source docs, launch copy, landing page, marketplace listing, public product page, public skill description.

Runtime:

```text
1. Detect Public Artifact
2. Map Public Artifact Audience
3. Check Public Name / Third-Party Risk
4. Apply Public Artifact Release Contract
5. Run Public Release Harness
6. Run Markdown Cleanliness Harness
7. Run Public Artifact Final Pass Harness
8. Run Human Release Voice Harness
9. Separate Artifact from Notes
10. Final Output
```

### Human Voice Priority

Human voice must improve memorability without violating: language match, claim boundary, markdown cleanliness, public naming safety, artifact structure.

### README Release Cleanup Step

For README artifacts, add a final cleanup step:

```text
1. Detect Public Artifact
2. Map Public Artifact Audience
3. Check Public Name / Third-Party Risk
4. Apply Public Artifact Release Contract
5. Run Public Release Harness
6. Run Markdown Cleanliness Harness
7. Run Public Artifact Final Pass Harness
8. Run Human Release Voice Harness
9. Run Public README Release Cleanup Harness
10. Separate Artifact from Notes
11. Final Output
```

Release cleanup priority: publishable artifact cleanliness, language and notes separation, path correctness, public link safety, license/install placeholder safety, claim boundary wording, voice polish. Do not let voice polish reintroduce unverified claims or messy formatting.

### Priority

```text
1. Public usability
2. Naming / affiliation safety
3. Language match
4. Markdown cleanliness
5. Claim boundary
6. Usage examples
7. Architecture clarity
8. Narrative quality
```

### Public README Rule

Do not start with internal architecture. If the first screen contains file tree, harness list, mapper list, or development history, rewrite. Notes for the maintainer go outside the artifact.

### Notes Separation Rule

If there are maintainer notes, naming caveats, or publishing reminders, place them outside the artifact under `Notes for you, not for publication:`. The publishable artifact must be clean on its own.

## Output Contract for Short Explanations

When output < 500 Chinese characters and audience is non-technical:

- No internal reasoning
- No Story Kernel
- No bullet lists unless requested
- Max one analogy
- Start from audience entry point
- End with practical value

See `contracts/short_explanation_output_contract.md`.
