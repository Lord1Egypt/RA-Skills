## Description:

Archives user prompts, assistant responses, and session metadata to a configured internal endpoint in authorized environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airis101](https://clawhub.ai/user/airis101)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized ByteDance internal teams use this skill to archive agent conversations and session metadata for approved recordkeeping and audit workflows.

### Deployment Geography for Use:

Global; limited to explicitly approved ByteDance internal environments, with no geographic restriction specified.

## Known Risks and Mitigations:

Risk: Persistent hooks send raw prompts, assistant replies, and session metadata to a ByteDance endpoint, potentially including confidential material.

Mitigation: Install only in explicitly approved internal environments; review the endpoint, access controls, and retention policy before enabling archival.

Risk: Conversation data may be transferred when archival is not appropriate for a project.

Mitigation: Set SYNC_ENABLE=0 to disable collection and transfer; avoid installation in personal, external, customer, or secret-bearing projects without organizational approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/airis101/skills/interaction-record-archive)
- [ClawHub publisher profile](https://clawhub.ai/user/airis101)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When installed and enabled, the hooks send JSON conversation records to the configured endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled skill frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
