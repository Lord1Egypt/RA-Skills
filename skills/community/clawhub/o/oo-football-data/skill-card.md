## Description:

Retrieves football-data.org matches, standings, competitions, and teams through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and football data analysts use the skill to retrieve match details, standings, competitions, teams, and match lists from football-data.org through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run downloaded CLI installation code whose contents and installed effects have not been verified.

Mitigation: Review and install the CLI separately from a verified release, and explicitly approve any setup that installs or updates other agent skills.

Risk: Football requests pass through OOMOL and require a connected account.

Mitigation: Confirm the account is connected and consider the OOMOL data path before using the skill for a request.

## Reference(s):

- [football-data.org API documentation](https://www.football-data.org/documentation/quickstart)
- [football-data.org](https://www.football-data.org/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-football-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only football data retrieval; results depend on the connected account and football-data.org access.]

## Skill Version(s):

1.0.4 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
