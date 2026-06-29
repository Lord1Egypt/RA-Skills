## Description: <br>
Guides an agent to make precise code edits by reading context first, applying minimal diffs, and checking the result after changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill when modifying existing files, fixing bugs, or refactoring while keeping edits small, targeted, and reviewable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code changes can affect the wrong location or introduce unrelated diffs if the agent edits without first reading the target context. <br>
Mitigation: Require the agent to read the relevant file section, match replacement text precisely, and keep each edit narrowly scoped. <br>
Risk: Sensitive maintenance actions or externally shared review bundles may have operational or disclosure impact if executed casually. <br>
Mitigation: Follow the security guidance for confirmation and dry-run steps before bans, restores, ownership changes, email sending, production migrations, or external review handoffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-edit) <br>
- [Skill-supplied homepage](https://github.com/zhaobod1/huo15-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with code and shell-command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Promotes small, targeted edits followed by rereading and validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
