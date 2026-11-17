---
name: iterate-design-review
description: Refine architecture designs or execution plans through a context-grounded independent review loop. Use when a draft needs reliable convergence on scope, layering, data ownership, interfaces, completeness, and simplicity before user approval or implementation. Do not use for ordinary code review or a trivial one-off answer.
---

# Iterate Design Review

Produce the smallest stable design or execution plan that satisfies the real system requirements. The primary agent owns the draft and decisions; reviewers challenge it but do not silently become co-authors.

## Select the output language

Keep this skill in English. Use the user's requested language, the target repository's documentation policy, or otherwise the conversation's dominant language for drafts and user-facing communication. Preserve code identifiers and quoted source text.

## Establish the design basis

Before drafting, assemble only the context needed to make the design trustworthy:

- the user's goals, confirmed decisions, non-goals, and unresolved material gates;
- upstream contracts the design must consume;
- current implementation capabilities, including what must remain supported;
- current implementation problems and responsibilities that belong elsewhere;
- real downstream consumer or application requirements;
- relevant operational evidence, failures, and prior design conclusions.

Distinguish current fact, target design, historical evidence, and open questions. Prefer a concise indexed context over repeatedly rereading broad repositories. Do not invent missing facts or treat an unfinished upstream implementation as current behavior.

## Write the primary draft

The primary agent writes and updates one canonical draft in place. Optimize for:

- clear ownership and dependency direction;
- the fewest necessary concepts and sources of truth;
- explicit data meaning and lifecycle;
- interfaces that cover verified consumers without exposing internals;
- preservation of necessary current capabilities;
- removal or relocation of redundant and misplaced responsibilities;
- visible material open gates rather than guessed defaults.

Do not add abstractions, optional fields, compatibility paths, registries, or extension points merely to answer speculative futures. A review iteration should normally simplify or clarify the draft, not make it larger.

## Configure review

Use one independent reviewer by default. Use multiple reviewers only when distinct review dimensions are substantial enough to justify parallel coverage, and give each a non-overlapping focus.

The reviewer receives the canonical draft and the design basis. Ask it to evaluate architecture and plan quality, not prose taste or implementation minutiae. Review dimensions should include:

- scope and non-goal fidelity;
- layer and ownership correctness;
- data model necessity, duplication, and lifecycle;
- public interface sufficiency and leakage;
- preservation of required current capabilities;
- downstream consumer coverage;
- failure, recovery, security, and persistence boundaries where relevant;
- unnecessary complexity and simpler alternatives;
- contradictions, hidden assumptions, and material omissions.

### Apply a materiality and plausibility gate

Review is risk-proportional, not an exercise in enumerating every theoretically possible failure. A finding is material enough to drive another design iteration only when at least one of these is true:

- it violates a confirmed user goal, supported business path, or explicit acceptance criterion;
- it breaks a public contract used by a verified consumer;
- it can corrupt durable state, authorization, identity, concurrency, recovery, confidentiality, or another high-consequence invariant;
- current code, runtime evidence, or a realistic input path demonstrates that the failure is reachable.

Rank findings by business impact, plausible reachability, and evidence strength. Do not block convergence on speculative hardening such as extreme nesting or size far outside supported limits, impossible internal states, hypothetical provider/library failures outside the owned contract, or portability concerns with no current consumer. A thousand-level JSON nesting case, for example, is non-blocking unless the system explicitly promises that input shape, exposes it as a realistic untrusted boundary, or has evidence that it occurs in production.

Consolidate non-material observations into at most one residual note. Do not require new abstractions, wrappers, schema fields, or test matrices solely to close those observations. If a cheap local correction is obvious, the primary agent may include it, but the reviewer must not turn optional defense-in-depth into a release gate.

Keep review discussion outside the canonical design unless the user explicitly requests review records. The design should always represent the latest accepted state, not the history of reviewer debate.

## Run the convergence loop

### Initial comprehensive review

Ask the reviewer to inspect the whole draft once and report all material findings it can identify in that pass. Require grouped, prioritized findings with evidence, impact, and a concrete correction or simpler alternative. Discourage serial discovery of one issue per turn.

Require the reviewer to omit non-material minutiae from the finding list and to distinguish blocking findings from optional follow-up. A severity label alone does not make a finding blocking; the report must state the owned contract, realistic reachability, and material impact.

### Triage

For every finding, the primary agent must choose one of:

- **accept**: update the canonical draft and any affected index;
- **reject**: explain why the existing design better satisfies the evidence and constraints;
- **clarify**: resolve a factual ambiguity through focused source inspection before deciding;
- **user gate**: ask the user only when the choice materially changes product semantics, authority, durable schema, or another explicitly user-owned decision.

Send disputed reasoning back to the same reviewer when useful. Do not accept a finding merely to end the loop, and do not ignore a supported finding because it changes earlier work.

### Focused repair reviews

After the comprehensive pass, subsequent reviews should inspect only accepted fixes, disputed findings, and their immediate consistency impact. Do not restart a full repository or full-draft audit on every round. Ask whether each named issue is resolved and whether the fix introduced a directly related contradiction or complexity increase.

### Final comprehensive review

When all known findings are resolved, request one final whole-draft review against the same design basis. If it finds new material issues, return to focused repair and repeat the final review once those issues are closed.

## Stop conditions

The draft is stable only when:

- the final comprehensive review has no unresolved material finding;
- all required current capabilities have an explicit owner or deliberate removal rationale;
- upstream and downstream contracts align;
- data and interfaces have no avoidable duplicate truth;
- material open gates are explicit and not disguised as defaults;
- the primary agent can explain the design coherently without relying on review history;
- further changes would be stylistic, speculative, or implementation-detail choices rather than architectural corrections.
- remaining concerns are only low-reachability defense-in-depth outside the confirmed threat model or supported input contract.

Stop instead of iterating indefinitely. Report residual uncertainty honestly when evidence is unavailable.

## Boundaries

- This skill refines designs and execution plans; it does not authorize implementation, migration, deployment, publication, or destructive actions.
- It does not prescribe a task-package directory, GOAL format, worktree layout, model, or messaging tool.
- It does not require every draft to use subagents when delegation is unavailable; an explicitly labeled independent review channel may substitute.
- Reviewers advise. The primary agent remains responsible for evidence, decisions, canonical updates, and the final explanation to the user.
