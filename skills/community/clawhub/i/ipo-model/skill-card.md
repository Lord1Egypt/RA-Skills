## Description:

IPO Model gives agents a recursive Input-Process-Output framework for structuring tasks, deciding when tools are needed, and producing text, plans, code, commands, or tool-use guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agent users can use this skill to break down broad tasks into recursive IPO trees, choose an execution mode, and decide whether a response should stay cognitive or use commands, scripts, tools, skills, or MCPs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The framework can lead an agent to propose commands, scripts, tool calls, skills, or MCP use for tasks that affect files or external services.

Mitigation: Keep normal confirmations, scoped permissions, and review in place before executing any proposed action.

Risk: A broad task-structuring method may produce plausible but incorrect plans when the input context is incomplete.

Mitigation: Review the generated IPO breakdown and final output against the user's actual constraints before relying on it.

## Reference(s):

- [IPO Model examples](artifact/references/examples.md)
- [ClawHub IPO Model skill page](https://clawhub.ai/wangjiaocheng/skills/ipo-model)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with IPO trees, code blocks, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to final results unless the user asks to see the IPO breakdown.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
