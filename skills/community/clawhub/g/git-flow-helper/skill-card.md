## Description: <br>
Assist with Git branch management, merging, rebasing, cherry-picking, and cleaning merged branches for smoother workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for Git workflow assistance, including branch creation, merges, rebases, cherry-picks, conflict-oriented workflow guidance, and cleanup of merged local branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run repository-changing Git commands without enough safeguards. <br>
Mitigation: Review each command manually, confirm the target repository and branch state, and avoid running commands with uncommitted work unless it has been intentionally preserved. <br>
Risk: Branch names, commit values, or other Git parameters from untrusted sources could be unsafe. <br>
Mitigation: Do not pass untrusted branch names or commit identifiers; validate inputs against expected Git refs or hashes before use. <br>
Risk: The merged-branch cleanup behavior can delete local branches. <br>
Mitigation: List the exact branches with git branch --merged first, exclude protected or active branches, and only then run deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HonestQiao/git-flow-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown text with inline shell commands and command-oriented examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository-changing Git commands that require manual review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
