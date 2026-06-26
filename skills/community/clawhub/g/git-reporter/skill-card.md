## Description: <br>
Git Reporter analyzes local Git history, branch state, and worktree changes to generate daily standups, weekly reports, or Sprint reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximum2974](https://clawhub.ai/user/maximum2974) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn local repository activity into concise status reports for standups, weekly updates, and Sprint reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may expose sensitive repository metadata such as commit messages, branch names, stash labels, author information, or file paths. <br>
Mitigation: Review each generated report before sharing it outside the intended team or system. <br>
Risk: The skill reads local working-tree and git history state, including uncommitted summaries. <br>
Mitigation: Run it only in repositories where the agent is allowed to inspect git metadata and worktree summaries. <br>
Risk: Report conclusions are inferred from local git data and may miss work that happened outside the current clone or fetched history. <br>
Mitigation: Treat generated standups and reviews as drafts and confirm important status, blockers, and team activity before publishing. <br>


## Reference(s): <br>
- [Git Reporter ClawHub release](https://clawhub.ai/maximum2974/git-reporter) <br>
- [Git Reporter README](artifact/README.md) <br>
- [Daily standup example](artifact/examples/daily.md) <br>
- [Weekly report example](artifact/examples/weekly.md) <br>
- [Sprint review example](artifact/examples/sprint.md) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with headings, bullets, tables, and inline git-derived metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports daily, weekly, and Sprint report modes; can filter by author or summarize team activity from local repository history.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
