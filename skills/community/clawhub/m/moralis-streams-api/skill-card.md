## Description:

Real-time blockchain event monitoring with webhooks for setting up, managing, and troubleshooting Moralis Streams across EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novnski](https://clawhub.ai/user/novnski)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, update, delete, inspect, and troubleshoot Moralis Streams webhooks for real-time wallet, token transfer, contract event, and chain activity monitoring across EVM networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A runnable tutorial contains a hard-coded third-party webhook URL, which could send stream monitoring data outside the user's control.

Mitigation: Replace webhook.site, YOUR_WEBHOOK_URL, and other placeholder destinations with an HTTPS endpoint the user owns before creating or updating streams.

Risk: The skill can produce curl commands that create, update, delete, patch, change status, or change settings for live Moralis Streams.

Mitigation: Review the endpoint, HTTP method, stream ID, chain IDs, webhook URL, and request body before running any API-changing command.

Risk: The skill requires MORALIS_API_KEY and webhook signature secrets to interact with and verify Moralis Streams.

Mitigation: Keep credentials in environment variables or local secret storage, never paste them into chat, and verify incoming webhooks with the Moralis streams secret.

## Reference(s):

- [Moralis documentation](https://docs.moralis.com)
- [Source repository](https://github.com/MoralisWeb3/onchain-skills)
- [ClawHub skill page](https://clawhub.ai/novnski/skills/moralis-streams-api)
- [Webhook Security](artifact/references/WebhookSecurity.md)
- [Delivery Guarantees](artifact/references/DeliveryGuarantees.md)
- [Common Pitfalls](artifact/references/CommonPitfalls.md)
- [Stream Configuration](artifact/references/StreamConfiguration.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with curl commands, JSON payload examples, and implementation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and MORALIS_API_KEY; API-changing commands should be reviewed before execution.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
