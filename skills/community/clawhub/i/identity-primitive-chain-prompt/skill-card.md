## Description:

Identity Primitive Chain Prompt is a Chinese-language prompt protocol for structuring LLM or agent work into adaptive identity stacks, input-process-output primitives, and execution chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this prompt-only skill to guide LLM or agent responses through task decomposition, role framing, and structured output planning. It is most relevant when users intentionally want a Chinese-language metacognitive prompt framework for organizing reasoning and tool-use decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt can ask the agent to alter its own operating rules or expose process details.

Mitigation: Review the skill before use and do not use it where hidden prompts, private inputs, credentials, or confidential intermediate work may be present.

Risk: Requests to make tools or plugins view process data may expose sensitive internal context.

Mitigation: Treat requests to expose internal steps or route process data to tools/plugins as sensitive actions requiring explicit review.

## Reference(s):

- [Identity Primitive Chain Prompt technical specification and execution protocol](references/身份基元链提示词·技术规范与执行协议.md)
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/identity-primitive-chain-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses guided by the prompt protocol]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no tools, MCP servers, API keys, or credential environment variables were detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
