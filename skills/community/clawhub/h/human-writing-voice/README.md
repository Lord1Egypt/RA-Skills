# human-writing

Write and review public copy so it sounds like a person, not polished AI sludge.

`human-writing` is an OpenClaw skill for drafting, rewriting, and reviewing posts, scripts, threads, essays, and comments where voice matters. It targets the deeper structural tells of AI writing: neat arcs, spelled-out morals, over-designed emotion, tidy closure, generic stand-ins, philosopher-dialogue, and single clean storylines.

It is built around the practical lesson from StoryScope / Russell et al. (2026): even after removing surface cues like punctuation, sentence length, and obvious formula phrases, human vs AI stories were still distinguishable from the way the writing was built underneath.

## Use Cases

- rewrite a LinkedIn post without turning it into content marketing
- review a draft for structural AI tells
- preserve roughness, side threads, concrete nouns, and unresolved tension
- avoid formulaic contrast writing such as `it's not X, it's Y`
- keep the writer's actual cadence instead of smoothing everything flat

## What It Checks

- Does the piece explain the moral too loudly?
- Did it invent a tidy arc or tidy ending?
- Did it replace real nouns with generic stand-ins?
- Did it package emotion with fake sensory/body cues?
- Did it remove useful awkwardness, contradiction, or side mess?
- Does it read like generic LinkedIn, content marketing, or a polished AI explainer?

## Installation

### OpenClaw

```bash
openclaw skills install human-writing
```

Or clone manually:

```bash
git clone https://github.com/LeoStehlik/human-writing.git /path/to/your/skills/human-writing
```

### Codex / Claude Code

Copy this folder into your agent skills directory.

## Usage

```text
Review this draft with human-writing.
```

```text
Rewrite this post so it keeps my voice and removes AI tells.
```

```text
Check this LinkedIn draft for structural AI smell.
```

## What's Inside

```text
human-writing/
├── SKILL.md
└── references/
    └── storyscope-tells.md
```

## License

MIT - see [LICENSE](LICENSE)
