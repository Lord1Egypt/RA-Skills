# Jane Street Puzzle Archivist

Repository-local skill for maintaining a long-lived Jane Street puzzle archive.

## Contents

- `SKILL.md` defines when and how to use the skill.
- `references/reference-repos.md` summarizes the three public reference repositories.
- `references/solving-patterns.md` captures recurring solving patterns worth reusing.
- `agents/openai.yaml` provides marketplace-facing metadata.

## Publish

```bash
clawhub publish .agents/skills/jane-street-puzzle-archivist \
  --slug jane-street-puzzle-archivist \
  --name "Jane Street Puzzle Archivist" \
  --version 0.1.0
```
