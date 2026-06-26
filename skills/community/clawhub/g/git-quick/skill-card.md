## Description: <br>
Show a quick summary of the current git repo: branch, status, recent commits, and contributor stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackeryht](https://clawhub.ai/user/hackeryht) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly inspect a local Git repository's branch state, file status, recent commit history, and top contributors from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prints local repository details such as changed file names, recent commit messages, and contributor names. <br>
Mitigation: Run it only in repositories where displaying that metadata in the terminal is acceptable. <br>
Risk: The skill depends on local git history and branch configuration, so output can be incomplete or fail outside a Git repository. <br>
Mitigation: Use it from inside the intended repository and confirm the reported state before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackeryht/git-quick) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain terminal text with documented bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the git binary and a local Git repository; supports --short, --commits, and --stats output modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
