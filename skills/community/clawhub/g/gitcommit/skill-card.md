## Description: <br>
Generate precise git commit messages following Conventional Commits with auto language detection, scope inference, and multi-module support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlykan](https://clawhub.ai/user/wlykan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect repository changes, infer Conventional Commit type and scope, and draft commit messages or user-approved git commit commands that match project language and style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads git status, diffs, and recent commit history, which may expose private code or secrets to the agent context. <br>
Mitigation: Use it only in repositories where sharing change context with the agent is acceptable, and review diffs for secrets or private data before requesting commit assistance. <br>
Risk: Generated git add and git commit commands may include unintended files or produce an inaccurate commit message. <br>
Mitigation: Review the proposed file list, grouping, scope, and commit text before approving any command execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wlykan/gitcommit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with git commit messages and optional bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include grouped git add and git commit proposals for explicit user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
