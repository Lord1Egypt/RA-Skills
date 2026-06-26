## Description: <br>
Git Standup Summary generates daily or weekly standup-ready status reports from local Git commit history by grouping recent work by type, scope, author, and time window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, scrum masters, and managers use this skill to turn recent repository activity into concise daily, weekly, team, branch, author, or date-range standup summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries can reveal private commit messages, author names, branch names, and file paths. <br>
Mitigation: Use the skill only in repositories whose history is appropriate to summarize, and review the generated standup text before sharing it. <br>
Risk: Summaries may omit context when the repository has large history or inconsistent commit messages. <br>
Mitigation: Check the underlying commit range when accuracy matters, especially before using the summary for formal reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/git-standup-summary) <br>
- [Skill homepage](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown standup summary with commit groupings, counts, authors, areas, and status-report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and reads local repository history for the requested time window, branch, author, or range.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
