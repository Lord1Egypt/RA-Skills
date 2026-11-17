## Description:

Search and read CollegeFootballData information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve CollegeFootballData account information, conferences, games, teams, and venues through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute unverified installation code, and automatic skill installation or synchronization can make broader agent changes.

Mitigation: Review and approve CLI installation separately using a verified release, and check and limit automatic skill installation and synchronization before use.

Risk: Requests through the connected OOMOL account may incur charges.

Mitigation: Check the connected account's terms and expected request costs before use.

## Reference(s):

- [CollegeFootballData](https://collegefootballdata.com/)
- [CollegeFootballData API documentation](https://api.collegefootballdata.com/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CollegeFootballData skill on ClawHub](https://clawhub.ai/oomol/skills/oo-college-football-data)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [Structured JSON responses from CollegeFootballData queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns data for the selected read action; available actions cover account information, conferences, games, teams, and venues.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
