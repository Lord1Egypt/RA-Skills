## Description:

M5Stack official technical support and development assistant for answering product specifications, pinouts, compatibility, troubleshooting, and development questions using M5Stack official MCP evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to answer M5Stack hardware, software, and integration questions from official MCP search or answer results, and to submit reproducible feedback when official material is missing, conflicting, or broken.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: M5Stack support queries are sent to M5Stack's official MCP service, and search or answer usage may be logged for maintenance statistics.

Mitigation: Redact credentials, Wi-Fi passwords, customer data, private logs, serial numbers, proprietary code, and other sensitive information before using MCP search or answer tools.

Risk: Incomplete, incorrect, conflicting, or broken official material can lead to unsupported technical conclusions.

Mitigation: Use MCP evidence before answering, state when official material does not confirm a claim, and submit reproducible feedback through knowledge_feedback for confirmed documentation or tool issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyun2000/skills/m5stack-assistant)
- [M5Stack official documentation](https://docs.m5stack.com)
- [M5Stack GitHub](https://github.com/m5stack)
- [M5Stack MCP service](https://mcp.m5stack.com)
- [M5Stack Arduino Programming Reference](references/quick-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in M5Stack official MCP results and should note when official material does not confirm a claim.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
