## Description:

Customer-service agents built on the PASM cognitive engine answer from sourced knowledge facts, refuse unsupported answers, escalate complaint classes, isolate each agent's knowledge base, and optionally use a vendor-neutral LLM with fallback to knowledge-base answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer-support teams use this skill to embed a customer-service agent that answers from their own FAQ or knowledge-base entries, declines unsupported questions, and returns escalation context for handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared default persistence paths can expose one tenant's knowledge-base entries to another tenant's support flow.

Mitigation: Configure a separate persist_dir or kb_dir for each tenant, store, or deployment.

Risk: The optional HTTP gateway does not provide built-in authentication controls.

Mitigation: Enable the gateway only behind an authenticated access layer and apply organization-specific controls for customer support data.

Risk: Optional external LLM use can send customer-support context to a configured model provider.

Mitigation: Use an approved provider configuration, protect API keys, and apply the organization's data-handling requirements before enabling LLM mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-cs-agent)
- [Project homepage from skill metadata](https://github.com/arronJack/pasm-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent can also return structured escalation context and machine-readable snapshots when used from code.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
