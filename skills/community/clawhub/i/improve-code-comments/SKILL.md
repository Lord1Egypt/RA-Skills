---
name: improve-code-comments
description: Use when auditing, adding, removing, or improving code comments, docstrings, JSDoc/TSDoc, TODO/FIXME/HACK notes, public API comments, inline rationale, stale/comment rot, redundant comments, documentation gaps, or "why not what" comment quality.
---

# Improve Code Comments

Improve comments with the smallest durable change. Only edit comments and docstrings; do not change code, tests, configuration, or external docs.

## Default Workflow

1. Read local guidance first: `AGENTS.md`, existing docstring style, lint rules, generated/vendor paths, and nearby examples.
2. Audit before editing unless the user explicitly asks for a narrow direct fix.
3. Report findings with `file:line`, severity, evidence, and proposed action.
4. Edit only confirmed or clearly requested comment targets. Avoid whole-repo rewrites.
5. Run the narrow formatter/check command when comment edits can affect syntax or generated docs.

## What To Change

Use this order:

1. **Remove** comments that are stale, misleading, redundant, commented-out code, author/date/history notes, or vague TODOs.
2. **Update** comments that contain useful context but no longer match current code.
3. **Add** comments only for hidden intent: business rules, non-obvious constraints, edge cases, performance/security tradeoffs, workaround reasons, lifecycle/ownership requirements, surprising return values, or public API contracts.
4. **Recommend escalation** when long architecture rationale belongs in ADRs, design docs, or API docs instead of large inline blocks.

## Quality Rules

- Explain **why**, not what the syntax already says.
- Match the existing project style; do not force a docstring format or file headers into a repo that does not use them.
- Public/exported API comments and docstrings may be more complete. Internal code gets comments only when the name, type signature, and local conventions do not carry enough context.
- Preserve tool directives exactly: `eslint-disable`, `biome-ignore`, `prettier-ignore`, `@ts-expect-error`, coverage pragmas, generated-code markers, and similar comments.
- Preserve institutional knowledge during refactors unless it is demonstrably wrong or the code it explains is removed.
- Do not use comment-density targets. Judge value per comment.
- TODO/FIXME/HACK comments need a concrete action and context: blocker, issue/spec reference, owner, or removal condition.

## Accuracy Checks

Verify comment claims against code before trusting them: thresholds, units, fallbacks, error handling, retries, null/empty cases, references, flags, public signatures, side effects, and tool-marker behavior.

## Severity

Use severity to keep reports useful:

- **Critical:** comment would cause unsafe use, data loss, security misunderstanding, or a false public contract.
- **High:** stale/misleading comment, commented-out code, or wrong docstring for a public API.
- **Medium:** redundant or vague comment, missing rationale around non-obvious behavior, weak TODO/FIXME/HACK.
- **Low:** style, placement, wording, or optional clarity improvement.

## Output

For audits, return:

1. Summary
2. Must Fix
3. Useful Improvements
4. Recommended Removals
5. Good Existing Patterns

For edits, summarize changed paths and validation. If the user asks to "add comments" broadly, stop after the audit report and ask which candidates to apply.
