## Description:

Shared Google Ads API skill for OpenClaw agents to query reporting data, run audits, review wasted spend and conversion tracking, and draft read-first recommendations before approved live changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to connect to Google Ads, run read-only reports and GAQL queries, audit campaign health, identify wasted spend, review conversion tracking, and prepare recommendations that require approval before live changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication helper prints a long-lived OAuth refresh token to standard output.

Mitigation: Do not run the helper in an agent, shared terminal, CI job, or logged environment until token handling is changed to use an approved secret channel without printing the token.

Risk: Reporting scripts use Google Ads credentials from the environment and contact Google's API.

Mitigation: Use approved credential injection, verify the target account ID and date range, and keep analysis read-only unless the user explicitly approves an operational change.

Risk: Google Ads exports and account notes can contain customer-identifying data.

Mitigation: Apply PII protection before sharing reports broadly or using exported data with additional models or agents.

## Reference(s):

- [API Setup](references/api-setup.md)
- [GAQL Examples](references/gaql-examples.md)
- [Audit Workflows](references/audit-workflows.md)
- [Optimization Heuristics](references/optimization.md)
- [Browser Fallback](references/browser-fallback.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and text API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use environment-provided Google Ads credentials and contact the Google Ads API; live account changes require explicit approval.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
