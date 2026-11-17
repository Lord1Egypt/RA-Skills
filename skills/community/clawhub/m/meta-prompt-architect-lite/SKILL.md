---
name: meta-prompt-architect-lite
description: Turn a plain-language task description into a minimal prompt template — extracts {{variable}} placeholders, detects output format, assembles a ROLE/TASK/INPUT/CONSTRAINTS/OUTPUT scaffold. Use when the user asks to write or templatize a prompt for an LLM.
---

# Meta-Prompt Architect (Lite)

`scripts/generate.mjs` deterministically extracts structure from a task description; **you** refine wording and variable names. The script never invents requirements — it surfaces what's missing.

## Rules

- The template is a scaffold, not the final prompt. Rewrite vague sections with the user's specifics.
- Keep `{{variable}}` names stable between INPUT and references.
- The CONSTRAINTS injection rule is load-bearing — do not remove it.
- Resolve each `warnings[]` item by asking the user or stating an explicit assumption.

## 1. Run

Requires Node 18+, zero dependencies. Fully offline.

```bash
node <skill-dir>/scripts/generate.mjs task.txt
echo "..." | node <skill-dir>/scripts/generate.mjs -
```

JSON on stdout; exit `1` when warnings exist, `2` on read/usage error.

## 2. Read the report

- `variables[]`: `{name, source}` candidate `{{placeholders}}`.
- `format`: detected output format or `null`.
- `warnings[]`: gaps to close.
- `template`: the assembled scaffold.

## 3. Refine before delivering

1. Rename variables to the user's domain vocabulary.
2. Fill `# OUTPUT` with a concrete shape (JSON schema, section list, length cap).
3. Add domain constraints the description implies.

## Lite vs full

The full `meta-prompt-architect` additionally detects tone and audience, adds assumption/ambiguity edge-case rules, and emits happy-path / edge / adversarial test-case stubs.
