## Description:

Poku lets an agent place and receive phone calls and messages, reserve dedicated phone numbers, and configure inbound webhooks through the Poku API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emileindik](https://clawhub.ai/user/emileindik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Poku to have an agent make calls, send SMS, WhatsApp, or Slack messages, reserve numbers, and set up inbound communication workflows after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound calls and messages expose recipient details, prompts, message content, and related metadata to Poku and downstream communications providers.

Mitigation: Confirm each outbound call or message before execution and avoid sending sensitive content unless the user accepts that disclosure.

Risk: Inbound webhook setup can wake the main agent with untrusted external messages.

Mitigation: Route inbound events to a dedicated low-privilege agent, use per-event sessions, and clearly label inbound text as untrusted.

Risk: Webhook administration controls are under-scoped for sensitive agents.

Mitigation: Verify webhook signatures and require trusted user confirmation before follow-up calls, messages, number changes, or webhook deletions.

## Reference(s):

- [Poku API Reference](references/API.md)
- [Calls Workflow](references/CALLS.md)
- [Messaging Flow](references/MESSAGES.md)
- [Phone Number Reservation and Management](references/NUMBERS.md)
- [Webhooks and Inbound Configuration](references/WEBHOOKS.md)
- [Poku Homepage](https://pokulabs.com)
- [Poku API Docs for LLMs](https://docs.pokulabs.com/llms.txt)
- [Poku Interactive Docs](https://docs.pokulabs.com)
- [Poku Webhook Setup](https://docs.pokulabs.com/poku-skill/webhook)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POKU_API_KEY. Outbound communication, number changes, and webhook administration should be confirmed before execution.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
