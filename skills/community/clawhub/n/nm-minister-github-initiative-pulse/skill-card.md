## Description: <br>
Generates markdown digests and CSV exports for GitHub initiative health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and project leads use this skill to turn tracker data and GitHub project metadata into initiative status summaries, GitHub comments, and CSV exports for stakeholder updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be activated for GitHub reporting tasks where broad repository or project access would expose more data than needed. <br>
Mitigation: Confirm the reporting scope before use and limit GitHub access to the repositories, projects, milestones, or issues needed for the requested report. <br>
Risk: Generated status digests can be misleading when tracker data or GitHub board metadata is stale or incomplete. <br>
Mitigation: Refresh or verify source data, review metrics and linked risks, and check rendered Markdown before posting updates to GitHub threads. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister) <br>
- [GitHub Comment Snippets](modules/github-comment-snippets.md) <br>
- [Status Digest Blueprint](modules/status-digest.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, CSV, guidance] <br>
**Output Format:** [Markdown digests, GitHub comment snippets, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include issue, pull request, project, milestone, owner, lane, and risk-query references supplied by the user or tracker data.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
