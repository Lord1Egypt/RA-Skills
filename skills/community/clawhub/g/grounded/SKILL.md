---
name: grounded
description: Verify code references against the repository before trusting them. Use when writing, renaming, or reviewing code, imports, paths, or comments.
---

# Grounded skill

Grounded checks whether concrete references in a repository actually
resolve: symbols, imports, file paths, magic numbers. It never guesses.

## When to verify

* Before calling a function you did not see defined in this session.
* After renaming anything: query what else touches the old name.
* Before trusting a comment, docstring, or README claim about the code.
* Before committing imports you did not see exported.

## How to verify

Prefer the MCP tools when available (`check_path` on edited files,
`blast_radius` before renames). Without MCP, shell out:

```console
grounded scan <file> --quiet          # exit 1 on findings, 0 when clean, 3 if a checker raised
grounded impact <symbol> [PATH]       # definers, importers, comment claims
grounded fix [PATH] --dry-run         # preview unambiguous rewrites
```

Single-file checks take about a millisecond in-process, about 60 ms cold.
Full trees take seconds; gate pull requests on changed lines instead:

```console
grounded scan . --changed
```

## What findings mean

* `lie`: provably false. Fix it before building on it.
* `drift`: adjacent evidence disagrees. Read it before trusting it.
* `smell`: fragile pattern. Note it, fix it when touching the area.

## Non-goals (use the right tool)

* Docstring contracts: darglint, pydoclint, eslint-plugin-jsdoc.
* Commented-out code: Ruff ERA001.
* Type errors: mypy, tsc. Style: ruff, eslint.

## References

Load these only when needed:

* `references/rules.md`: exact checker semantics, severities, suppressions.
* `references/commands.md`: full CLI surface and exit codes.
