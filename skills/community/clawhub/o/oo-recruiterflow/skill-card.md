## Description:

Connects to Recruiterflow to search and read candidate, job, and user records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams use the skill to retrieve candidate, job, and user records from a connected Recruiterflow workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded CLI code without a separate approval step.

Mitigation: Review and approve the CLI installation and decide which agent hosts may receive bundled skills before installing it.

Risk: Recruitment records requested through the skill may be processed by OOMOL.

Mitigation: Confirm that OOMOL may process the recruitment records requested from the connected workspace.

## Reference(s):

- [Recruiterflow](https://recruiterflow.com)
- [Recruiterflow API documentation](https://recruiterflow.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval; pagination and inclusion options vary by action.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
