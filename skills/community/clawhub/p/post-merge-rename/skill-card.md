## Description: <br>
Post-merge branch renaming. Appends --merged-YYYY-MM-DD to preserve history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to identify merged Git branches and rename them with dated suffixes after merge while preserving branch history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can delete old remote branch names after pushing renamed branches. <br>
Mitigation: Run --dry-run first, confirm the repository and origin remote, and require explicit approval before non-dry-run execution. <br>
Risk: Branch-name changes can disrupt CI, pull requests, links, audits, or protected workflows. <br>
Mitigation: Use it only on intentionally merged branches and make remote deletion opt-in or team-approved where branch names are operationally significant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/post-merge-rename) <br>
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with bash commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and bash; use --dry-run before changing branch names.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
