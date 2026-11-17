## Description:

Submits a product to relevant startup, SaaS, AI, and MCP directories, then tracks listing status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

Product owners and small teams use the skill to submit their own product to relevant directories, confirm verification emails, and track which listings are live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated submissions can publish inaccurate product details or proceed before the product kit and workflow are checked.

Mitigation: Review the product kit and test the workflow on two sites before enabling daily submissions; submit only the user's own product with accurate information.

Risk: Verification email and directory account access involve inbox and credential handling.

Mitigation: Use a dedicated verification inbox and store directory passwords as Nodo secrets, not in the product kit or chat.

Risk: Nodo's external setup instructions and service behavior are unverified, and daily schedules may use credits or permissions unexpectedly.

Mitigation: Review requested permissions, schedule controls, and current usage costs, and test submissions before daily operation.

## Reference(s):

- [Nodo setup guide](https://mcp.nodo.com/start.md)
- [Nodo](https://nodo.com)
- [ClawHub skill release](https://clawhub.ai/otto-iron/skills/nodo-directory-submissions-autopilot)

## Skill Output:

**Output Type(s):** [Text, Status records]

**Output Format:** [Directory listing status records and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status records identify submissions, live listing URLs, badge requirements, and blocked sites.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
