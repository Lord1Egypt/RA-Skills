## Description: <br>
Automates the backup of the OpenClaw workspace to a remote Git repository by validating Git configuration, excluding large files, and syncing local changes with conflict handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vemec](https://clawhub.ai/user/vemec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to back up an OpenClaw workspace or repository to its configured Git remote with preflight checks, large-file exclusions, commits, pulls, and pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage, commit, and push repository contents to the configured origin, which may publish unintended files or secrets. <br>
Mitigation: Review git status and git diff before running, keep secrets ignored, and confirm the remote repository is private and trusted. <br>
Risk: A remote URL that embeds credentials or points to an untrusted destination can expose sensitive access or repository data. <br>
Mitigation: Use SSH keys or a credential helper and verify the origin URL before syncing. <br>
Risk: Remote divergence or pull conflicts can interrupt synchronization. <br>
Mitigation: Run from the intended repository and branch, then resolve any reported conflicts manually before rerunning the sync. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured log examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured status messages use INFO, SUCCESS, WARNING, and ERROR prefixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
