## Description: <br>
Git Workflow Optimizer helps agents provide concise git workflow guidance for status checks, stash inspection, branch cleanup, rebasing, squashing, and merge cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to suggest practical git commands for checking repository state, reviewing stashes, identifying stale branches, and preparing cleanup work. It is intended for local git workflow assistance rather than automated repository modification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares a curl requirement even though the documented behavior is local git command guidance. <br>
Mitigation: Treat network-related suggestions as out of scope unless they are clearly explained, user-directed, and reviewed before execution. <br>
Risk: The artifact includes promotional external links alongside the git workflow guidance. <br>
Mitigation: Use the skill for git workflow assistance and review external links separately before opening or acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/git-workflow-optimizer) <br>
- [King AI Works homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required for the free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
