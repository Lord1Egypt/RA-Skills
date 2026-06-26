## Description: <br>
Weekly engineering retrospective that analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garrytan](https://clawhub.ai/user/garrytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate weekly or comparative retrospectives from local git history, including shipping metrics, team contribution patterns, code quality signals, and trend snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local git history and names individual contributors while producing people-focused feedback. <br>
Mitigation: Use it only in repositories and team settings where contributor analysis is expected, and get team consent before sharing growth or performance-style sections. <br>
Risk: Saved retro snapshots in memory/ may contain sensitive team metrics or contributor observations. <br>
Mitigation: Treat saved retro JSON files as sensitive project records and periodically review, restrict, or delete them according to team policy. <br>
Risk: Generated growth areas could be mistaken for formal performance evaluation. <br>
Mitigation: Use the output as retrospective guidance only and have humans review it before using or distributing people-focused feedback. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/garrytan/gstack-openclaw-retro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/garrytan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON files, Guidance] <br>
**Output Format:** [Telegram-oriented Markdown narrative with git metrics and a saved JSON retro snapshot] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local git commands, reads commit history and contributor names, and saves retro snapshots under memory/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
