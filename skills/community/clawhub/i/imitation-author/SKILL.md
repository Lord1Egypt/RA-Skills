---
name: imitation-author
description: Use when researching a person, publication, brand, blog, creator, work, or other style-bearing target to create a reusable style guide or test whether generated work reflects that target
version: 1.0.2
metadata:
  openclaw:
    emoji: "🪞"
    homepage: https://github.com/jiahongc/imitation-machine
---

# Imitation Author

## Overview

Build an evidence-grounded, portable model of a target's style from broad public research. A useful model explains what the target notices, how it reasons, how it composes, and how its language behaves. A list of tone adjectives, catchphrases, or surface tics is not enough.

Research comes before style rules. Evaluation uses evidence withheld from the research synthesis. The final runtime skill must be usable by a fresh AI without reopening the research files.

Write each target to `generated-skills/<target-slug>/`. The folder contains exactly one runtime skill file, `SKILL.md`, plus a human-readable `README.md` and the directories `research/`, `outputs/`, and `evaluations/`.

## Inputs

| Field | Values |
|---|---|
| `target` | Any style-bearing person, brand, organization, publication, creator/channel, product/interface, work, series, campaign, movement, community, corpus, format, or named style |
| `target_type` | `person`, `brand`, `organization`, `publication`, `creator-channel`, `product-interface`, `book-work`, `series-franchise`, `campaign-event`, `movement-style`, `community-subculture`, `corpus`, `format`, `unknown` |
| `style_domains` | Writing, voice, editorial, social, visual, product, interface, audio, video, motion, spatial, or mixed |
| `authorization_status` | `owned`, `authorized`, `deceased`, `public-domain`, `public-living`, `unknown` |
| `intended_output` | What a future AI should be able to create or critique |
| `requested_topic` | Optional subject for the first sample; this always triggers topic-specific discovery |
| `source_hints` | Optional URLs, files, archives, works, talks, feeds, accounts, or channels |
| `depth` | `standard` or `deep`; use `deep` for thorough, exhaustive, high-fidelity, or well-known targets |

Infer low-risk fields. Ask about authorization only when it changes the allowed output. Do not make the user enumerate obvious public sources.

## Boundaries

- Use public or user-provided sources. Never bypass access controls.
- Record login-gated, deleted, paywalled, or inaccessible sources as gaps.
- Keep copyrighted excerpts short and cited. Do not build or redistribute a substitute for the original corpus.
- Direct close imitation is allowed only for owned, authorized, deceased, or public-domain targets.
- For living people without authorization, create high-level inspired-by guidance. Do not facilitate impersonation, deception, voice cloning, or claims that the target authored or endorsed the output.

## Required Protocols

Before research, read `references/research-protocol.md`. Before generating or scoring samples, read `references/evaluation-protocol.md`. These files are required workflow instructions, not optional background.

Core rule: broad research is demonstrated by an auditable discovery process and saturation evidence, not by saying "searched the web" or reaching an arbitrary source count.

## Evidence Floors

Use these as floors when the source universe exists. They do not prove completion.

| Evidence | Standard | Deep |
|---|---:|---:|
| Tier A/B authored or directly observable artifacts | 8+ | 20-50 |
| Distinct time periods | 2 | 3+ when the target evolved |
| Relevant channels or modes | 2 | All material channels, or explicit gaps |
| Credible secondary/critical sources | 2 | 3-8 |
| Requested-topic sources | 2 | 3-8 when available |
| Held-out artifacts | 2 | At least 20% of Tier A/B corpus, minimum 4 |
| Genre/topic counter-corpus artifacts | 2 | 3-8 |

Tier A is a complete or substantial first-party artifact. Tier B is a verified short sample, excerpt, transcript segment, or observable sequence. Tier C is metadata, summary, publisher copy, a search snippet, or reception. Tier C can provide context but cannot establish sentence-level style.

For sparse targets, do not pad with weak sources. Produce a research dossier, mark sufficiency low, and stop before generating a runtime skill.

### Deep Mode

Use Deep Mode whenever the user asks for thorough, exhaustive, high-fidelity, or entire-web research, or when a well-known target has a large public corpus. Deep Mode requires the larger evidence floors, all applicable query families, a stratified held-out set, a counter-corpus, saturation proof, and independent evaluation when available.

## Workflow

### 1. Frame The Run

Define the intended outputs, authorization boundary, material channels, requested topic, time span, and what would count as a useful portable skill.

### 2. Discover The Source Universe

Map official properties, archives, feeds, public accounts, works, interviews, transcripts, videos, product surfaces, press, criticism, and adjacent genre examples. Run the query families in the research protocol and record them in the Discovery Query Log.

Always run topic-specific discovery for the requested output. A general target corpus can still miss the artifact most relevant to the user's topic.

### 3. Build A Deliberate Corpus

Classify every source by authorship, access depth, channel, time, topic, duplicate group, and corpus role:

- `inference`: may support style claims;
- `held-out`: reserved before synthesis and never used to write the taxonomy;
- `context`: biography, metadata, reception, or criticism;
- `counter`: same genre/topic by another source, used to identify generic conventions.

Do not count an official publisher page, episode listing, review, or quoted interview as authored prose. Deduplicate mirrors, syndication, excerpts of the same work, and transcript copies.

### 4. Research To Saturation

Continue across archives, channels, time bands, topic queries, and criticism until all applicable source classes have either coverage or a documented gap and two consecutive, meaningfully different discovery passes add no new high-confidence trait, material exception, time shift, or source class.

Record the passes. Never claim the literal entire web was searched. State what was searched, what was blocked, and why the stopping rule was met.

