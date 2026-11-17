## Description:

Search and read API-SPORTS football data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and sports data analysts use this skill to retrieve football fixtures, standings, team and player statistics, injuries, lineups, match events, and predictions from API-SPORTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may run an unverified installer and automatic skill synchronization may affect broader agent configuration.

Mitigation: Install a verified oo CLI release yourself and review its skill synchronization before connecting API-SPORTS.

Risk: Queries may consume account credit.

Mitigation: Check account credit before making repeated queries.

## Reference(s):

- [API-SPORTS](https://api-sports.io)
- [API-SPORTS football API documentation](https://api-sports.io/documentation/football/v3)
- [API-SPORTS ClawHub release](https://clawhub.ai/oomol/skills/oo-api-sports)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON API responses summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only sports data queries; results depend on API-SPORTS coverage and the connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
