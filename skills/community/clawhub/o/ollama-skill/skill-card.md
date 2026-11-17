## Description:

Integrates Ollama into coding agents, IDEs, and agent harnesses through local, on-premises, Docker, Ollama Cloud, and OpenAI/Anthropic-compatible API paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waiyannyeinnaing](https://clawhub.ai/user/waiyannyeinnaing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Ollama runtime integration to agent harnesses, IDE extensions, and application backends. It helps configure chat, streaming, structured outputs, embeddings, tool calling, web search, and provider-compatible client paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Docker setup can expose an unauthenticated Ollama API on port 11434 beyond the local machine.

Mitigation: Bind Ollama to 127.0.0.1 when possible, avoid exposing port 11434 to untrusted networks, and review network configuration before deployment.

Risk: Cloud mode and web search can send prompt, query, or workload data off-device.

Mitigation: Use local or on-premises deployment for sensitive data, keep cloud API key handling separate from local configuration, and disclose off-device data flow to users.

Risk: Dependencies and the container image are not pinned to exact versions in the artifact examples.

Mitigation: Pin package and container versions for repeatable installs, then rescan before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waiyannyeinnaing/skills/ollama-skill)
- [Ollama API](https://ollama.com/api)
- [Artifact skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, configuration snippets, and runnable example commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local or cloud Ollama endpoints and example files; outputs should avoid secrets.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
