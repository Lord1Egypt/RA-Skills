## Description:

PKU BDKJ helps agents use a CLI to log in to PKU's bdkj.pku.edu.cn service, find academic discussion rooms, manage participant groups, and create or cancel reservations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

PKU students or staff and their agents use this skill to query available academic discussion rooms, reuse saved participant groups, and manage real room bookings through the bdkj CLI.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can guide stored-credential login and preserve session and participant group data locally.

Mitigation: Require explicit approval before stored-credential login and periodically inspect or delete ~/.config/info/bdkj data on shared or sensitive machines.

Risk: The skill can guide creation or cancellation of real PKU room reservations.

Mitigation: Confirm the intended room, time, reason, participants, and apply ID with the user before reservation or cancellation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-bdkj)
- [PKU BDKJ service](https://bdkj.pku.edu.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide actions that create or cancel real room reservations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
