## Description:

Use for direct Open Exchange Rates integration, plan-aware historical-rate retrieval, currency-conversion safeguards, and caller-owned App ID handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Open Exchange Rates through Pontx while keeping API credentials caller-owned, checking plan requirements, previewing requests, and approving live reads explicitly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Open Exchange Rates App IDs can be exposed if pasted into chat, source control, commands, or logs.

Mitigation: Keep the App ID in the caller environment, use local SDK or CLI guidance to construct requests, and show only redacted previews.

Risk: Live API reads can consume quota or fail when the selected capability is not available on the caller's plan.

Mitigation: Verify the current resource, plan requirements, requested currencies, and quota impact before approving execution.

Risk: Currency conversion output can be misused in transaction-processing workflows without local financial controls.

Mitigation: Treat exchange-rate results as application input and apply the caller's own validation, rounding policy, and approval boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-open-exchange-rates)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes redacted previews, plan checks, quota considerations, and credential-handling guidance before live API reads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
