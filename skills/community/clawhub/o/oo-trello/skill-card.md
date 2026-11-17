## Description:

Trello (trello.com). Use this skill for ANY Trello request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Trello users use this skill to search and read boards, cards, members, and checklists, or to create and update them through their connected account. Confirm the exact payload and effect before writes, and get explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified remote installer automatically.

Mitigation: Review and pin the CLI before installation, and check its automatic agent-skill installation behavior.

Risk: Changes made through Trello actions can alter or remove board data.

Mitigation: Keep the skill's approval requirements: confirm the exact payload and effect before writes, and get explicit approval before destructive actions.

## Reference(s):

- [Trello](https://trello.com)
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [OOMOL Trello connection setup](https://console.oomol.com/connections/trello)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Trello data; write and destructive actions require confirmation as described in the skill.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
