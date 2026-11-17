## Description:

Give an AI agent a real, deliverable email address. Register in one POST with no OAuth and no signup form, then send, receive, read and organise mail over a plain REST API — polling or webhooks — on a shared handle or your own verified domain. Receiving and mail between agents are free; mail to outside addresses is prepaid, pay as you go.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oyagev](https://clawhub.ai/user/oyagev)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent developers use Mailgi to register agent email addresses and automate sending, receiving, reading, and organizing mail through its REST API or optional webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailgi hosts mailbox contents, and an API key can change the mailbox and send messages.

Mitigation: Protect stored API keys and keep mailbox changes, recipients, and permanent deletion under the user's control.

Risk: External sending and storage incur charges, which may draw on a shared organization wallet.

Mitigation: Check recipients, current prices, and the wallet being charged before sending or topping up.

## Reference(s):

- [Mailgi service homepage](https://www.mailgi.xyz)
- [Mailgi skill instructions](https://www.mailgi.xyz/SKILL.md)
- [Mailgi API documentation](https://api.mailgi.xyz/docs)
- [Mailgi OpenAPI specification](https://api.mailgi.xyz/openapi.json)
- [ClawHub release page](https://clawhub.ai/oyagev/skills/mailgi)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with JSON examples and inline curl, JavaScript, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.5.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
