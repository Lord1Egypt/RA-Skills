---
name: lineage-mini
version: 0.1.3
description: "Behavioral adaptation for AI agents. Builds a lightweight user profile from interaction history and adapts response style, topic focus, timing, and recovery when replies stop landing."
user-invocable: true
metadata: {"openclaw": {"emoji": "🧬", "requires": {"bins": ["node"]}}}
---

# Lineage Code Mini — Behavioral Adaptation Skill

You have access to `lineage-code-mini`, a behavioral adaptation engine. It learns how each user likes to be talked to and adapts your responses accordingly.

## Links

- GitHub source: https://github.com/PabloTheThinker/lineage-code-mini
- npm package: https://www.npmjs.com/package/lineage-code-mini
- ClawHub listing: https://clawhub.ai/pablothethinker/lineage-mini

## How It Works

1. **Record** — after each conversation, record whether the user engaged positively
2. **Compactify** — compress interaction history into a behavioral profile
3. **Adapt** — inject the profile into your system prompt before responding

## Commands

### `/lineage` or `/profile` — View a user's behavioral profile

Run the adaptation pipeline on the current user's conversation history:

```bash
node --input-type=module -e "
import { compactify, DEFAULT_CONFIG } from 'lineage-code-mini';
import { existsSync, readFileSync } from 'node:fs';
const historyPath = '{baseDir}/data/interactions.json';
const history = existsSync(historyPath) ? JSON.parse(readFileSync(historyPath, 'utf8')) : [];
const profile = compactify('current-user', history, DEFAULT_CONFIG);
console.log(JSON.stringify(profile, null, 2));
"
```

### `/adapt` — Generate behavioral hints for the current user

```bash
node --input-type=module -e "
import { pipeline } from 'lineage-code-mini';
import { existsSync, readFileSync } from 'node:fs';
const historyPath = '{baseDir}/data/interactions.json';
const history = existsSync(historyPath) ? JSON.parse(readFileSync(historyPath, 'utf8')) : [];
const basePrompt = 'You are a helpful AI assistant.';
const { context, profile } = pipeline('current-user', history, basePrompt);
console.log('Active patterns:', context.active_patterns);
console.log('Fitness:', context.fitness);
console.log('Personalized:', context.personalized);
console.log('---');
console.log(context.prompt);
"
```

## Automatic Adaptation

This skill provides the commands and storage layout. Your host agent still needs to call these commands or wire recording into its turn loop. Installation alone does not automatically capture conversations.

When this skill is loaded, you should:

1. **Before each response**, check if a user profile exists at `{baseDir}/data/profiles/`. If it does, read it and apply the behavioral hints to your response style.

2. **After each conversation turn**, record the interaction:
   - Was the user's response positive/engaged? (replied, followed up, said thanks, acted on suggestion) → `accepted: true`
   - Was it negative/disengaged? (ignored, changed topic, expressed frustration, no reply) → `accepted: false`

3. **Every 10 interactions**, run compactification to update the profile.

## Profile Fields

| Field | What it means |
|---|---|
| `preferred_style` | "direct" / "detailed" / "casual" / "formal" — how to frame responses |
| `strong_topics` | Topics user engages with — lean into these |
| `weak_topics` | Topics user ignores — avoid leading with these |
| `acceptance_rate` | 0-1 — how often your responses land |
| `fitness` | 0-1 — how well you're serving this user. Below 0.35 = change approach |
| `productive_hour` | Hour of day user is most engaged |
| `channel_distribution` | Which channels user talks on most |

## SOUL.md Integration

Generate a section for your SOUL.md or USER.md:

```bash
node --input-type=module -e "
import { compactify, asSoulPatch, DEFAULT_CONFIG } from 'lineage-code-mini';
import { existsSync, readFileSync } from 'node:fs';
const historyPath = '{baseDir}/data/interactions.json';
const history = existsSync(historyPath) ? JSON.parse(readFileSync(historyPath, 'utf8')) : [];
const profile = compactify('current-user', history, DEFAULT_CONFIG);
console.log(asSoulPatch(profile));
"
```

Append the output to your USER.md for persistent behavioral adaptation.

## Data Storage

Interaction history is stored at `{baseDir}/data/interactions.json`. Profiles are stored at `{baseDir}/data/profiles/`. These are plain JSON files — portable, inspectable, no database required.

## Installation

```bash
npx clawhub@latest install lineage-mini
```

Or manually: copy this `skill/` directory into your `~/.openclaw/skills/lineage-mini/`.
