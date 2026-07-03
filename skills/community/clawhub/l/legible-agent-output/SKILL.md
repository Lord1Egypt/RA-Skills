---
name: legible-agent-output
description: |
  Force every user-facing string from an AI agent into plain language a non-technical human can read.

  Your AI agent outputs `T-A127: run ingest` and `hunk:42`. You stare at it wondering what it means. This skill rewrites the agent's output — task titles, status messages, error messages, action previews — in language a non-technical product manager can read.
triggers:
  use_when:
    - agent emits task titles
    - agent emits status messages
    - agent emits error messages
    - agent emits action previews
    - agent emits plan summaries or cycle reports
    - agent emits sub-agent delegation prompts
    - user says "agent said A127" or "what does this code mean?"
    - user complains "too much jargon in plan" or "task titles are opaque"
  do_not_use_for:
    - backend logging (developer-only output)
    - internal RPC payloads
    - debug dumps
    - system-to-system messages
license: MIT
model: "Claude Sonnet 4.5"
compatibility: |
  Tested with Claude Sonnet 4.5 (Mavis / Claude Code).
  Designed for Claude Code, Codex, VS Code, OpenCode, Cursor, GitHub Copilot.
  No external dependencies, no MCP required, no network access at runtime.
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: 1.0
  created: 2026-06-30
  updated: 2026-06-30
  status: accepted
---

# Legible Agent Output

## Purpose

Force every agent-facing string to be readable by a non-technical human **without external context**. The agent must never expose internal IDs, framework jargon, or system-state shorthand to the user as the primary label — those belong in metadata, never in the headline.

This is a **documented UX failure** in agentic AI, not a quirk. The literature uses terms like *Intent Preview* (Smashing Magazine) and *Invisible actions* / *Unclear state* (Hatchworks); this skill synthesizes them as *plain-language action preview* and *legible agent state*.

## When to use

Load this skill when generating ANY of:

- Task or step titles in a plan / todo / worktree list
- Status messages ("working on X…", "failed at Y")
- Error messages shown to the user
- Action previews before executing ("about to do Z")
- Plan summaries or cycle reports
- Tool-call summaries surfaced to the user
- Sub-agent delegation prompts that get echoed back

**Trigger phrases:** "agent said A127", "what does this code mean?", "agent uses cryptic codes", "too much jargon in plan", "task titles are opaque", "agent output is illegible".

## The problem

AI agents routinely surface internal identifiers and framework vocabulary as if they were human-readable labels:

| Bad agent output | What the user actually sees |
|---|---|
| `T-A127: run ingest` | A random code with no meaning |
| `Applying patch from diff hunk @src/services/foo.ts:42` | Wall of internal path noise |
| `Phase 2: post-merge validation` | Vague corporate phase jargon |
| `EBADF: EBADF: bad file descriptor` | Raw OS error, no remediation |
| `mavis team plan cycle 2` | The agent's own infrastructure name |

## Core rules (the 7 laws)

Apply these as a hard checklist before emitting any user-facing string:

1. **Title first, code second.** If a task has a real-world description, that description IS the title. Internal IDs go in a parenthetical or metadata field, never in the headline.
   - BAD: `T-A127: run ingest`
   - GOOD: `Ingest weekly sales data (T-A127)`

2. **One concrete verb + one concrete object.** No gerunds of gerunds, no abstract nouns.
   - BAD: `Doing the post-merge validation processing`
   - GOOD: `Validate the merged build runs locally`

3. **Translate every error code into a sentence a stranger could act on.** A user who sees `ENOENT: no such file` cannot act; a user who sees `Profile photo file is missing — pick a new one` can.
   - BAD: `Error: EBADF`
   - GOOD: `Couldn't read the file because it's already closed — please retry`

4. **Never expose framework names as nouns.** The user does not know what a "cycle", "phase", "verifier", "hunk", or "diff" is. Either explain or drop.
   - BAD: `Cycle 2 dispatch complete`
   - GOOD: `Second review pass scheduled`

5. **Status messages describe visible state, not internal plumbing.** "Connecting to DB" is fine. "Awaiting asyncio.gather coroutine completion" is not.
   - BAD: `Awaiting Future.result() from worker pool`
   - GOOD: `Waiting for the analysis to finish`

6. **Numbers without units or context are noise.** "12.5%" of what? "step 3 of 7" — 7 what?
   - BAD: `Progress: 23%`
   - GOOD: `Processed 23 of 100 files (23%)`

7. **If you cannot write the label in ≤8 plain words, you do not yet understand the task. Stop and decompose.**

## Workflow

### Phase 1 — Pre-emission audit

Before writing the headline of any user-facing string, ask:

- Would my mother understand this without explanation? (If no, rewrite.)
- Is there an ID or code in the headline that isn't preceded by a human description? (If yes, move it.)
- Am I using a word I learned from the framework docs but the user has never seen? (If yes, translate it.)

### Phase 2 — Transform

Apply the 7 laws. For each rule violated, perform the corresponding transform (see `examples/before-after.md` for 30+ worked cases).

### Phase 3 — Self-check (eval loop)

