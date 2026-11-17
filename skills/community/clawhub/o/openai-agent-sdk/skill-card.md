## Description:

Build multi-agent AI systems with OpenAI Agents SDK using tools, handoffs, guardrails, tracing, and LiteLLM-backed model integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendwealth](https://clawhub.ai/user/sendwealth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create OpenAI Agents SDK applications, including multi-agent routing, tool calling, handoffs, guardrails, tracing, voice agents, and reusable agent templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an eval-based calculator example that can execute arbitrary Python code if copied directly.

Mitigation: Replace the eval-based calculator before use with a constrained parser, allowlisted operations, or another safe computation implementation.

Risk: Agent runs may expose API keys, traces, or conversation history through logs or debugging output.

Mitigation: Keep API keys out of logs and sanitize traces, debug output, and conversation history before sharing or storing them.

Risk: Unpinned or broadly ranged dependencies can change behavior over time.

Mitigation: Install dependencies in an isolated environment and pin package versions for production deployments.

## Reference(s):

- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK GitHub repository](https://github.com/openai/openai-agents-python)
- [OpenAI Agents SDK examples](https://github.com/openai/openai-agents-python/tree/main/examples)
- [openai-agents on PyPI](https://pypi.org/project/openai-agents/)
- [ClawHub skill page](https://clawhub.ai/sendwealth/skills/openai-agent-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples and templates for Python >=3.10 with openai-agents >=0.1.0.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
