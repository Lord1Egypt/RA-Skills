## Description:

Automate GitHub contributions by finding good first issues, analyzing projects, forking, implementing fixes, and submitting pull requests efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thatgfsj](https://clawhub.ai/user/thatgfsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find suitable open-source issues, plan contributions, and run GitHub workflows for forking, branching, implementing, testing, and submitting pull requests. It can also guide optional recurring contribution searches when the user explicitly wants scheduled activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use the user's GitHub identity to fork repositories, push branches, and create pull requests.

Mitigation: Use a GitHub token with only the permissions needed for the intended repositories and review proposed GitHub operations before execution.

Risk: The optional cron workflow can create recurring account activity.

Mitigation: Enable scheduled activity only after explicit user approval, document how to inspect or remove the schedule, and periodically review whether it is still needed.

Risk: Broad cleanup guidance could affect unrelated local work if run from the wrong directory.

Mitigation: Run the skill in a dedicated workspace and review cleanup commands before allowing deletion or file-removal steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thatgfsj/skills/github-pr-automation)
- [Publisher Profile](https://clawhub.ai/user/thatgfsj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, issue comments, commit messages, PR descriptions, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands, GitHub API calls, local git commands, candidate issue recommendations, and optional cron configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
