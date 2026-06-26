# Writing Guide

Read this reference when filling out a skill's SKILL.md content.

## Frontmatter: name

Rules:
- Lowercase letters, digits, and hyphens only
- 1-64 characters
- Must match the directory name
- No leading, trailing, or consecutive hyphens

Good names are short, literal, and task-led:

- Prefer `postgres-backup` over `db-guardian`
- Prefer `pdf-redline` over `document-workbench`
- Prefer `skill-test` over `quality-checker`

Checklist:
- Includes the target object or system
- Includes the main action
- A user searching for this task would type these words

## Frontmatter: description

The description is the single most important line in the skill. It determines whether the agent invokes the skill. Write it carefully.

Template:

```
<Action> <object/system> for <main outcome>. Use when you need to <job 1>, <job 2>, <job 3>, or when the user asks about <common phrasing>.
```

Rules:
- 110-420 characters for optimal search recall
- First sentence: what the skill does (action + object + outcome)
- Second sentence: when to use it ("Use when...")
- Include concrete action verbs: create, analyze, build, fix, test, deploy, convert, generate, optimize
- Cover synonyms and common user phrasings
- Do not start with "Use when" — that belongs in the second sentence

Anti-patterns:

What to avoid | Why | Fix
--- | --- | ---
"A powerful tool for..." | Generic filler | State the specific action and object
"Use when user needs..." | Wastes the first sentence | Lead with what the skill does
Keyword lists in description | Looks spammy, hurts recall | Write one clean sentence
Brand-only name in description | Users search for tasks, not brands | Name the task
Description over 420 chars | Too long for list-page scanning | Tighten; move detail to body

## Frontmatter: metadata.openclaw

For OpenClaw compatibility, add a single-line JSON metadata field:

```yaml
metadata: { "openclaw": { "emoji": "🔧", "requires": { "bins": ["python3"] } } }
```

Available keys inside `metadata.openclaw`:
- `emoji` — icon shown in UI
- `requires.bins` — CLI binaries that must be available
- `requires.env` — environment variables that must be set
- `requires.config` — config keys that must be present

Only declare what the skill actually needs. Do not pad with unnecessary requirements.

## Body: Section Order

Write sections in this recommended order:

1. **One-sentence summary** — first paragraph after frontmatter. Repeat the core task phrase from the description.
2. **Quick Start** — 3-5 lines showing the fastest path to using the skill.
3. **When to Use / When Not to Use** — explicit activation and boundary guidance.
4. **Example Prompts** — at least 3, written as a real user would type them.
5. **Workflow** — numbered steps describing the skill's process.
6. **Commands** — runnable examples in code blocks using `{baseDir}`.
7. **Definition of Done** — measurable criteria for when the skill has finished.
8. **Resources** — links to references/ files.

## Writing Example Prompts

Example prompts help both search recall and agent triggering. Write them as a real, slightly messy human would.

Good example prompts:
- Use backtick-quoted format in a bullet list: `` - `Audit this skill for search visibility and rewrite the description.` ``
- Vary formality: some casual, some precise
- Include edge cases and non-obvious triggers
- Cover the full range of the skill's capability

Bad example prompts:
- Too abstract: "Do the thing"
- Too clean: real users do not write perfectly structured requests
- All identical phrasing: vary the wording

Aim for at least 3 prompts. 5-7 is better for broad skills.

## Writing Workflows

Use numbered steps. Each step should be a concrete action, not a vague instruction.

Good:
```
1. Read the target file and identify the format.
2. Run the conversion script.
3. Verify the output matches the expected schema.
```

Bad:
```
1. Understand the input.
2. Process it.
3. Check the result.
```

## Using {baseDir}

All command paths must use `{baseDir}` to reference files within the skill directory. This ensures portability across platforms and install locations.

```sh
python3 {baseDir}/scripts/analyze.py <input>
```

Never use hardcoded absolute paths like `/Users/`, `/home/`, or `~/`.

## Writing Definition of Done

State measurable criteria. Each item should be verifiable by a human or a script.

Good:
- The output file exists at the specified path
- The script exits with code 0
- skill-test scores the result at 85 or above

Bad:
- The skill works correctly
- The output looks good
- Everything is done

## Common Traps

Trap | Why it fails | Fix
--- | --- | ---
Explaining what X is | The model already knows | Explain WHEN and HOW to use X
Putting "Use when..." in body only | Body loads after triggering; too late | Put trigger phrasing in the description
Templates inline in SKILL.md | Bloats the file | Move to references/ or assets/
Vague "observe" instructions | Gets flagged as suspicious by security scans | Be specific about what data to read and why
Undeclared file creation | Security flag | Add a Prerequisites or Notes section
Duplicating content in SKILL.md and references/ | Wastes tokens, risks drift | Information lives in one place only
