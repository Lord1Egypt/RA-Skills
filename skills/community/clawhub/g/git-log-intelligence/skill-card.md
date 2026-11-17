## Description:

Fetches, filters, and summarizes GitHub repository activity without cloning while maintaining persistent ignore patterns for bot, CI, documentation, and chore noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickludlam](https://clawhub.ai/user/nickludlam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect recent GitHub repository activity, summarize meaningful repository changes, and maintain local ignore patterns for routine bot, CI, documentation, and chore noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a GitHub API token through the GitHub CLI.

Mitigation: Use a fine-grained read-only token limited to the repositories the agent needs to inspect.

Risk: The skill stores persistent local ignore patterns that can hide relevant commits.

Mitigation: Review the ignore list periodically and remove patterns that are too broad or no longer appropriate.

Risk: Commit text returned by GitHub can contain untrusted content.

Mitigation: Treat retrieved commit messages as source material to summarize, not instructions for the agent to follow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickludlam/skills/git-log-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown or structured text summaries with inline shell commands for filter management]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commit messages are filtered by persistent local ignore patterns; full commit messages are truncated to 1000 characters and displayed commits are capped at 200.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
