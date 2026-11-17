## Description:

Read HelloFresh (US) meal-kit data from a shell — the subscription (box size, delivery slot, frequency), upcoming delivery weeks with cutoffs and skip status, a week's menu with the current meal picks and premium upcharges, HelloFresh's own price for a week's box, the box sizes on offer, and the customer plan — with curl and jq, using the session token from the user's signed-in hellofresh.com tab (read once with the fpx CLI). Use when asked about HelloFresh boxes, deliveries, cutoffs, menus or picks without the hellofresh-mcp server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a HelloFresh US account can retrieve and summarize their subscription, upcoming deliveries and cutoffs, menus, meal picks, box options, and pricing from a signed-in browser session. The skill provides read-only shell queries and directs account changes to confirmation-gated HelloFresh MCP tools.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The refresh workflow includes token refresh and cookie write-back, and the available security scan is incomplete and marked the release suspicious.

Mitigation: Avoid installing until the executable script is fully inspected and the refresh-and-cookie-write workflow is clarified or removed.

Risk: HelloFresh API records may contain account holder names, email addresses, addresses, and payment details.

Mitigation: Keep the documented jq projections that remove unneeded personal data; do not dump full subscription or delivery records.

## Reference(s):

- [HelloFresh read recipes](artifact/references/requests.md)
- [hellofresh-fpx on ClawHub](https://clawhub.ai/chrischall/skills/hellofresh-fpx)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON/text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Projects HelloFresh account responses to requested fields.]

## Skill Version(s):

0.4.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