Run the agent's own output through this checklist before showing it:

```
□ Every task title reads as a complete sentence fragment with a verb + object
□ Zero bare codes (A127, ENOENT, hunk:42) appear without a leading plain-language phrase
□ Every error message contains either (a) what happened, (b) what to do, or both
□ No framework-internal vocabulary appears in headlines (cycle, phase, hunk, verifier, …)
□ Every percentage / count has a denominator or unit
```

If any box fails → rewrite before emitting. Do not "ship it, will fix later" — illegibility compounds across cycles.

### Phase 4 — Surface the mapping when useful

For technical users, optionally append the internal ID in parentheses (`Update user profile (T-A127)`) so traceability is preserved without sacrificing legibility. For non-technical users, drop the ID entirely.

### Phase 5 — When the agent itself is the user

If the next reader is another agent (handoff, sub-task delegation), the headline can be terser but must still avoid raw error codes and framework-internal vocabulary that the receiving agent would have to look up.

## Anti-patterns

- **"It's just internal, the user won't see it."** They will. Every status message, every cycle report, every plan summary ends up in front of a human eventually.
- **"The code is needed for traceability."** Move it to metadata. Parentheses are not a crime.
- **"Translating is extra work."** It is less work than re-running a 5-minute cycle because the human misread the plan.
- **"The agent already knows what it means."** The agent is not the user. Optimize for the human at the keyboard.

## Anti-fluency & anti-sycophancy hardening

This skill shapes user-facing output of an agent — high-stakes because illegibility erodes user trust in the product, not just in the agent. Two failure modes that the skill must resist:

**Anti-fluency guard.** The skill's own examples and templates are plain language by construction. Do not "improve" the legibility of a status message by adding flowery prose, marketing-style adjectives, or "contextual embellishments" that obscure the underlying state. *Restraint is the rule.* A user who reads "We're working on it" is less informed than one who reads "Processed 23 of 100 files".

**Anti-sycophancy guard.** When a user pushes back on a legibility fix ("but the code is important", "we always use the term X"), do not capitulate. The user's domain expertise is real; their preferences about what users should see are the skill's job. Push back politely, cite law #1 or law #4 by name, and offer the parenthetical-ID compromise from Phase 4. If the user still insists, flag the trade-off explicitly ("This will make headlines harder to scan for the 80% of users who don't know the code") rather than silently agree.

**Faithfulness check.** If you find yourself rephrasing a legibility fix to make it shorter or smoother but losing the action verb or the error translation, stop. The skill is about *what the user can do with the information*, not about how the agent looks while saying it.

## Quality checklist

Before declaring output done:

- [ ] All task titles pass the "verb + object ≤8 words" test
- [ ] No bare codes, paths, or framework terms in any headline
- [ ] Error messages are actionable
- [ ] Status updates name the visible state, not the internal call
- [ ] Counts have units; percentages have denominators
- [ ] Internal IDs, if present, are in parentheses, not headlines

## Eval loop (skill-creator protocol)

To test this skill works, run these three prompts against any agent:

1. **Trigger test:** "Generate a 5-step plan to migrate a Postgres database." — Plan titles must be plain language, not `step_1`, `init_migration`, etc.
2. **Error test:** "An ENOENT error happens when reading /tmp/profile.jpg during upload. Tell the user." — Output must not contain `ENOENT`.
3. **Status test:** "Write 3 status updates the agent would show while running a 10k-row CSV ingest." — Updates must describe visible state, not `pandas.read_csv`, `chunk 23/100`, etc.

**Pass criterion:** A non-technical reader can answer "what is happening?" and "what should I do?" from the output alone.

## Output

The deliverable is the rewritten text. No file, no JSON. The agent emits the plain-language version directly to the user.

## References

Full quotes and citations from the 7 articles that ground this skill: see `references/articles-sources.md`. Quick links:

- Smashing Magazine — Designing For Agentic AI (Feb 2026) — *plain-language action preview*
- Hatchworks — Agent UX Patterns (Mar 2026) — *invisible actions, unclear state*
- boost.ai — Common Conversational AI Mistakes (Jun 2025) — *generic system messages*
- LogRocket — Overusing AI is ruining UX (Mar 2026)
- Orange Loops — 9 UX Patterns for Trustworthy AI (Jul 2025)
- Exalt Studio — UX for AI Startups
- Medium Bootcamp — UX Designers & AI Agents (Dec 2025)

Six-category taxonomy of failure modes: see `references/jargon-categories.md`.

30+ before/after transformations: see `examples/before-after.md`.

## Related skills

- `agent-auditor` (workspace) — audit agent definitions; pair with this skill to audit whether agents emit legible output
- `prompt-architect` (workspace) — uses this skill implicitly when writing prompts for sub-agents
- `ecosystem-auditor` (workspace) — periodic sweep to ensure no agent regressed into jargon
- `socratic-dialogue` — for high-stakes decisions where legible framing is not enough; reasoning rigor is also required
- `kano-model-strategist` — for deciding which features to build; legible output is about *how* you talk about them, not *which* to build

## License

MIT — see the `LICENSE` file in the repository root. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.
