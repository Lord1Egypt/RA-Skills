## Description:

Fetches sports schedules, practices, games, and events from myclub.fi accounts, including account and club discovery, date-range schedule retrieval, and local credential-based setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanninen](https://clawhub.ai/user/hanninen)

### License/Terms of Use:

MIT-0

## Use Case:

People with myclub.fi accounts and agents assisting them use this skill to discover linked clubs and retrieve practices, games, tournaments, and other events for selected date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a myclub.fi password and stores it locally.

Mitigation: Install only when local password storage is acceptable, restrict access to the config file, and remove stored credentials when the skill is no longer needed.

Risk: Passing a real password with --password can expose it through shared shell history or logged agent sessions.

Mitigation: Avoid entering real passwords in shared shells or captured sessions; rotate the password if exposure is suspected.

Risk: Debug mode can write session cookies and private schedule pages to disk.

Mitigation: Use --debug only for troubleshooting, keep debug files private, and delete them after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanninen/skills/myclub)
- [Publisher profile](https://clawhub.ai/user/hanninen)
- [Project homepage](https://github.com/hanninen/myclub-skill)
- [myclub.fi](https://myclub.fi)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text or JSON schedule data, with shell commands for setup and fetch operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns discovered account and club data or schedule events including id, name, group, venue, date, time, event category, inferred type, and registration status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
