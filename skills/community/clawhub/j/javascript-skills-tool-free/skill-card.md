## Description:

面向个人开发者的JavaScript代码风格指南,涵盖核心规则与基础代码审查能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual JavaScript users use this skill to generate style-compliant JavaScript snippets, review pasted JavaScript for common style issues, and receive concise explanations of core conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review classifies the release as suspicious because it grants broader tool and workflow authority than a passive JavaScript style guide clearly requires.

Mitigation: Review the skill before installing, restrict use to JavaScript style review or snippet generation, and avoid allowing it to run commands or modify files automatically.

Risk: The artifact describes command execution and file modification pathways through agent tools.

Mitigation: Require explicit user approval for file writes and command execution, and use allowlisted commands when linting or formatting code.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/javascript-skills-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, JSON, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as review guidance or generated snippets; file changes and command execution should remain user-controlled.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
