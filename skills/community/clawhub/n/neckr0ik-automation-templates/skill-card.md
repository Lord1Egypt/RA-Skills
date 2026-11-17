## Description:

Provides ready-to-use automation templates for n8n, Make.com, and Zapier workflows across email, CRM, data sync, notifications, and e-commerce use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to find, customize, and generate workflow templates for common automation tasks in n8n, Make.com, and Zapier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated automation workflows can connect to external systems and credentials.

Mitigation: Review each destination, use least-privilege credentials or platform secret managers, and test with non-production data before activation.

Risk: The CLI can write generated templates or workflows to user-provided output paths.

Mitigation: Choose output paths deliberately and review existing files before writing generated workflow content.

Risk: Templates adapted across n8n, Make.com, and Zapier may require platform-specific adjustments.

Mitigation: Validate generated workflow structure and platform settings before connecting production services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-automation-templates)
- [ClawHub publisher profile](https://clawhub.ai/user/neckr0ik)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows may be written to user-specified output files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/claw.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
