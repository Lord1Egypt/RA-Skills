## Description: <br>
Guides users through permanently removing files from Git repository history with git filter-repo, including backups, verification, force pushes, and follow-up handling for exposed secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhjin](https://clawhub.ai/user/hhjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need operational guidance for removing sensitive files, large files, or other unwanted paths from all Git branches and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History-rewrite commands and force pushes can disrupt collaborators or remove expected repository state. <br>
Mitigation: Confirm the repository and target paths, make a full backup, notify collaborators, and review commands before execution. <br>
Risk: Removing a secret from Git history does not guarantee the secret was never copied. <br>
Mitigation: Revoke exposed credentials, generate replacements, and check forks, CI/CD caches, and local clones. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhjin/git-clear-committed-file-history) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for repository confirmation before destructive history-rewrite steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
