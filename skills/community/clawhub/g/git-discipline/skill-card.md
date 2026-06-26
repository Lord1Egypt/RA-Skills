## Description: <br>
Apply safe Git workflow rules for the current local repository: branches, commits, staging, and history handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep local Git work focused, reversible, and safe when inspecting repository state, creating branches, preparing commits, reviewing staged changes, or managing history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Git commands could stage, commit, branch, or alter repository history in the current working tree. <br>
Mitigation: Review proposed Git commands before running them, especially in shared repositories. <br>
Risk: History-changing operations can affect shared branches or unrelated work. <br>
Mitigation: Avoid rewriting published history, do not force-push shared branches, and inspect repository state before acting. <br>


## Reference(s): <br>
- [Git Discipline on ClawHub](https://clawhub.ai/sf0799/git-discipline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current Git status, next safe operation, branch name or commit message suggestions, and explicit risk notes for history-changing requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
