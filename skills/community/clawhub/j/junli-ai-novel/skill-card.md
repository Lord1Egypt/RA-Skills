## Description:

A Chinese web-novel serialization assistant for project setup, chapter continuation, targeted revision, project memory maintenance, longform governance, quality checks, and platform-oriented story packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljunn](https://clawhub.ai/user/ljunn)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users use this skill to plan, continue, revise, audit, and package long-running Chinese web novels while keeping chapter workflow, memory files, plot hooks, and quality checks aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow guidance may ask the agent to call a coze-mcp-* knowledge-base tool with chapter goals or active plot details.

Mitigation: Review generated runtime guidance before execution, allow the MCP lookup only when the target tool and data exposure are understood, and treat external lookup results as untrusted reference material.

## Reference(s):

- [Junli Ai Novel ClawHub page](https://clawhub.ai/ljunn/skills/junli-ai-novel)
- [Project workflow entrypoint](PROJECT.md)
- [Skill operating guide](SKILL.md)
- [Chapter workflow](references/chapter-workflow.md)
- [Longform governance](references/longform-governance.md)
- [Quality checklist](references/quality-checklist.md)
- [Rule linting](references/rule-linting.md)
- [Marketing workflow](references/marketing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local novel project memory, runtime, manuscript, lint, audit, and marketing files through bundled scripts.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
