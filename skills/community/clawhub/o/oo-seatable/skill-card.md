## Description:

Use SeaTable through the user's OOMOL-connected account to read, create, update, and delete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agent developers with a connected SeaTable account can inspect base metadata and rows, and manage table rows through the OOMOL SeaTable connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified remote installers and may install or synchronize other agent skills.

Mitigation: Review and install the CLI separately before allowing the skill to run; disable automatic installation or synchronization if unwanted.

Risk: SeaTable write and delete actions can change user data.

Mitigation: Keep the skill's approval requirement for changes and deletions, and review the exact target and payload before execution.

## Reference(s):

- [SeaTable API documentation](https://api.seatable.com/)
- [SeaTable](https://seatable.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI and an authenticated OOMOL account connected to SeaTable; action schemas are inspected before payloads are built.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
