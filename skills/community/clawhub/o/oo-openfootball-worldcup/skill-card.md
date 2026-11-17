## Description:

OpenFootball World Cup (github.com). Use this skill for ANY OpenFootball World Cup request — searching and reading data. Whenever a task involves OpenFootball World Cup, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People looking up World Cup data can use this skill to retrieve groups, matches, qualification playoffs, squads, stadiums, and teams from the community OpenFootball dataset. It returns connector data for the agent to inspect or summarize; the dataset is not an official or real-time results source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded CLI installers directly, and the remote installers were not verified.

Mitigation: Review and approve CLI installation separately; prefer a verified, fixed release and check whether setup installs or updates other agent skills.

Risk: Use may depend on OOMOL sign-in and may incur OOMOL charges.

Mitigation: Review sign-in and possible charges before setup, and distinguish OOMOL billing errors from third-party account credit errors.

## Reference(s):

- [OpenFootball World Cup dataset](https://github.com/openfootball/worldcup.json)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector results with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dataset coverage depends on the season's published files; results are community data and may not be current or official.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
