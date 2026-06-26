# Writing Patterns

How to write effective instructions inside a skill's `SKILL.md` and reference files.

## Voice

Use imperative voice. Tell the model what to do, not what it could consider doing.

Good: "Read the config file before generating output."
Weak: "It might be helpful to consider reading the config file first."

## Explain the why, not just the what

Today's LLMs have strong theory of mind. When you explain *why* a step matters,
the model generalizes better than when you just bark orders.

Good: "Check for existing files first — overwriting without warning breaks trust
with the user and creates undo work."

Weak: "ALWAYS check for existing files. NEVER overwrite without asking. This is
CRITICAL."

If you catch yourself writing ALWAYS, NEVER, or CRITICAL in all caps, pause and
reframe as reasoning instead. The model will follow reasoning more reliably than
shouted constraints.

## Output format templates

When a skill needs consistent output structure, define it explicitly:

```markdown
## Report structure
Use this template:
# [Title]
## Summary
## Findings
## Recommendations
```

Keep templates short. If you need variants, put them in a `references/` file.

## Examples pattern

Include 1-2 concrete examples when the instruction is ambiguous without them.
Format clearly:

```markdown
## Commit message format
**Example:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

Do not overload with examples. Two good ones beat ten mediocre ones.

## Scope boundaries

State what the skill does *and* what it does not do. This prevents drift and
helps the model route correctly.

```markdown
## Use when
- ...

## Do not use when
- ...
```

Keep both lists short (3-5 items). If you need more exclusions than that, the
skill's scope may be too vague.

## Progressive context loading

Write `SKILL.md` so the model gets what it needs on every trigger but does not
pay the token cost for optional detail.

Pattern:
- Core workflow and rules of thumb → `SKILL.md` (always loaded)
- Detailed checklists, schemas, variant-specific guidance → `references/` (loaded on demand)
- Point to reference files with clear guidance on when to read them:

```markdown
For audit work, read `references/audit-checklist.md` before reviewing the skill.
```

## Avoid

- Manifesto language and mission statements
- Paragraphs of preamble before the first actionable instruction
- Duplicating the same guidance in `SKILL.md` and a reference file
- Passive voice ("the file should be read" vs "read the file")
- Hedging ("you might want to consider possibly checking")
