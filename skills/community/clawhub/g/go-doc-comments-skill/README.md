# go-doc-comments-skill

A [Claude](https://claude.com/claude-code) / Agent **skill** that writes and supplements Go source comments to the official Go doc comment standard ([go.dev/doc/comment](https://go.dev/doc/comment)).

> 中文文档见 [README.zh-CN.md](./README.zh-CN.md)

## What it does

When you ask an agent to comment, document, or annotate Go code, this skill guides it to produce documentation that is idiomatic, tool-friendly, and consistent with how the Go ecosystem expects doc comments to look. It merges two ideas:

- **Comment sparingly inside function bodies** — explain *why*, not *what*; prefer clear names over comments.
- **But document every exported identifier** — a hard Go convention. `go doc`, `gopls`, and `pkg.go.dev` all extract doc comments, so every exported package, func, type, const, and var gets one.

The skill keeps these two rules separate so the agent never skips an exported API's doc comment by citing "self-documenting code."

## Features

- **A decision framework for whether to comment at all.** A step-by-step gate (exported? → self-explanatory? → better name/refactor? → WHY not WHAT?) that decides both whether to add a comment and what kind — the core of good commenting judgment.
- **Official standard, encoded.** Placement rules, identifier-first sentences, `reports whether` for booleans, zero-value/concurrency/complexity documentation, `Deprecated:` markers, and the full gofmt-aware syntax (headings, doc links `[pkg.Name]`, lists, code blocks, notes, directives) — with the exhaustive syntax rules in [`references/doc-comment-syntax.md`](references/doc-comment-syntax.md), loaded on demand.
- **Language-aware.** Detects the existing comment language in a file/package and matches it (English by default), while keeping Go's machine tokens (`Deprecated:`, `TODO(...)`, `//go:...`, doc-link brackets) and the identifier-first structure in canonical form.
- **gofmt-stable output.** Comments are written so `gofmt` leaves them unchanged — correct indentation for lists and code blocks, `#` headings, and doc-link syntax.
- **Audit-then-fix workflow.** Inventories exported-but-undocumented declarations before mass-editing, so nothing is missed.
- **Anti-patterns and a checklist.** Catches the common Go documentation defects: missing doc comments, non-identifier-first sentences, blank lines that demote doc comments, accidental code blocks from indentation, and redundant/dead-code comments.
- **Accuracy guardrail.** Describes only behavior confirmed from the code; never asserts unverified versions, RFCs, or benchmark bounds.

## Installation

Install it where your agent discovers skills. The skill is `SKILL.md` plus a `references/` folder loaded on demand.

### Let the agent install it (easiest)

Just send your agent a message like:

```
Install this skill for me: https://github.com/rroy233/go-doc-comments-skill
```

The agent will clone the repository into the appropriate skills directory (`.claude/skills/` for project scope or `~/.claude/skills/` for user scope) and confirm the skill is available.

### Claude Code

Clone into your project or user skills directory:

```bash
# Project-scoped (this repo only)
git clone https://github.com/rroy233/go-doc-comments-skill .claude/skills/go-doc-comments

# Or user-scoped (all your projects)
git clone https://github.com/rroy233/go-doc-comments-skill ~/.claude/skills/go-doc-comments
```

The skill directory only needs to contain `SKILL.md`. After installing, the skill auto-activates when you ask about commenting Go code, or you can invoke it explicitly with `/go-doc-comments`.

### Manual

Download this repository's contents (`SKILL.md` and `references/`) and place them at:

```
<your-skills-dir>/go-doc-comments/
├── SKILL.md
└── references/
    └── doc-comment-syntax.md
```

## Usage

Just ask, in a project that contains Go code:

```
Document the exported functions in server.go
Add doc comments to this package
Fix the comments in handler.go to match the Go standard
```

The skill will read the code, detect the comment language, inventory undocumented exported symbols, and write standard-conforming doc comments.

## References

- [Go Doc Comments](https://go.dev/doc/comment)
- [Effective Go: Commentary](https://go.dev/doc/effective_go#commentary)

## License

MIT
