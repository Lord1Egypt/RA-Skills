## Description:

Monitors PETKIT smart pet devices, including feeders, litter boxes, water fountains, and air purifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External users with PETKIT smart pet devices use this skill to query current feeder, litter box, water fountain, and purifier status from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking PETKIT credentials and stores user passwords in plaintext configuration.

Mitigation: Remove bundled credentials before use, rotate the PETKIT password if it is real, and use a secure credential store or interactive prompt instead of plaintext config files or command-line passwords.

Risk: The skill uses a reverse-engineered PETKIT API that may change or fail without notice.

Mitigation: Review behavior before deployment, monitor failures, and avoid relying on the skill for critical pet care decisions without independent checks.

Risk: Logging in through the skill may sign the same account out of the PETKIT mobile app.

Mitigation: Use a shared or dedicated account where possible and confirm account-session impact before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/petkit-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-like status text and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Device status summaries may include PETKIT account and device state data returned by the PETKIT client.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
