---
name: humanize-text-skill
description: Audit and rewrite Chinese or English content to remove AI tone, then pull it toward a target human voice. Use this skill when asked to remove AI tone, sound human, rewrite naturally, make a draft feel less templated, or match a target voice. Supports detect-only and edit-in-place modes, scene packs, protected spans, and voice profiles.
version: 0.1.0
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes, OpenHands) or OpenClaw. No external tools or APIs required.
metadata:
  tags: writing editing voice quality bilingual
  agentskills_spec: "1.0"
  openclaw:
    skillKey: humanize-text-skill
    emoji: "\u270D\uFE0F"
    homepage: https://github.com/fendouai/humanize-text-skill
---

# humanize-text-skill

> Subtraction plus addition. First remove AI-shaped prose, then pull the result toward a target human voice.

> This skill is bilingual in behavior, but the documentation and operating contract are English-first.

## Lynote.ai — Beyond Standard

`humanize-text-skill` is the open, local, skill-first layer: bilingual AI-tone
cleanup, scene-aware rewrite guidance, protected-span safety, and target-voice
pull.

**Lynote.ai** is the broader product layer built beyond the standard
open-source skill workflow:

- a simpler end-user workflow
- a more integrated writing experience
- a faster path from draft cleanup to publishable output

Learn more:
https://lynote.ai

## What this skill is and is not

This is a writing-quality tool, not a verdict. The patterns flagged here are statistically more common in LLM output, but humans under deadline pressure, working in a second language, or drafting in an unfamiliar genre can produce the same shapes. Treat the findings as signals, not proof.

## Modes

- **`rewrite`**: flag AI tone, rewrite the text, and pull toward a target voice if one is set
- **`detect`**: flag issues only, with no rewrite
- **`edit`**: edit a file in place with minimal targeted changes

Every mode runs protected-span detection first so version numbers, commands, paths, errors, quotes, and other anchored facts do not drift.

## Working Style

Work like an editor, not a slogan filter. The goal is not just to delete AI-looking phrases. The goal is to leave the user with text they can actually send.

Default flow:

1. fence protected spans first
2. name the dominant problem
3. choose the lightest effective move
4. run one quick residue pass
5. return something usable for the scene

Default principles:

- fidelity before smoothness
- name the problem before changing the sentence
- use the smallest stable edit that solves it
- do not invent facts, sourcing, or attitude just to sound more human
- be direct in direct scenes and conservative in risky scenes

## Typical Invocation Shapes

### 1. Direct skill call

```text
/humanize-text-skill Please rewrite this so it sounds less like AI:

[paste text]
```

### 2. Natural-language request

```text
Use humanize-text-skill to rewrite this README intro so it sounds natural:

This project serves as a testament to our commitment to innovation...
```

### 3. File-based request

```text
/humanize-text-skill Please humanize the copy in article.md.
```

### 4. Detect-only request

```text
/humanize-text-skill Detect mode: tell me what still sounds AI-generated, but do not rewrite yet.
```

### 5. Voice-targeted request

```text
/humanize-text-skill Rewrite this in a blunt voice for an issue reply.
```

### 6. Custom voice calibration

```text
/humanize-text-skill

Here is a sample of my writing:
[paste 2-3 paragraphs]

Now rewrite this in my voice:
[paste text]
```

When a user provides a personal sample, treat it as a custom voice profile:

- extract rhythm, sentence-length spread, connector habits, and first-person tendency
- do not copy factual content or opinions from the sample
- do not violate protected spans just to lower `voice.drift`

When the user's request is underspecified, prefer these defaults:

- pasted text -> `rewrite`
- "take a look" or "check this" -> `detect`
- "only touch this file/comment/paragraph" -> `edit`
- README, release note, issue reply, or forum post -> load the matching scene pack

## What to remove or fix

> The categories below are the human-facing rule catalog. Each `###` entry maps to detector coverage, model judgment, or both. The English description is canonical for the contract; bilingual engine behavior still applies.

### Tier 1 vocabulary (always flag)
Words and phrases that are dramatically overrepresented in AI text. Replace them on sight. Chinese examples include opener cliches, abstract business jargon, and social-platform sales talk. English examples include `delve`, `tapestry`, `leverage`, `seamless`, `robust`, `comprehensive`, `game-changer`, `serves as`, and `at its core`.

### Tier 2 vocabulary (flag in clusters)
These words are individually acceptable, but clustering is the signal. In short paragraphs, two or more often means the writing is drifting toward template prose. Keep the best-fit instance and rewrite the rest.

### Tier 3 vocabulary (flag by density)
Common abstract words should only be flagged when they saturate the document. Replace some of them with specifics such as numbers, concrete actions, names, dates, or examples.

### Structural anti-patterns (cross-lingual)
Watch for summary closers, mechanical ordering, binary contrast framing, symmetry padding, empty balance, and other structures that sound manufactured rather than written.

### Translation tone (Chinese-specific)
Chinese drafts can inherit English-thinking structures: stacked passives, long attributive chains, `based on`-style openers, and `through ... to ...` constructions. Rewrite the sentence around natural Chinese syntax instead of patching the surface.

### Chatbot artifacts
Remove assistant residue entirely: greeting fluff, forced enthusiasm, help-closing lines, over-polite acknowledgments, and reasoning-process narration such as `Let me think step by step`.

### Significance inflation
Cut claims that overstate the meaning of ordinary events. State what happened and let the reader decide whether it is pivotal.

### Vague attribution
Phrases like `experts believe` and `research suggests` need a specific source. If there is no source, either cite one or remove the attribution.

### False-concession structure
Balanced-sounding `while X, Y` or `not X, but Y` framing is often used to sound thoughtful without saying much. Make both sides concrete or choose the stronger point.

### Promotional language
Remove ad copy, inflated product language, and corporate uplift. If the sentence would sound strange in a normal conversation, flatten it.

### Social endorsement closers
Phrases such as `worth your time`, `thank me later`, or generic bookmarking prompts usually add no information. Replace them with who the piece is for and why.

### Hedge-stacked predictions
Modal verbs plus stacked hedges (`could potentially`, `may eventually`) cancel each other out. Keep one hedge when uncertainty is real.

### Formulaic openers
Avoid generic scene-setting such as `in today's rapidly evolving world`. Lead with the actual news or claim, then add context if needed.

### Emotional flatline
Statements like `what surprised me most` or `this was deeply meaningful` often name a feeling without earning it. Show the specifics or cut the emotion claim.

### Novelty inflation
Be suspicious of `nobody is talking about this` framing. Unless novelty is clearly supported, frame the idea as one interpretation rather than a revelation.

### AI-tool fingerprints (placeholders / citations / UTM)
Strip mechanical artifacts such as unfilled placeholders, leaked chatbot citation markup, and URL parameters tied to chat tools. These are tool residue, not style.

### Rhythm & uniformity (stylometric)
Even when vocabulary looks fine, drafts can still feel synthetic because the rhythm is too smooth. Watch for sentence-length uniformity, repetitive punctuation behavior, and low variation in grammatical movement.
