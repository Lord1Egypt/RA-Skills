## Description:

Integrate Frankfurter v2 through Pontx for reference-rate conversion, provider-pinned compliance, auditable time series, attribution, and large exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate Frankfurter v2 exchange-rate data through Pontx for display conversions, provider-pinned compliance calculations, auditable official-rate workflows, and large attributed history exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live exchange-rate retrieval may occur before the user has approved the resolved GET request.

Mitigation: Preview the request from live Pontx contract metadata and execute it unchanged only after explicit user approval.

Risk: Audit logs may store raw rate responses and query context for compliance workflows.

Mitigation: Confirm audit logging is intended before installation or use, and retain only the normalized query, provider, observation date, retrieval time, and raw response required for the calculation.

Risk: Using blended rates where a provider-specific official rate is required can produce incorrect compliance or accounting results.

Mitigation: Ask for the controlling jurisdiction or authority, pin the required provider, and never silently substitute a blended result for a missing provider-specific observation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-frankfurter-v2)
- [Pontx publisher profile](https://clawhub.ai/user/pontjs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to inspect live Pontx contract metadata, preview requests, require user approval for live retrieval, preserve attribution, and keep audit context for exchange-rate workflows.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
