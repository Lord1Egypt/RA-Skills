## Description:

Openclaw Memory Stack is an OpenClaw memory plugin that provides local multi-engine memory search, structured fact extraction, deduplication, cross-agent sharing, and self-healing maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apptah](https://clawhub.ai/user/apptah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent local memory recall, project-aware search, structured fact capture, and controlled memory sharing across agent tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent memory plugin that can read and write OpenClaw memory and change OpenClaw plugin configuration.

Mitigation: Review the installer and configuration changes before installation, use a controlled OpenClaw profile, and back up existing memory/configuration data before enabling it.

Risk: Security evidence flags unsafe command execution paths and installer/update behavior that require review.

Mitigation: Review or disable installer and update paths before deployment, install dependencies through approved channels, and verify update packages and checksums.

Risk: Optional cloud LLM fallback can send conversation excerpts to a configured endpoint when API keys are present.

Mitigation: Avoid setting cloud API keys unless remote fact extraction is intended, prefer local Ollama or MLX endpoints for sensitive work, and verify the configured LLM endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apptah/skills/openclaw-memory-stack)
- [Openclaw Memory Stack repository](https://github.com/Apptah/openclaw-memory-stack)
- [License](https://github.com/Apptah/openclaw-memory-stack/blob/main/LICENSE)
- [Support issues](https://github.com/Apptah/openclaw-memory-stack/issues)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with optional JSON tool results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are memory recall, search, health, graph, expertise, consolidation, and setup guidance for OpenClaw agents.]

## Skill Version(s):

0.6.1 (source: server release evidence, SKILL.md frontmatter, plugin package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