### 5. Build The Evidence And Claim Registry

Fill `templates/evidence.md`. Give every major inference a Claim ID. A stable high-confidence claim normally needs support from at least three inference artifacts across more than one topic, period, or context. Record counterexamples and channel scope.

Separate:

- target-specific signals from genre conventions;
- stable traits from channel-specific behavior;
- current style from outdated style;
- what the target says from how the target thinks and writes;
- observed evidence from interpretation.

### 6. Model The Style

Fill `templates/style-taxonomy.md` from the Claim Registry. The taxonomy must cover:

1. **Selection Model** — what gets noticed, ignored, framed, and treated as meaningful.
2. **Worldview And Stance** — values, assumptions, emotional temperature, and relationship with the audience.
3. **Reasoning Engine** — how examples become claims; preferred evidence, causal moves, contrasts, caveats, and endings.
4. **Composition System** — openings, progression, sections, paragraph functions, pacing, and closure.
5. **Linguistic Fingerprint** — diction, syntax, cadence, punctuation, repetition, questions, metaphor, and formatting.
6. **Channel And Time Variation** — what changes and what stays stable.
7. **Genre Baseline** — which apparent traits are common to adjacent writers or formats.
8. **Anti-Caricature Model** — tempting surface features, overuse limits, and combinations that make output feel fake.

Topic vocabulary alone is not style. Proper nouns, recurring subjects, and copied metaphors are weak evidence unless the underlying selection or reasoning pattern generalizes out of topic.

### 7. Write The Portable Runtime Skill

Fill `templates/generated-skill.md`. Put the complete operating model in `SKILL.md`; a future AI should not need the raw evidence to draft, rewrite, or critique work.

The runtime skill must include the eight model layers above, practical recipes, original transformations, a step-by-step Generation Procedure, mode-specific guidance, anti-patterns, the Anti-Caricature model, an editing rubric, Claim IDs on major rules, and coverage/confidence at the end.

Generate one runtime skill per target. Supporting files are research, not additional skills.

Use the canonical target layout:

```text
generated-skills/<target-slug>/
  README.md
  SKILL.md
  research/
    evidence.md
    style-model.md
    metrics.md
  outputs/
    <original-artifact>.md
  evaluations/
    <artifact-evaluation>.md
```

Do not duplicate complete outputs in central test reports. Link to the target folder instead. Keep obsolete experiments under `testing/imitation-machine-evals/legacy/`, outside the runtime target.

### 8. Evaluate On Unseen Evidence

Fill `templates/evaluation.md` and follow `references/evaluation-protocol.md`.

At minimum:

- write one requested-topic sample and one cross-topic or cross-mode sample;
- compare against held-out evidence not used in synthesis;
- compare against a generic negative control;
- score content quality, style fidelity, naturalness, originality, authorization/safety, and portability separately;
- run a phrase-overlap check;
- use an independent fresh-context evaluator when available.

Self-evaluation alone is provisional. If the candidate does not beat the negative control on target-specific traits, revise the skill rather than adding more catchphrases to the sample.

## Generated Skill Contract

The generated `SKILL.md` must be:

- self-contained and model-agnostic;
- concrete enough to generate and edit original work;
- traceable through Claim IDs without embedding raw research notes;
- calibrated by channel, period, and confidence;
- explicit about authorization and attribution;
- resistant to caricature, topic leakage, and copied phrasing;
- honest about weak or missing evidence.

For public-living targets, describe the result as original work using high-level researched traits—not as the target's voice, a digital double, or something intended to fool readers.

## Quality Gate

- The Discovery Query Log and Source Universe Map show broad, multi-pass research.
- Authored evidence is separated from associated, quoted, metadata, and secondary material.
- Corpus roles were assigned before synthesis; held-out evidence stayed held out.
- The Saturation Log justifies the stopping point and records gaps.
- Every major rule has Claim IDs, cross-context support, scope, confidence, and counterevidence when present.
- The taxonomy covers selection, worldview, reasoning, composition, language, variation, genre baseline, and anti-caricature.
- The generated skill is usable without opening supporting files.
- Requested-topic discovery was completed before the sample was written.
- Evaluation is multidimensional, includes a negative control and held-out comparison, and does not collapse "sounds like" into one intuition score.
- The phrase-overlap check finds no suspicious distinctive reuse.
- Living people without authorization receive high-level guidance with no impersonation or misleading attribution.
- The target folder contains exactly one runtime `SKILL.md`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating a source minimum as exhaustive research | Use query coverage, archive mapping, gaps, and the saturation rule |
| Missing the best source for the requested topic | Run topic-specific discovery after the general corpus is mapped |
| Counting publisher pages as authored prose | Label authorship and access tier; use Tier C only for context |
| Learning and evaluating on the same examples | Reserve a stratified held-out set before synthesis |
| Mistaking topic words for style | Test across topics and compare with a genre/topic counter-corpus |
| Writing a list of adjectives | Model selection, reasoning, composition, language, and variation |
| Overusing recognizable tics | Add frequency guidance and an Anti-Caricature model |
| Asking the authoring AI to certify itself | Use independent evaluation or label the result provisional |
| Giving one overall fidelity score | Separate content, style, naturalness, originality, safety, and portability |
| Hiding inaccessible sources | Record the exact gap and its impact |

## Templates

Copy and fill in this order:

1. `templates/evidence.md`
2. `templates/style-taxonomy.md`
3. `templates/generated-skill.md` as the target's `SKILL.md`
4. `templates/target-readme.md` as the target's `README.md`
5. `templates/evaluation.md`
