## Description:

Automatically switches between cloud and local LLMs when rate limits occur, with explicit user confirmation before local code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhardie](https://clawhub.ai/user/dhardie)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to keep OpenClaw agents available when cloud LLM providers hit rate limits by switching new agents to a local Ollama model. It makes local code-generation work visible by requiring a confirmation phrase before code-oriented tasks proceed in local mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local-mode code tasks may proceed without a deliberate user approval because the confirmation gate is weak.

Mitigation: Treat the confirmation phrase as a best-effort control; review local-mode code work before execution and prefer cloud mode for production code changes until the gate is hardened.

Risk: A weaker local model may reduce code-generation quality after automatic fallback from cloud LLMs.

Mitigation: Use `/llm status` to confirm the active mode, switch back to cloud with `/llm switch cloud` for sensitive code work, and review generated changes before applying them.

## Reference(s):

- [LLM Supervisor ClawHub release](https://clawhub.ai/dhardie/skills/llm-supervisor-agent)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-formatted command replies and notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update agent LLM profile selection between cloud Anthropic and local Ollama modes; local code tasks depend on a configurable confirmation phrase.]

## Skill Version(s):

0.2.0 (source: server release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
