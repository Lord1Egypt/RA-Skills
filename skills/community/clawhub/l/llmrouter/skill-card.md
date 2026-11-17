## Description:

Intelligent LLM proxy that routes requests to appropriate models based on complexity. Save money by using cheaper models for simple tasks. Tested with Anthropic, OpenAI, Gemini, Kimi/Moonshot, and Ollama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexrudloff](https://clawhub.ai/user/alexrudloff)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to install, configure, and operate an LLM routing proxy that selects models based on request complexity to reduce cost while preserving stronger models for harder tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to run external llmrouter code as a long-running local proxy that can process prompts and API credentials.

Mitigation: Review the external repository before installation, prefer a pinned and reviewed commit, and keep the service bound to localhost.

Risk: Configuration files, logs, or provider credentials could expose sensitive prompts or API tokens.

Mitigation: Protect configuration and log files, avoid unnecessary always-on service setup, and use local classification for sensitive prompts when possible.

## Reference(s):

- [llmrouter homepage](https://github.com/alexrudloff/llmrouter)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/alexrudloff/skills/llmrouter)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides users through local service setup, provider configuration, health checks, and troubleshooting.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
