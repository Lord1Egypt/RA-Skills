## Description:

Oomnitza (oomnitza.com). Use this skill for ANY Oomnitza request — searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents connected to an Oomnitza account can validate the connection and retrieve asset or user records. The skill guides callers to inspect each action's schema and submit a matching request through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without verification or a separate approval step.

Mitigation: Preinstall a vetted oo CLI release and require approval before installing software or changing agent skills.

Risk: The OOMOL-connected account may expose requested Oomnitza records to the connector.

Mitigation: Confirm that OOMOL should receive access to the records needed for the task.

## Reference(s):

- [Oomnitza](https://www.oomnitza.com)
- [Oomnitza API documentation](https://oomnitza.zendesk.com/hc/en-us/articles/6515859398807-Creating-asset-workflows-using-the-Oomnitza-API)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Oomnitza skill release](https://clawhub.ai/oomol/skills/oo-oomnitza)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON action responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results vary by selected Oomnitza read operation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
