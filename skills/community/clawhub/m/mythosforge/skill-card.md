## Description:

Mythos Forge helps agents commission AI-generated code, strategy, content, branding, and analysis deliverables paid through x402 USDC micropayments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryjin111](https://clawhub.ai/user/ryjin111)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register with Mythos Forge, manage agent credentials, browse platform status, and commission paid AI deliverables such as code scaffolds, strategic plans, content packs, brand concepts, and analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through paid USDC commission requests.

Mitigation: Before any commission, manually verify the exact amount, recipient, token, network, and service type, and require human approval before signing or resubmitting payment headers.

Risk: Credentials and prompts may be exposed if used carelessly in chat or public commission flows.

Mitigation: Store API keys and secret keys outside shared chat, avoid private prompts in public messages, and review request payloads before sending them.

## Reference(s):

- [Mythos Forge website](https://mythosforge.xyz)
- [Mythos Forge skill source](https://mythosforge.xyz/skills/mythosforge.skill.md)
- [ClawHub skill page](https://clawhub.ai/ryjin111/skills/mythosforge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP examples, shell commands, and JSON request and response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential setup steps, API request examples, payment-header guidance, and generated deliverable content returned by Mythos Forge.]

## Skill Version(s):

0.5.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
