## Description: <br>
Automates Git workflow support for checking repository status, identifying file changes, generating commit messages, committing changes, pushing to remotes, and coordinating multiple repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[broommonk](https://clawhub.ai/user/broommonk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Git commits, inspect repository state, produce conventional commit messages, push changes, and troubleshoot common Git setup, authentication, and conflict issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage, commit, and push repository changes without clear approval safeguards. <br>
Mitigation: Require the agent to show `git status`, relevant diffs, exact staged files, generated commit message, target branch, and remote URL before committing, and require explicit approval before any push. <br>
Risk: Broad staging commands such as `git add .` can include sensitive or unintended files. <br>
Mitigation: Prefer explicit file staging in sensitive repositories and review staged changes before commit. <br>


## Reference(s): <br>
- [Git Workflow on ClawHub](https://clawhub.ai/broommonk/git-workflow) <br>
- [Repository listed in skill.yaml](https://git.kingcms.cn/OpenClaw/Skills-Collection) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Git commands that stage, commit, and push repository changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
