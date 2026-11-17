<div align="center">

# humanize-text-skill

### Make AI-written text sound human, not just less AI.

**Bilingual zh/en engine · zero dependencies · detector + rewrite skill + voice pull**

</div>

`humanize-text-skill` is a bilingual writing skill for removing AI-shaped prose and pulling the result toward a target human voice.

It does two jobs:

- **Subtraction**: remove AI-shaped vocabulary, structure, rhythm, and chatbot residue.
- **Addition**: pull the cleaned text toward a target voice such as `casual`, `professional`, or `technical`.

Unlike simple AI-writing detectors, this project is built as a full skill:

- it detects issues
- it decides what is safe to rewrite
- it protects facts, commands, paths, and quoted text
- it shapes the final output for scenes like README intros, release notes, issue replies, and status updates

## At A Glance

![humanize-text-skill capability map](./docs/capability-map.svg)

## Why It Exists

Most tools stop at "less AI." `humanize-text-skill` aims for "sounds like a real person wrote this."

Common targets:

- Chinese filler and black-box jargon such as `值得注意的是`, `赋能`, `闭环`, and `综上所述`
- English AI staples such as `delve into`, `seamless`, `serves as a testament`, and `Let's dive in`
- over-even sentence rhythm
- false significance and vague authority claims
- pasted chatbot residue

## What It Can Do

- Detect 50 executable issue types across Chinese and English.
- Keep the same concept mapped to the same detector type across both languages where symmetry is intended.
- Route behavior by scene: `chat`, `status`, `docs`, `public-writing`.
- Support three modes: `rewrite`, `detect`, `edit`.
- Protect spans that must not drift: numbers, commands, paths, versions, names, logs, and quotes.
- Compute `voice.drift` separately from `score`, with concrete pull suggestions.
- Document **17 pattern categories** in the skill contract.
- Lock examples and engine behavior with `143 CI checks`.

## Quick Example

```bash
node -e "const H=require('./detector/patterns.js'); console.log(H.analyzeText('值得注意的是，我们打造了一套赋能开发者社区的方案，助力企业实现降本增效闭环。综上所述，未来可期！').score)"
```

```bash
# expected: 55
```

```bash
node -e "const H=require('./detector/patterns.js'); console.log(H.analyzeText('今天把连接池上限从 20 调到 100，504 先压下来了。观察 24 小时，错误率 0.1% 以下就全量。').score)"
```

```bash
# expected: 0
```

## Validation Snapshot

Current locked examples:

- AI-heavy zh sample: `score = 55`
- human technical zh sample: `score = 0`
- formal text against `casual` voice target: `voice.drift = 71`
- current test suite: `143 CI checks`

## Install And Use

```bash
git clone https://github.com/fendouai/humanize-text-skill.git
cd humanize-text-skill
npm test
```

This repository is usually used as a skill package inside an agent runtime.

- Claude Code: copy `SKILL.md`, `references/`, and `policy/` into `.claude/skills/humanize-text-skill/`
- Cursor: use [`cursor-rules/humanize-text-skill.mdc`](./cursor-rules/humanize-text-skill.mdc)
- Codex / OpenClaw / Hermes: point the tool at the repo root

### ClawHub publish readiness

This repository is prepared for ClawHub upload:

- canonical entry file: `SKILL.md`
- runtime support files: `detector/`, `references/`, `policy/`
- publish filter: [`.clawhubignore`](./.clawhubignore)

Suggested publish command:

```bash
clawhub skill publish . \
  --slug humanize-text-skill \
  --name "humanize-text-skill" \
  --version 0.1.0
```

`policy/` is a required runtime dependency. If you install the skill manually
and omit that directory, `voiceMode` will fail.

### Install health check

```bash
node -e "const H=require('./detector/patterns.js'); const r=H.analyzeText('值得注意的是，我们打造了一套方案。', { voiceMode: 'casual' }); console.log({ score: r.score, hasVoice: !!r.voice, drift: r.voice && r.voice.drift });"
```

Expected:

- `score` is greater than `0`
- `hasVoice` is `true`
- `drift` is a number

## Common Usage Patterns

In tools like Claude Code, Codex, or other skill-aware agents, people usually use `humanize-text-skill` in one of these ways.

### 1. Direct skill call

```text
/humanize-text-skill Please rewrite this so it sounds less like AI:

[paste text]
```

### 2. Natural-language request

```text
Use humanize-text-skill to rewrite this so it sounds more natural:

This project serves as a testament to our team's commitment to innovation.
Moreover, it showcases our pivotal role in the evolving technology landscape.
```

### 3. File-based request

```text
/humanize-text-skill Please humanize the copy in article.md.
```

### 4. Detect before rewrite

```text
/humanize-text-skill Detect mode: show me what still sounds AI-written, but don't rewrite yet.
```

### 5. Target a voice or scene

```text
/humanize-text-skill Rewrite this in a blunt voice for an issue reply.
```

```text
/humanize-text-skill Rewrite this README intro in a technical voice.
```

Practical defaults:

- pasted text usually means `rewrite`
- "check this first" usually means `detect`
- "only touch this file/comment/paragraph" usually means `edit`
- README, release note, forum post, and issue reply requests automatically benefit from scene-pack behavior

## Voice Calibration

If you want the rewrite to sound more like you, provide a short sample of your own writing and use `voiceMode: custom`.

```text
/humanize-text-skill

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now rewrite this in my voice:
[paste draft]
```

What the skill uses from the sample:

- sentence length and rhythm
- connector preferences
- first-person tendency
- a measurable voice profile, not private identity traits

What it does not do:

- it does not copy your facts or opinions from the sample
- it does not override protected spans
- it does not try to impersonate a real person beyond observable writing style

## Engine API

```js
const HumanizeTextSkill = require("./detector/patterns.js");

const result = HumanizeTextSkill.analyzeText("your text", {
  contextMode: "general",
  sceneMode: "docs",
  voiceMode: "casual",
  sample: "optional sample",
});

console.log(result.score);
console.log(result.issues);
console.log(result.voice?.drift);
console.log(result.voice?.suggestions);
```

Important:

- `score` is the only engine score.
- `voice.drift` is a separate dimension.
- `fidelity` is currently enforced in the rule layer, not returned as an engine field.

## Skill Runtime

![humanize-text-skill skill architecture](./docs/skill-architecture.svg)

The detector is only one layer. The full skill runtime is:

1. choose mode: `rewrite`, `detect`, or `edit`
2. judge scene and scope
3. protect spans that must not drift
4. run detector and voice analysis
5. choose action: rewrite, audit-only, or minimal edit
6. run a second-pass residue audit
7. return output in a scene-appropriate shape

See [references/skill-architecture.md](./references/skill-architecture.md) for the full map.

## Repository Map

- [SKILL.md](./SKILL.md): top-level skill contract
- [detector/](./detector/): executable detector and voice engine
- [references/](./references/): human-readable rules, scene packs, examples, checklists
- [policy/](./policy/): auditable scene/tier/voice policy in TOML
- [evals/](./evals/): benchmark cases, fixtures, voice samples

Good entry points:

- [references/scene-packs.md](./references/scene-packs.md)
- [references/examples.md](./references/examples.md)
- [references/quick-checklist.md](./references/quick-checklist.md)
- [references/voice-contract.md](./references/voice-contract.md)

## Related Work

`humanize-text-skill` builds on ideas and assets from:

- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
- [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua)
