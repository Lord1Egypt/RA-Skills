## Description: <br>
Generates descriptive Conventional Commits-style commit messages by analyzing staged or unstaged git diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect staged or unstaged git diffs and draft concise Conventional Commits-style commit messages for repository changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git diffs may contain private code, configuration, or accidentally staged secrets. <br>
Mitigation: Use the skill only when the agent may inspect the relevant diff, and review staged changes for sensitive data before sharing or committing. <br>
Risk: Suggested commit messages can mischaracterize the intent or scope of a change. <br>
Mitigation: Review the generated message against the actual diff before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laimiaohua/gi-git-commit-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Conventional Commits-style commit message, optionally with a short Markdown body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be drafted in Chinese or English depending on the user's request and repository context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
