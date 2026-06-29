## Description: <br>
Provides 2026 FIFA World Cup data by retrieving schedules, match details, team and player information, rankings, and Sporttery football odds from Baidu Sports and sporttery.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Chinese-language questions about the 2026 FIFA World Cup, including schedules, match analysis, team and player data, rankings, and Sporttery odds. Odds should be treated as informational only, not betting or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reports betting odds and betting-related workflows. <br>
Mitigation: Treat odds as informational only, not betting or financial advice, and consider local law, age restrictions, and site terms before use. <br>
Risk: The skill scrapes third-party sports and lottery sites and uses rotating browser or mobile identities for requests. <br>
Mitigation: Review site terms and installation policy before deployment, and monitor for upstream blocking, rate limits, or data availability changes. <br>
Risk: Live match, odds, and ranking data can be delayed, incomplete, or unavailable from upstream sources. <br>
Mitigation: Verify important results against official sources before relying on them for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/haizei-worldcup-2026-skill) <br>
- [Baidu Sports](https://tiyu.baidu.com) <br>
- [Sporttery football match calculator API](https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry) <br>
- [World Cup overview reference](references/overview.md) <br>
- [Sporttery odds reference](references/calculator.md) <br>
- [Workflow reference](references/workflows.md) <br>
- [Usage reference](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with optional JSON or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live scraped sports data, match identifiers, team or player identifiers, rankings, and odds; accuracy depends on upstream Baidu Sports and Sporttery availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
