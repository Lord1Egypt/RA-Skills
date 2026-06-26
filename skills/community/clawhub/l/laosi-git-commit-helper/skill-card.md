## Description: <br>
Git Commit Helper Pro helps developers inspect repository status, summarize diffs, list branches and history, and generate Conventional Commits-style commit messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to streamline everyday Git workflows, including checking changes, reviewing diffs, browsing branch or commit history, and preparing Conventional Commits-style messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The commit workflow can stage all tracked, untracked, and deleted files and create a commit without clearly requiring user confirmation. <br>
Mitigation: Review repository status and staged files before committing, and require explicit user approval before running staging or commit commands. <br>
Risk: Repositories may contain secrets, unrelated changes, or work that should not be included in a broad commit. <br>
Mitigation: Avoid broad staging in sensitive repositories; manually stage only intended files or inspect the generated status and diff output first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-git-commit-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with generated commit text, Git workflow summaries, and code or command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Git staging and commit actions when the user asks for commit automation.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
