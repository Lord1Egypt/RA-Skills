## Description:

Use when calculating, auditing, implementing, or reviewing token pricing and billing formulas for OpenAI-style APIs, NewAPI-compatible gateways, cached input/prompt caching, per-1K or per-1M token prices, quota consumption, recharge ratios, and cost comparison dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y-victor](https://clawhub.ai/user/y-victor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and reviewers use this skill to calculate and audit token billing for OpenAI-style APIs, NewAPI-compatible gateways, cached input pricing, quota conversion, and dashboard cost comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token cost calculations can become inaccurate if provider prices, units, or gateway ratios are stale or mixed.

Mitigation: Verify current provider prices and billing mode before applying the formulas, and keep quota calculations separate from money conversions.

Risk: Cached input tokens may be double-counted if treated as a separate bucket rather than part of input tokens.

Mitigation: Split cached input from total input before pricing and clamp cached input so it cannot exceed total input tokens.

## Reference(s):

- [Token Cost Formula Reference](references/formulas.md)
- [ClawHub skill page](https://clawhub.ai/y-victor/skills/openai-newapi-calc-token)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with formulas, checklists, examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider prices are not embedded; users should verify current pricing separately before relying on calculations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
