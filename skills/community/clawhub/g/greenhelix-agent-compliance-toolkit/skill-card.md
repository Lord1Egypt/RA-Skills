## Description:

EU AI Act Compliance for Autonomous Agents provides a compliance toolkit for AI agent commerce, including EU AI Act risk classification, Annex IV technical documentation, cryptographic audit trails, liability-bounded escrow patterns, service contracts, monitoring, and implementation checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compliance engineers use this skill to design, document, and monitor autonomous agent commerce systems against EU AI Act obligations, audit-trail requirements, human oversight expectations, and liability-aware escrow patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code examples may affect live GreenHelix agents, escrows, disputes, webhooks, or reports if used with production endpoints or credentials.

Mitigation: Review each GreenHelix-calling example, set an explicit sandbox URL during testing, and use least-privilege test credentials.

Risk: Escrow, dispute, webhook, daemon, and reporting workflows can create operational or legal consequences when run against production systems.

Mitigation: Require operational and legal approval before adapting those examples for production use.

Risk: The guide references API and signing credentials needed for real integrations.

Mitigation: Provide GREENHELIX_API_KEY and AGENT_SIGNING_KEY through managed secrets and avoid exposing them in prompts, logs, or generated reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-agent-compliance-toolkit)
- [ClawHub Publisher Profile](https://clawhub.ai/user/mirni)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python examples, contract templates, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable skill content; real integrations may require GREENHELIX_API_KEY and AGENT_SIGNING_KEY.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
