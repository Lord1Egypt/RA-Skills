## Description: <br>
Fetch KBO game schedules and results for a specific date with the kbo-game npm package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5eun](https://clawhub.ai/user/5eun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch and summarize KBO schedules, scores, and game status for a specific date, including compact team-filtered scoreboard responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs the third-party npm package kbo-game globally. <br>
Mitigation: Review or pin the npm package version before use, especially in locked-down or sensitive environments. <br>
Risk: KBO site changes or package response changes can break or alter returned scoreboard data. <br>
Mitigation: Check date-specific results for plausibility and provide raw JSON when the user needs verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/5eun/kbo-results) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with compact scoreboard summaries and optional inline shell commands or JSON excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter results by date and, when requested, by team.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
