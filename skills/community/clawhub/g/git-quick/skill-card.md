## Description:

Show a quick summary of the current git repo: branch, status, recent commits, and contributor stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackeryht](https://clawhub.ai/user/hackeryht)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly inspect a local Git repository's branch tracking state, working tree status, recent commits, and top contributors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can display local repository details such as file paths, commit subjects, branch tracking information, and contributor names.

Mitigation: Run it only in repositories where those details are appropriate to show in the current agent session or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hackeryht/skills/git-quick)
- [Publisher profile](https://clawhub.ai/user/hackeryht)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text Git summary with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the git CLI and reads local repository metadata without modifying repository state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
