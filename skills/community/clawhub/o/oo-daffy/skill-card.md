## Description:

Search and read Daffy account, contribution, donation, user, cause, and nonprofit data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can ask an agent to search Daffy's nonprofit directory and read account, contribution, donation, user, and cause information through their connected Daffy account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may direct the agent to execute downloaded CLI code whose installer and hosted connector implementation have not been verified.

Mitigation: Install a reviewed, pinned CLI separately and review its implementation before use.

Risk: The connected service can access Daffy financial information, and automatic agent-skill synchronization may affect the agent environment.

Mitigation: Review OOMOL's access to Daffy data and the skill synchronization behavior; consult the oo CLI command reference for the OO_SKILLS_SYNC_DISABLED setting.

## Reference(s):

- [Daffy](https://www.daffy.org/)
- [Daffy API documentation](https://docs.daffy.org/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
