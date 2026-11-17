## Description:

Retrieves 2026 FIFA World Cup teams, schedules, match details, team and player data, rankings, predictions, and official sporttery.cn betting odds using Baidu Sports and China Sports Lottery data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer 2026 FIFA World Cup questions about teams, fixtures, match details, player and team statistics, standings, and odds. It is suited for informational sports lookup workflows and should not be used as betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scrapes public sports sites and uses rotating browser/mobile headers, which may trigger blocking or conflict with source-site expectations.

Mitigation: Review source-site terms before deployment, keep request rates conservative, and stop using the skill against a source that blocks or rejects requests.

Risk: The skill exposes betting odds and prediction-oriented data that could be misused for wagering decisions or conflict with local gambling laws.

Mitigation: Present odds and predictions as informational only, avoid betting recommendations, and require users to check applicable laws before acting on wagering-related information.

Risk: Some behavior can return broader football data instead of only World Cup data.

Mitigation: Use explicit filters such as --wc, --team, and --date when the intended workflow is limited to World Cup results.

Risk: Live scores, odds, and scraped statistics may be delayed, incomplete, or unavailable.

Mitigation: Verify time-sensitive results against official sources before relying on them for reporting or decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/haizei-worldcup-2026-skill)
- [Baidu Sports](https://tiyu.baidu.com)
- [China Sports Lottery football calculator API](https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry)
- [Overview reference](references/overview.md)
- [Usage workflows](references/workflows.md)
- [Calculator reference](references/calculator.md)
- [Schedule reference](references/schedule.md)
- [Match reference](references/match.md)
- [Team reference](references/team.md)
- [Player reference](references/player.md)
- [Rankings reference](references/rankings.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include live scraped sports data, predictions, and betting odds; odds are informational and may require filtering with --wc, --team, or --date.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence, created 2026-06-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
