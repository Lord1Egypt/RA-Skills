## Description:

Access Claude, Gemini, Kimi, GLM, and other language models through the inference.sh CLI using OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover and call OpenRouter-hosted language models for coding, writing, analysis, chat, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path includes mutable remote installation and unpinned package commands.

Mitigation: Prefer a manually downloaded, version-pinned, checksum- or signature-verified CLI release before installation.

Risk: Prompts and inputs may be sent through inference.sh, OpenRouter, and selected model providers.

Mitigation: Do not send secrets, regulated data, private source code, or sensitive prompts unless those services and providers are approved for the data.

## Reference(s):

- [Skill page](https://clawhub.ai/okaris/skills/llm-models)
- [inference.sh](https://inference.sh)
- [Manual install checksums](https://dist.inference.sh/cli/checksums.txt)
- [Agents Overview](https://inference.sh/docs/concepts/agents)
- [Agent SDK](https://inference.sh/docs/api/agent/overview)
- [Building a Research Agent](https://inference.sh/blog/guides/research-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model output depends on inference.sh, OpenRouter, and the selected provider.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
