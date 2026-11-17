## Description:

Run a small business help desk by creating tickets from email, replying in customer threads, and managing support queues and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conecto](https://clawhub.ai/user/conecto)

### License/Terms of Use:

MIT-0

## Use Case:

Small businesses and their support teams use this skill to handle incoming email tickets, send replies, track response targets, save common replies, and review support reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to Conecto's external MCP service and requests Help Desk and Email access through OAuth.

Mitigation: Review the requested access before authorizing the connection, and revoke the key from the account owner controls if access is no longer needed.

Risk: Replies, ticket changes, and a support inbox can incur charges; inbox billing renews monthly.

Mitigation: Confirm the reply approval mode before sending, ask before paid actions and inbox creation, and check the service pricing and per-call balance.

## Reference(s):

- [Conecto Help Desk](https://conecto.chat/solutions/ai-help-desk?from=clawhub)
- [Help Desk tool reference](https://conecto.chat/tools/helpdesk.md)
- [Conecto pricing](https://conecto.chat/pricing.md)
- [Conecto error codes](https://conecto.chat/docs/errors.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [MCP tool actions, email replies, and support report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send replies or change account data may incur service charges.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
