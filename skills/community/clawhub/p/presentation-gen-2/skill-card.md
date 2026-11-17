## Description:

演示文稿生成工具 helps agents generate professional HTML and PDF presentations from Markdown, URLs, or topics, with Chinese-language interaction support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill to turn Markdown, URLs, or topic prompts into exportable presentation outputs. It is intended for presentation generation and related document-conversion workflows, not for complex decisions that require human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broad read, write, and command authority for a presentation-generation skill.

Mitigation: Review the skill before installation and approve only the file access and command execution needed for the intended presentation workflow.

Risk: The skill can process local files or URLs that may contain sensitive or unintended content.

Mitigation: Use only explicit input files or URLs intended for processing, and avoid sensitive documents unless they are required for the task.

Risk: External API or command use can affect privacy, cost, or local system behavior.

Mitigation: Confirm any external API use or command execution before allowing the agent to proceed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/presentation-gen-2)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON status objects, Markdown guidance, and generated HTML/PDF presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use read, write, and command-execution authority while processing supplied content.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
