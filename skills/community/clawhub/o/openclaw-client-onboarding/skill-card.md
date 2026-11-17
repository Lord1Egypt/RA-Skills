## Description:

OpenClaw Client Onboarding helps collect client requirements, generate configuration recommendations, create client profile files, and prepare a quote for paid OpenClaw setup services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Service providers or operators onboarding paid OpenClaw clients use this skill to collect model, messaging-channel, budget, and use-case requirements, then prepare configuration guidance, client records, and a quote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent customer files using a customer name as part of the folder path.

Mitigation: Confirm before writing files, scope writes to the intended workspace, and sanitize customer names into safe folder identifiers.

Risk: Client notes, configuration files, or invoices may capture unnecessary sensitive customer data.

Mitigation: Record only the information needed for onboarding and review generated customer-facing files before sharing them.

## Reference(s):

- [Openclaw Client Onboarding on ClawHub](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-client-onboarding)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration content and client-facing notes or invoice content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent client files such as config.json, notes.md, and invoice.md when the agent is authorized to write them.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
