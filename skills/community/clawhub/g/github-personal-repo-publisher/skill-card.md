## Description: <br>
Create a repository under your own GitHub account, wire a local project repo to it, and push committed history safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grey0758](https://clawhub.ai/user/grey0758) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to publish a local Git project to a new personal GitHub repository, create the repository when needed, wire the remote, push committed history, and report any local-only work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create GitHub repositories, change a local origin remote, and push committed history. <br>
Mitigation: Confirm the GitHub owner grey0758, SSH alias github-grey0758, target repository name, and private or public visibility before invoking it. <br>
Risk: Committed history may contain secrets, proprietary files, or content that should not be uploaded to GitHub. <br>
Mitigation: Review the committed history and scan for sensitive material before allowing the push. <br>
Risk: The workflow uses a 1Password-stored GitHub PAT for API repository creation. <br>
Mitigation: Use the configured 1Password item only for the intended account and do not expose token values in prompts, logs, or files. <br>
Risk: Repository creation alone may be mistaken for a complete project publication. <br>
Mitigation: Treat pushed committed history as the publication boundary and explicitly report any uncommitted local-only work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grey0758/github-personal-repo-publisher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/grey0758) <br>
- [GitHub user repositories API endpoint](https://api.github.com/user/repos) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown status report with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local repository status, GitHub repository existence or creation status, remote wiring, push status, and remaining local-only work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
