## Description:

Operate apaleo through an OOMOL-connected account to read and manage properties, units, unit groups, and unit attributes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Apaleo account operators use the skill to inspect and manage properties, units, unit groups, and unit attributes through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs execution of downloaded installer code without a separate approval step.

Mitigation: Review setup before enabling the skill, install a verified CLI release yourself, and prevent automatic remote-installer execution.

Risk: OOMOL mediates account access and receives requested operation payloads; write and deletion actions can change or remove apaleo data.

Mitigation: Require approval for the exact write payload and deletion target before execution.

## Reference(s):

- [apaleo API documentation](https://apaleo.dev/)
- [apaleo](https://apaleo.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and destructive actions require approval for the exact payload and target.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
