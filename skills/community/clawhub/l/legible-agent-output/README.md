# Legible Agent Output

**Force every user-facing string from an AI agent into plain language a non-technical human can read.**

Your AI agent outputs `T-A127: run ingest` and `hunk:42`. You stare at it wondering what it means. This skill rewrites the agent's output — task titles, status messages, error messages, action previews — in language a non-technical product manager can read.

## What it does

The agent must never expose internal IDs, framework jargon, or system-state shorthand to the user as the primary label. Those belong in metadata, never in the headline.

The skill enforces **7 laws** for plain-language user-facing output:

1. **Title first, code second.** Real-world description IS the title; IDs go in parentheses.
2. **One concrete verb + one concrete object.** No gerunds of gerunds.
3. **Translate every error code into a sentence a stranger could act on.**
4. **Never expose framework names as nouns.** No "cycle", "phase", "verifier", "hunk".
5. **Status messages describe visible state, not internal plumbing.**
6. **Numbers without units or context are noise.** "23%" of what?
7. **If you cannot write the label in ≤8 plain words, you do not yet understand the task.**

Full taxonomy of failure modes (6 categories: bare codes, raw errors, framework vocabulary, corporate phases, numbers without context, invisible state) and 30 worked before/after transformations live in `references/` and `examples/`.

## When to use

- The agent emits task titles, status messages, error messages, or action previews
- The agent's output is going to a non-technical human (PM, stakeholder, end user)
- The user is confused by cryptic codes, framework jargon, or raw error strings

## When NOT to use

- Backend logging (developer-only output)
- Internal RPC payloads
- Debug dumps
- System-to-system messages

The legibility rules don't apply to non-user-facing strings.

## Path B evidence

A Path B eval (parallel producer + baseline) was run on 2026-06-30. The with-skill output wins 1 rubric point outright (error translation) and ties 2. The senior baseline leaked a server file path `/tmp/profile.jpg` in an error message; the with-skill output correctly translated to *"Your profile photo couldn't be uploaded because the file is missing or was moved."*

Full results in `EVIDENCE.md`.

## Sources

Grounded in 6 published UX-research articles, all verified 2026-06-30:

- Smashing Magazine — *Designing For Agentic AI* (Feb 2026) — the *Intent Preview* pattern
- Hatchworks — *Agent UX Patterns* (Mar 2026) — *Invisible actions* and *Unclear state*
- Exalt Studio — *UX for AI Startups* (Jun 2026) — contextual + concrete framing
- boost.ai — *Common Conversational AI Mistakes* (Jun 2025)
- Orange Loops — *9 UX Patterns for Trustworthy AI* (Jul 2025)
- Medium Bootcamp — *What UX Designers Should Understand About AI Agents* (Dec 2025)

Full quotes and citations in `references/articles-sources.md`. The skill's own descriptive terms (*plain-language action preview*, *legible agent state*) are synthesized labels for naming convenience — the literature uses different terms that map 1:1.

## Compatibility

- **Tested with:** Claude Sonnet 4.5 (Mavis / Claude Code)
- **Designed for:** Claude Code, Codex, VS Code, OpenCode, Cursor, GitHub Copilot
- **No MCP, no external dependencies, no network access at runtime**

## What's inside

```
legible-agent-output/
├── README.md                       ← this file
├── SKILL.md                        ← what the agent loads (7 laws, workflow, eval loop)
├── ATTRIBUTION.md                  ← source citations and license chain
├── EVIDENCE.md                     ← Path B eval results
├── LICENSE                         ← MIT
├── SYNCHRONIZATION.md              ← source-of-truth ↔ public copy mapping
├── with-skill.md                   ← Path B output (with-skill condition)
├── baseline.md                     ← Path B output (baseline condition)
├── references/
│   ├── articles-sources.md         ← 6 sources with direct quotes
│   └── jargon-categories.md        ← 6-category failure-mode taxonomy
└── examples/
    └── before-after.md             ← 30 worked transformations
```

## License

MIT — see the `LICENSE` file in this directory. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisekstudio/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
