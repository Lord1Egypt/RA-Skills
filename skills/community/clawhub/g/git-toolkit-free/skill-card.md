## Description: <br>
Provides Git commit, branch, merge, conflict-resolution, and history-recovery guidance for everyday developer version-control workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for Git command guidance and command execution plans for commits, feature branches, merges, conflict handling, and recovering from common history mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to change local Git history, push to remotes, delete remote branches, or alter global Git authentication and configuration. <br>
Mitigation: Require the agent to show the exact repository, branch, files, remote, and command before execution; do not allow credential.helper store or hard reset unless explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Git configuration, and gitignore code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable Git commands that require repository, branch, remote, file, and credential context review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
