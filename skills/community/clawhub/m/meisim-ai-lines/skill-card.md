## Description:

Real US mobile numbers for AI agents, on the T-Mobile network, not virtual numbers. Texts over the API and webhooks; voice over SIP with the number as caller ID. $35 a month for texts, $45 with voice, two months up front. Every account passes an identity check, and we keep spammers off our lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meisimusa](https://clawhub.ai/user/meisimusa)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill on behalf of their owners to review MeiSIM's current offer, guide owner-led account setup, and manage approved US mobile lines for texting and calls. It covers checking prices, placing orders only after clear approval, and configuring messaging or SIP voice.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill sends API requests and the account key to MeiSIM, and the security review notes that the scan was partial.

Mitigation: Use the service only if the owner trusts MeiSIM; keep the key in a secret store, and review linked API documentation before enabling actions.

Risk: Line orders, renewals, messages, and calls can have financial or real-world effects.

Mitigation: Require the owner's clear approval for the exact order or renewal price, and review consent and recipient details before sending messages or placing calls.

## Reference(s):

- [MeiSIM AI agent overview](https://www.meisimusa.com/api-for-ai-agents.html)
- [SMS lines API reference](https://www.meisimusa.com/api-docs.html#sms-lines)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
