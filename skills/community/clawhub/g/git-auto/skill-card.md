## Description: <br>
Git workspace automation (status/commit/push/log/diff) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Git status, summarize diffs and logs, create commits with generated messages, and push the current branch from an agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage and commit all workspace changes, including files the user did not intend to include. <br>
Mitigation: Inspect git status and diff before using commit actions, and run the skill only in repositories where automatic commits are acceptable. <br>
Risk: The skill can push the current branch without the sensitive-file, branch, conflict, or large-change safeguards described in its documentation. <br>
Mitigation: Review the target branch, remote state, and staged changes manually before push actions; do not rely on documented safeguards unless they are implemented in a future version. <br>


## Reference(s): <br>
- [Git Auto ClawHub page](https://clawhub.ai/mupengi-bot/git-auto) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify the active Git workspace by staging files, committing changes, and pushing the current branch.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
