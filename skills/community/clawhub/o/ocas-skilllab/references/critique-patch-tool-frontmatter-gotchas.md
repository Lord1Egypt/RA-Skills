# Patch Tool Frontmatter Gotchas

## Orphaned List Items from Removed Keys

When using `patch` to remove a YAML frontmatter key that has a list value (e.g., `triggers:` with `- item1\n- item2`), the key name is removed but the list items can survive and attach to the next YAML key.

**Real example**: Removing `triggers:` from util-github frontmatter — its list items (`- git rebase`, `- git merge`, etc.) landed under `includes:`, corrupting that field into `includes: [references/**, git rebase, git merge, ...]`.

**Fix**: After ANY frontmatter edit that removes a key, re-read the entire frontmatter region and verify orphaned items didn't migrate. Use `python3 -c "import yaml; yaml.safe_load(...)"` to validate, but also visually inspect — YAML can parse invalid structures silently.

## Block Scalar Truncation

`description: >` and `description: |` block scalars contain embedded newlines. Using `execute_code` with `content.split('---')` to extract frontmatter WILL truncate at the first `---` inside the block scalar.

**Fix**: Use `read_file` to get exact line ranges, then `patch` with precise old_string from the read. Always verify YAML parses after frontmatter edits.

## includes: Duplicate in Metadata

When moving `includes:` before `metadata:` in frontmatter, a copy can remain inside the metadata block. After any frontmatter reorder, grep the file for ALL occurrences of `includes:` and remove duplicates outside the top-level position.

## ## Headings Eaten When old_string Ends Adjacent

When `patch` replaces text where `old_string` ends immediately before a `##` heading (no trailing newline gap), the heading is consumed/deleted. This happened when replacing a section body without including the next `##` heading in the `old_string` — the replacement text doesn't include the heading, and the original heading vanishes.

**Real example**: Replacing Part 2 body text in util-github where `old_string` ended with the last line before `## Part 1: Local Git Workflows`. The `## Part 1` heading was eaten. Had to re-add it in a separate patch.

**Fix**: Always include the next `##` heading boundary INSIDE the `old_string` so it's preserved in the replacement. Or after any patch, grep for expected `##` headings: `grep -n '^## ' <file>` — if one is missing, re-add it immediately.

## Code Ratio Inflation from Inline Examples

When a SKILL.md has many inline code blocks (bash, Python, curl examples), the code ratio easily exceeds 20%. The highest-impact fix is moving large code blocks to `references/` files and replacing them with short pointers. This consistently improves D3, D4, and D8 by 1-2 points each. When code ratio is above 30%, it's a Major D3 issue that must be fixed before critique completes.