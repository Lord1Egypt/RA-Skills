## Description:

Agent skill for reasoning with Forrest Landry's Immanent Metaphysics, configuring IM-grounded soul files, onboarding OpenClaw agents, and guiding team agent communication and attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-dunlap](https://clawhub.ai/user/samuel-dunlap)

### License/Terms of Use:


## Use Case:

External developers and team members use this skill to onboard and configure OpenClaw agents grounded in the Immanent Metaphysics framework. It helps agents reason over IM concepts, prepare soul/workspace files, follow attribution discipline, and coordinate with the team's agent ecosystem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends persistent agent setup and automatic gateway service configuration.

Mitigation: Review the account, permissions, logs, network access, and uninstall path before enabling the gateway as an automatic service.

Risk: The setup flow can involve plaintext API-key storage.

Mitigation: Prefer a secret manager or OS keychain for API keys and avoid exposing credentials in workspace files or logs.

Risk: The setup guide includes executable install commands and a remote shell installer pattern.

Mitigation: Use pinned and verified install sources, and review downloads before executing them.

## Reference(s):

- [Effective Choice and the Path of Right Action](artifact/references/effective-choice.md)
- [Agent-to-Agent Ethics](artifact/references/agent-ethics.md)
- [Attribution Guide for the Immanent Metaphysics](artifact/references/attribution-guide.md)
- [Key IM Concepts](artifact/references/key-concepts.md)
- [Installation & Setup Guide](artifact/references/setup-guide.md)
- [Soul File Template & Workspace Files](artifact/references/soul-file-template.md)
- [Team Ecosystem](artifact/references/ecosystem.md)
- [Immanent Metaphysics Ontology Schema](artifact/ontology/schema.yaml)
- [An Immanent Metaphysics, Chapter 6](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_path)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local markdown, YAML, and workspace files when helping an agent apply the framework.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
