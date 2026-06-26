## Description: <br>
Automatically generates standardized Git commit messages by analyzing staged Git changes, with support for Chinese and English Conventional Commits output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oct1st85](https://clawhub.ai/user/oct1st85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to draft Conventional Commit messages from staged Git changes during routine coding, team collaboration, open source contribution, and code review preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Git status and staged diffs, which may include secrets or sensitive private implementation details. <br>
Mitigation: Invoke it explicitly only in repositories and changesets you are comfortable exposing, and avoid using it on staged changes that contain secrets or confidential data. <br>
Risk: Generated commit messages can misstate the intent or business meaning of a change. <br>
Mitigation: Review and edit the proposed message before using it in a Git commit. <br>
Risk: Broad trigger wording could cause the skill to run in situations where commit-message generation was not intended. <br>
Mitigation: Use explicit prompts and confirm the skill output is only applied to the intended staged changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oct1st85/git-commit-helper-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted Conventional Commit message with an optional bullet-list body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English output; generated messages should be reviewed before committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
