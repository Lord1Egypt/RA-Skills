## Description:

Shared Meta Ads skill for OpenClaw agents. Analyze Meta (Facebook and Instagram) ad accounts, campaigns, ad sets, ads, insights, and lead-form data with a production-safe read-first workflow. Use when an agent needs Meta Ads reporting, account audits, creative or audience diagnostics, lead-form review, or recommendations before live ad changes. Require explicit approval before any write action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to analyze Meta Ads accounts, inspect campaign and lead performance, run audits, and prepare practical recommendations before any approved live changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Improperly scoped or mishandled Meta credentials could expose account access.

Mitigation: Use approved credential injection, verify token scope before work, and never store tokens in tracked files or chat.

Risk: Lead-form data can contain sensitive personal information.

Mitigation: Retrieve only necessary lead fields, scrub PII before broader reasoning, and limit sharing to approved contexts.

Risk: Unapproved live ad changes could affect spend, delivery, or creative performance.

Mitigation: Keep the default workflow read-only and require clear user approval before pausing, enabling, editing, changing budgets, or changing creative.

## Reference(s):

- [API Setup](references/api-setup.md)
- [Account Structure](references/account-structure.md)
- [Insights and Query Patterns](references/insights-queries.md)
- [Audit Workflows](references/audit-workflows.md)
- [Optimization Heuristics](references/optimization.md)
- [Browser Fallback](references/browser-fallback.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with practical findings, recommended actions, query guidance, and approval-gated operational steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first workflow; live ad account, budget, creative, pause, or enable actions require explicit approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
