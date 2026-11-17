# Audience, cognition, and author persona

This document adds the reader-strategy layer before the rewrite. It answers four questions:

1. Who is this text really for?
2. What do those readers already know?
3. What new cognition does this piece add?
4. What author persona should carry the piece?

The goal is not marketing decoration. The goal is to make the rewrite useful to a real reader instead of merely smoother.

## When to use this pass

Use it for:

- essays, posts, newsletters, explainers, product copy, landing pages, README prose, speeches, long social posts, and thought-leadership drafts
- any request that mentions audience, user profile, persona, positioning, conversion, cognition, insight, or "who is this for"
- publication-ready mode

Keep it implicit for:

- short transactional replies
- private messages
- tiny grammar/style edits
- reference, legal, medical, or encyclopedic prose where author persona should stay minimal

## 1. Target reader

Infer the target reader from:

- topic and promised outcome
- domain vocabulary and assumed knowledge
- examples and objections in the draft
- target surface: tweet, email, blog, README, landing page, investor note, product doc
- distribution channel: search, newsletter, community post, internal doc, social feed

Produce a compact reader profile:

```text
target_reader:
  role:
  situation:
  pain_or_question:
  desired_outcome:
  objections:
  vocabulary:
  reading_context:
```

Avoid fake demographic detail. "B2B SaaS founder deciding whether to add AI support chat" is useful. "32-year-old named Alex who drinks coffee" is not.

## 2. Cognitive starting point

The cognitive starting point is what the reader likely already knows before the article begins.

Find it from:

- user-supplied notes, comments, customer calls, search terms, or sales objections
- web search results and People Also Ask style questions
- competitor pages and docs
- GitHub issues, forums, Reddit/Hacker News/Product Hunt threads, support docs, reviews, social posts
- beginner guides and expert explainers in the domain

Search when:

- the user explicitly asks to search
- the topic is current, product/market-facing, technical, medical, legal, financial, or otherwise likely to change
- the draft makes assumptions about what users know
- you need to distinguish beginner knowledge from expert knowledge

When search is unavailable, label the result as inference.

Use this shape:

```text
starting_point:
  already_knows:
  likely_misunderstands:
  questions_they_are_asking:
  language_they_use:
  evidence:
```

Do not over-teach what the reader already knows. Do not skip the bridge they need.

## 3. New cognition

New cognition is the mental upgrade the text gives the reader. It can be:

- a sharper distinction
- a decision rule
- a mechanism
- a workflow
- a surprising constraint
- a risk the reader had not named
- an evidence synthesis
- a before/after framing
- a practical next step

Use this test:

```text
After reading, the reader can now say:
"I used to think <old model>. Now I understand <new model>, so I can <new action>."
```

If the draft has no new cognition, do not simply polish it. Flag the gap:

```text
new_cognition_gap:
  the draft mostly repeats what the reader already knows
  missing: <distinction / evidence / mechanism / decision rule / example>
```

Then either ask the user for the missing material or rewrite the piece as a clearer summary rather than pretending it has insight.

## 4. Author persona

Prefer the user's real voice when samples exist. If no sample exists, choose a concrete editorial persona. A persona is a writing posture, not a fake biography.

A persona may shape:

- level of directness
- sentence rhythm
- tolerance for caveats
- examples and analogies
- amount of warmth
- degree of opinion
- how the author handles uncertainty

A persona must not invent:

- personal experience
- credentials
- employment history
- customer stories
- emotional stakes
- relationships
- access to private data

## Built-in personas

Use these as starting points and adapt lightly to the target surface.

### 1. The field-note operator

- **Best for**: product lessons, startup posts, operational writing, build-in-public notes.
- **Posture**: has shipped things, cares about what broke, avoids grand theory.
- **Style**: concrete, direct, slightly compressed; uses "what changed", "what failed", "what I would do next".
- **Avoid**: fake war stories or invented metrics.

### 2. The skeptical technical editor

- **Best for**: technical docs, README prose, tool comparisons, engineering explanations.
- **Posture**: precise, allergic to hype, willing to say "this depends".
- **Style**: short definitions, clear boundaries, examples before claims.
- **Avoid**: snark, superiority, or over-explaining basics to expert readers.

### 3. The practical teacher

- **Best for**: tutorials, explainers, onboarding content, beginner-to-intermediate posts.
- **Posture**: patient but not patronizing.
- **Style**: starts from what the reader already knows, then adds one new distinction at a time.
- **Avoid**: classroom filler and "let's dive in" energy.

### 4. The product strategist

- **Best for**: landing pages, positioning docs, product narratives, feature announcements.
- **Posture**: connects user pain to product behavior and market context.
- **Style**: benefit-led, concrete, constraint-aware; names the trade-off.
- **Avoid**: vague value props, "seamless", "unlock", "revolutionary".

### 5. The research translator

- **Best for**: research summaries, health/science/AI papers, evidence-heavy explainers.
- **Posture**: careful, citation-minded, comfortable with uncertainty.
- **Style**: claim, evidence, limitation, implication.
- **Avoid**: overstating causal claims or turning weak evidence into advice.

### 6. The community insider

- **Best for**: social posts, community updates, creator notes, open-source announcements.
- **Posture**: speaks from inside the community, knows the shared frustrations.
- **Style**: warm, concise, lightly opinionated; uses community vocabulary.
- **Avoid**: pretending to belong to a community without evidence from the user.

### 7. The executive memo writer

- **Best for**: internal strategy notes, investor updates, leadership memos.
- **Posture**: decision-oriented, clear about trade-offs and next steps.
- **Style**: concise, structured, direct; names risks and owners.
- **Avoid**: motivational language and excessive narrative.

### 8. The calm critic

- **Best for**: opinion pieces, reviews, contrarian posts, critique-heavy essays.
- **Posture**: has a position, but argues from reasons instead of outrage.
- **Style**: plainspoken, restrained, uses contrast and counterexample.
- **Avoid**: dunking, vague cynicism, or fake certainty.

## Persona selection rule

Choose the persona that best matches:

```text
persona_fit:
  reader_need:
  surface:
  content_value:
  evidence_level:
  user's_voice_if_available:
```

When the user's real voice conflicts with a built-in persona, the user's voice wins. The persona should make the piece easier to aim, not overwrite the author.

## How this changes the rewrite

The rewrite should reflect the four-part analysis:

- Target reader controls what gets explained and what gets skipped.
- Cognitive starting point controls the opening and examples.
- New cognition controls the article's spine.
- Author persona controls posture, rhythm, and stance.

If the text still reads like it could be for anyone, the pass failed.

## Compact report shape

When the user asks for process or when publication-ready mode is used, include:

```text
Audience/Cognition:
- Target reader:
- Starting point:
- New cognition:
- Author persona:
- Remaining gap:
```

Keep this report short. The rewritten text is still the deliverable.
