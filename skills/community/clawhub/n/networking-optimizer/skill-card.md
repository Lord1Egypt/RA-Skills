## Description:

Identify and reduce GCP networking and egress costs across projects and regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and FinOps teams use this skill to analyze exported GCP billing and network configuration data, break down egress costs, and identify optimization opportunities such as Private Google Access, CDN offload, and interconnect ROI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided GCP billing exports or network configuration may contain business-sensitive cost, project, or topology details.

Mitigation: Provide only sanitized exports or read-only CLI output, and review generated analysis before sharing it outside the intended audience.

Risk: Credentials, access keys, or unrelated project data could be pasted alongside raw diagnostic data.

Mitigation: Confirm pasted data contains no credentials, access keys, secret keys, or unrelated project details before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/networking-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, command examples, and Terraform configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided exported GCP billing and network configuration data; does not require credentials or direct account access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
