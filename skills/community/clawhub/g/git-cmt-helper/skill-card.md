## Description: <br>
Generate standardized git commit messages in Conventional Commits format with required type, project-module scope, subject, optional body, and breaking-change guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xtresser](https://clawhub.ai/user/0xtresser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to draft consistent git commit messages or commit proposals that follow team conventions for type prefixes, real module scopes, concise subjects, optional explanatory bodies, and breaking-change footers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated commit message may misstate the intent, scope, or breaking-change impact of the actual diff. <br>
Mitigation: Review the final commit message against the staged changes before accepting or using it. <br>
Risk: When an agent proposes an actual git commit command, it may commit unintended files or use an unreviewed message. <br>
Mitigation: Check git status and review any proposed git command before approving execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xtresser/git-cmt-helper) <br>
- [Publisher profile](https://clawhub.ai/user/0xtresser) <br>
- [Project Modules](references/modules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text commit message with optional git commit command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commit subjects are constrained to 72 characters including type and scope; scopes should come from the project module list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
