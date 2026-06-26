## Description: <br>
Openclaw Retro generates periodic engineering delivery retrospectives from git history and code quality signals across 24h, 7d, 14d, and 30d windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate periodic retrospectives that summarize delivery metrics, contributor activity, hotspots, backlog health, and next-focus recommendations from repository history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated retrospectives may include contributor metadata, git history, test structure, TODO/backlog notes, or confidential roadmap details. <br>
Mitigation: Run the skill only on repositories where that inspection is acceptable, and review the generated retro before sharing it outside the team. <br>
Risk: Repository inspection can surface sensitive personal contributor data or project details in the output. <br>
Mitigation: Avoid using the skill on repositories containing sensitive personal data or confidential roadmap information unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Openclaw Retro on ClawHub](https://clawhub.ai/x-rayluan/openclaw-retro) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with metrics tables, contributor sections, histograms, hotspot analysis, backlog review, summary, and status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 24h, 7d, 14d, and 30d windows; defaults to 7d when no window is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
