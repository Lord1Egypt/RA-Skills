## Description: <br>
Generates markdown digests and CSV exports for GitHub initiative health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and project leads use this skill to turn tracker data and GitHub board metadata into initiative status digests, scorecards, blocker summaries, PR watchlists, and CSV-style exports for GitHub issues, pull requests, or Discussions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as github, projects, reporting, status, and dashboards may invoke the skill unexpectedly. <br>
Mitigation: Confirm the requested task is GitHub initiative reporting before using the generated templates or summaries. <br>
Risk: Generated digests may summarize project, stakeholder, or issue details that should not be posted broadly. <br>
Mitigation: Review and edit reports before pasting them into GitHub issues, pull requests, or Discussions. <br>
Risk: Outdated tracker or GitHub Projects data can produce misleading completion, blocker, or ETA summaries. <br>
Mitigation: Refresh tracker and GitHub data before generating stakeholder-facing status updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-minister-github-initiative-pulse) <br>
- [claude-night-market minister plugin](https://github.com/athola/claude-night-market/tree/master/plugins/minister) <br>
- [GitHub Comment Snippets](modules/github-comment-snippets.md) <br>
- [Status Digest Blueprint](modules/status-digest.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, checklists, GitHub comment snippets, and CSV export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before posting because they may summarize project or stakeholder information.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
