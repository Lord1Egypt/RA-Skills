## Description:

Github Stars Tracker helps agents monitor GitHub repository stars, forks, and watchers, record local history, and report metric changes through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to add, list, check, and inspect GitHub repositories whose stars, forks, and watchers they want to track over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI reads GITHUB_TOKEN when it is set and uses it for GitHub API requests.

Mitigation: Use a minimally scoped GitHub token and confirm the skill is only sending it to GitHub's API before installation.

Risk: The CLI writes repository tracking state to ~/.github-stars-tracker.json.

Mitigation: Review the local state file location and avoid placing sensitive repository names in tracked entries when that file may be shared or backed up.

Risk: The current implementation appears to print changes rather than provide real notifications or complete trend analysis.

Mitigation: Validate the CLI behavior before relying on notification or trend-analysis claims in an operational workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/github-stars-tracker)
- [GitHub Repository API Endpoint](https://api.github.com/repos/{owner}/{repo})
- [GitHub Token Settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes tracked repository state to ~/.github-stars-tracker.json when the bundled CLI is run.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
