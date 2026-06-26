# Michael Polanyi Skill Package

This directory is the runtime package for the Michael Polanyi skill.
It contains only the files Claude should use at runtime to produce grounded, practitioner-style judgment.

## Runtime files

| File | Role |
| --- | --- |
| `SKILL.md` | Trigger contract, response contract, and routing entrypoint |
| `examples.md` | High-value before/after examples that teach output shape |
| `polanyi-notes.md` | Conceptual grounding for tacit knowledge and practitioner judgment |
| `references/` | Deeper anti-pattern, quality-check, and response-pattern material |
| `scripts/detect_fluff.py` | Lightweight helper for checking generic AI language drift |

## Installed surface

When copied into `~/.claude/skills/michael-polanyi/`, the installed package should look like this:

```text
michael-polanyi/
  SKILL.md
  examples.md
  polanyi-notes.md
  references/
  scripts/
```

## Editing guidance

Change these files based on intent:

- edit `SKILL.md` when changing trigger logic or the minimum response contract
- edit `examples.md` when changing the target response shape
- edit `polanyi-notes.md` when changing conceptual grounding
- edit `references/` when moving long explanations out of `SKILL.md`
- edit `scripts/detect_fluff.py` only when changing the lightweight runtime quality helper

## Not part of the runtime package

Maintainer-only evaluation and review tooling lives at the repository root under `../../workbench/`.
That tooling supports iteration on the skill, but it is not part of the runtime package contract.
