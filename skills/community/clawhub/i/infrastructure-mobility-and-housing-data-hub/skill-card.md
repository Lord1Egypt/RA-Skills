## Description:

Infrastructure, Mobility, and Housing Data Hub helps agents query World Bank infrastructure and urban development data by country or region through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to fetch country or regional infrastructure, mobility, urbanization, water, sanitation, electricity, internet, roads, logistics, and SDG progress data without manually selecting World Bank indicator codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live instructions and schemas returned by AgentPMT may change after publication.

Mitigation: Treat live AgentPMT content as untrusted guidance, keep behavior bounded by the local skill, and verify schema details before production integrations.

Risk: Setup examples include unpinned npx commands connected to account, wallet, and payment workflows.

Mitigation: Pin or independently verify packages before running setup commands, especially in sensitive environments.

Risk: Credential, wallet, or payment data could be exposed if copied into prompts or logs.

Mitigation: Do not provide account secrets, private keys, mnemonics, signatures, or payment headers in prompts, logs, or remote tool inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/infrastructure-mobility-and-housing-data-hub)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/infrastructure-urban-development)
- [Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown instructions with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool calls return JSON infrastructure data, country metadata, access gaps, SDG progress, urban-rural analysis, logistics notes, and validation errors when inputs are invalid.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
