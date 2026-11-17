## Description:

A Chinese-language coding assistant for code generation, debugging, and code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangtaoid](https://clawhub.ai/user/jiangtaoid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft code, diagnose errors, and review code quality in Chinese-language coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese coding trigger phrases may invoke the skill during normal coding conversations.

Mitigation: Use it in workspaces where a Chinese coding assistant is expected, and review whether trigger phrases overlap with other installed skills.

Risk: Users may paste secrets or proprietary code while requesting debugging or review help.

Mitigation: Avoid sharing sensitive code or credentials with the assistant runtime unless that use is approved for the workspace.

Risk: Generated code and review guidance may be incomplete or incorrect for a specific project.

Mitigation: Review, test, and scan suggested code before using it in production.

## Reference(s):

- [Popeye Coding ClawHub skill page](https://clawhub.ai/jiangtaoid/skills/popeye-coding)
- [Code generation module](artifact/modules/generate.md)
- [Debugging module](artifact/modules/debug.md)
- [Code review module](artifact/modules/review.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with code blocks and structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential access, or hidden data handling is included in the artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
