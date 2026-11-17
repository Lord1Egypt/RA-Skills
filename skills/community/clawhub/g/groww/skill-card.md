## Description:

Trade stocks and manage portfolio on Groww for Indian NSE/BSE market data, portfolio holdings, order placement, order status, and order cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushp1997](https://clawhub.ai/user/pushp1997)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent retrieve Groww portfolio and Indian equity market data, then prepare or execute Groww order-management actions when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live Groww stock orders without documented confirmation safeguards.

Mitigation: Require explicit human confirmation for every buy, sell, or cancel request and keep trading disabled unless order execution is intended.

Risk: The skill requires a Groww API key that can expose account and trading capabilities.

Mitigation: Use a restricted key if Groww supports it, store GROWW_API_KEY securely, and revoke or rotate it when access is no longer needed.

## Reference(s):

- [ClawHub Groww skill page](https://clawhub.ai/pushp1997/skills/groww)
- [Groww API base URL](https://api.groww.in/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API calls, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROWW_API_KEY and may produce trading commands or direct Groww API requests.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
