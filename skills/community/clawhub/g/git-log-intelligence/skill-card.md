## Description: <br>
Fetch, filter, and summarize GitHub repository activity without cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickludlam](https://clawhub.ai/user/nickludlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review recent GitHub repository activity, summarize important commits, and maintain reusable ignore patterns for noisy bot, CI, chore, documentation, or test commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub personal access token and calls the GitHub CLI to retrieve repository commit history. <br>
Mitigation: Use the narrowest token scope possible, such as public_repo for public repositories and repo only when private repository access is required. <br>
Risk: Persistent ignore patterns can hide important commits if old or broad filters remain in place. <br>
Mitigation: Review the ignore list periodically with the show command and remove stale or overly broad patterns. <br>
Risk: Detailed summaries may include private repository commit messages when used with private repository access. <br>
Mitigation: Treat generated summaries as repository-sensitive output and avoid sharing them outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickludlam/git-log-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style commit summaries with shell command examples and ignore-list guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include filtered commit counts, capped result warnings, short commit subjects, authors, SHA prefixes, and optional truncated full commit messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
