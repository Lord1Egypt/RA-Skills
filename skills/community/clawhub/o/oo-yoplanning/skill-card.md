## Description:

YoPlanning (yoplanning.com). Use this skill for ANY YoPlanning request — searching and reading data. Whenever a task involves YoPlanning, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can ask an agent to search and read YoPlanning teams, online products, and bookable availability through their connected account. The agent can inspect available action schemas before sending queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run a remote installer whose contents are unverified.

Mitigation: Review the installer before use, and install and verify the CLI separately instead of allowing a missing-command error to trigger downloaded code execution.

Risk: Setup may install or update other agent skills.

Mitigation: Check which skills the setup changes before accepting those changes.

Risk: Connecting YoPlanning authorizes OOMOL to use the connected account's API key.

Mitigation: Connect only an account authorized for this use and review the connection before relying on it.

## Reference(s):

- [YoPlanning homepage](https://www.yoplanning.com/)
- [YoPlanning API documentation](https://yoplanning.pro/api/v3.1/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON query responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns data from read-only YoPlanning queries; setup guidance may also be provided.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
