# Best Practices

## Frontmatter

- Keep only `name` and `description`.
- Use lowercase letters, digits, and hyphens in `name`.
- Keep `name` under 64 characters.
- Make `description` do the triggering work.
- Put "when to use" information in `description`, not in a body section.

## SKILL.md Body

- Write imperative instructions.
- Start with the execution path, not project background.
- Keep core guidance in the main file and move detail to `references/`.
- Link directly to reference files from `SKILL.md`.
- Stay concise enough that the whole file can load comfortably.

## Resource Choice

- Add `scripts/` when code would otherwise be rewritten repeatedly.
- Add `references/` when detailed guidance is useful but not always needed.
- Add `assets/` when templates or starter files improve output quality.
- Skip any directory that does not remove real friction.

## Anti-Patterns

- Do not ship placeholder prose disguised as `.py` scripts.
- Do not add auxiliary documentation such as `README.md` inside the skill folder.
- Do not duplicate the same rule in multiple files.
- Do not mix discovery questions, implementation details, and marketing copy in one section.
- Do not force bilingual text unless it helps a real user interaction step.

## Quality Bar

Check these before finishing:

- Triggering is specific enough to fire on the right requests.
- The chosen pattern matches the real failure mode.
- Files in `references/` are one hop from `SKILL.md`.
- Scripts run successfully.
- Packaging excludes junk like `.git` and `.DS_Store`.
