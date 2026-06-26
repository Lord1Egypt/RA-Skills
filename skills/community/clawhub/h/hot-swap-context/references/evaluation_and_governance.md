# Evaluation and Governance Guide

## Why this reference exists

Read this file when the task involves trust, deletion, portability, auditability, or retrieval quality. Use it to evaluate whether a context system is genuinely usable and governable rather than merely impressive in demos.

## Governance principles

A context system should make durable memory useful **and** reversible.

OpenAI documents memory deletion behavior separately from chat deletion, which shows that persistent memory must have explicit lifecycle controls [1]. Anthropic exposes view, edit, pause, reset, and organization-level controls for memory, which shows that governance is part of the memory surface rather than an afterthought [2].

Build governance around the following principles:

| Principle | What it requires |
|---|---|
| Visibility | Users or admins can inspect important memory objects |
| Editability | Incorrect or outdated memories can be corrected |
| Deletability | Memories can be forgotten with a defined propagation path |
| Exportability | Durable context can be extracted for migration or review |
| Scope control | Personal, team, and enterprise memories are not mixed carelessly |
| Auditability | Reads, writes, deletions, and bundle generation can be traced |

## Evaluation scorecard

Evaluate the system across five dimensions.

| Dimension | Core question |
|---|---|
| Retrieval quality | Did the right context arrive at the right task? |
| Portability | Can the context move between tools or runtimes without collapse? |
| Governance | Can memory be inspected, edited, deleted, and scoped correctly? |
| Trust | Can users understand why a memory was used or changed? |
| Operational value | Does the context measurably reduce cold starts and improve task quality? |

Use `templates/eval_scorecard.md` as the standard artifact.

## Suggested metrics

| Metric | Interpretation |
|---|---|
| Cold-start reduction | Lower re-explanation burden |
| Retrieval precision | Higher percentage of useful retrieved memory |
| Retrieval noise rate | Lower proportion of irrelevant context |
| Portability success rate | Higher percentage of bundles that remain usable after migration |
| Memory edit acceptance rate | Higher trust in system-proposed memory updates |
| Forget/delete integrity | Lower rate of deleted memory resurfacing |
| Governance exception count | Lower number of policy violations or ambiguous ownership cases |

## Audit procedure

Follow this procedure when auditing a system.

1. Identify all memory stores and where ownership resides.
2. Check whether the system distinguishes memory types.
3. Inspect retrieval logic and whether it is just-in-time or indiscriminate.
4. Verify that important memory objects can be viewed and edited.
5. Test deletion semantics conceptually or practically.
6. Test whether exported or bundled context is reusable in another runtime.
7. Record metrics and qualitative failure modes in the scorecard.

## Common failure modes

| Failure mode | Why it matters |
|---|---|
| Memory cannot be inspected | creates hidden coupling and low trust |
| Deletion is nominal only | causes resurfacing of unwanted or sensitive memories |
| Artifacts are absent from memory design | loses the user’s most valuable work product layer |
| Retrieval is over-broad | wastes context window and degrades reasoning quality |
| Portability stops at ZIP export | preserves data but not operational context |
| Ownership boundaries are unclear | risks IP leakage or broken migration logic |

## Decision rule

Do not declare the system mature unless it passes both tests below:

1. It improves real work through retrieval and continuity.
2. It preserves user or organization control through clear governance.

If either test fails, the memory layer is still incomplete.

## References

[1]: https://help.openai.com/en/articles/8590148-memory-faq "Memory FAQ | OpenAI Help Center"
[2]: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context "Use Claude’s chat search and memory to build on previous context | Claude Help Center"
