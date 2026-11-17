## Description:

Send real handwritten notes through robots with real pens -- physical cards mailed to recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidwachs](https://clawhub.ai/user/davidwachs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and business users connect an AI assistant to Handwrytten so it can browse cards and fonts, manage address data, create custom card assets, and submit handwritten-note mailings. The skill is suited to customer outreach, thank-you notes, bulk mailings, and order tracking workflows where physical mail is intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit paid physical-mail orders, including bulk sends and gift-card orders.

Mitigation: Require human review and explicit approval in the client before live sends, bulk sends, gift-card orders, or basket submission.

Risk: The skill can process recipient addresses and mutate saved recipients, senders, custom cards, images, and QR codes.

Mitigation: Use an API key tied to an account where the assistant is allowed to process that data, and prefer a limited or test account when evaluating the skill.

Risk: The server does not enforce confirmation safeguards before actions that spend credits or change account data.

Mitigation: Add client-side confirmation gates for order placement, deletions, asset changes, and other irreversible or costly actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidwachs/skills/handwrytten)
- [Project homepage from ClawHub metadata](https://github.com/handwrytten/handwrytten-mcp-server)
- [Handwrytten website](https://www.handwrytten.com)
- [Handwrytten API settings](https://www.handwrytten.com/api/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [MCP tool results as JSON-formatted text, plus concise agent-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and HANDWRYTTEN_API_KEY; tool calls can submit paid mail orders and mutate saved Handwrytten account data.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact package.json and MCP server report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
