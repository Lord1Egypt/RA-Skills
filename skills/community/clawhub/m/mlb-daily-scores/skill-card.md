## Description:

Provides daily MLB baseball scores, box scores, starting pitchers, and injury reports for a configured favorite team across spring training, regular season, playoffs, and on-demand use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremydouglaslaw-ui](https://clawhub.ai/user/jeremydouglaslaw-ui)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to receive scheduled or on-demand MLB briefings for a configured favorite team, including yesterday's recap, today's game preview, probable pitchers, and injury information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install hook runs Python setup code and downloads unpinned third-party packages from the package index.

Mitigation: Review the setup scripts before installation and prefer pinned or hash-verified dependency installs when deploying in controlled environments.

Risk: The skill depends on external MLB API availability and configured team/timezone values.

Mitigation: Validate the configured team name and timezone, and treat missing game data or API failures as operational conditions rather than authoritative baseball status.

## Reference(s):

- [MLB Daily Scores on ClawHub](https://clawhub.ai/jeremydouglaslaw-ui/skills/mlb-daily-scores)
- [ClawHub MLB Daily Scores Search](https://clawhub.ai/skills?focus=search&q=mlb-daily-scores)
- [MLB Stats API](https://statsapi.mlb.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report generated from JSON returned by the MLB fetch script, with setup and scheduling commands when configuration is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report may suppress delivery with HEARTBEAT_OK when no game or injury data is available.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
