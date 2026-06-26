## Description: <br>
Git Toolkit provides bash-based helper commands for summarizing Git repositories, listing authors, generating changelogs, estimating file effort, and making selected repository changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they want an agent to inspect a local Git repository, produce repository summaries or changelog text, and propose or run simple Git utility commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-changing commands can alter local Git state, including appending to .gitignore, creating an orphan branch, or soft-resetting commits. <br>
Mitigation: Run git status first, confirm the intended repository and branch, and use ignore, fresh-branch, and undo only when those state changes are desired. <br>
Risk: Generated summaries and changelogs depend on the local repository history and Git configuration available to the agent. <br>
Mitigation: Review generated text before publishing or using it as release documentation. <br>


## Reference(s): <br>
- [Git Toolkit on ClawHub](https://clawhub.ai/ckchzh/git-toolkit) <br>
- [Publisher profile: ckchzh](https://clawhub.ai/user/ckchzh) <br>
- [tj/git-extras reference project](https://github.com/tj/git-extras) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text and Markdown with shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands inspect repository history; ignore, undo, and fresh-branch can modify Git state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
