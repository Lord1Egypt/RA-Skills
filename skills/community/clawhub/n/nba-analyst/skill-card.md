## Description:

NBA 全能数据分析助手。查询比分、排名、球员数据、球队信息、球员/球队对比、AI深度分析、生成可视化HTML报告。全中文界面，零API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language NBA questions about scores, schedules, standings, players, teams, comparisons, drafts, and recent performance. It can also generate local HTML analysis reports for players, teams, and current games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are range-based rather than locked, so future package updates may change runtime behavior.

Mitigation: Install in an isolated Python environment and add a lockfile or pinned dependency set before relying on the skill.

Risk: The skill performs outbound requests to NBA data services, so results can fail, change, or be rate-limited by upstream services.

Mitigation: Review outputs for freshness and handle endpoint failures or empty data as part of the agent workflow.

Risk: Report and cache behavior creates local files inside the skill package.

Mitigation: Run the skill with appropriate filesystem permissions and periodically review or clean generated cache and report files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/nba-analyst)
- [ClawHub publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [Text, Analysis, Files]

**Output Format:** [Chinese-language plain text tables and local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report mode writes HTML files, and data queries may create local cache files inside the skill package.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
