## Description:

Invoke various LLMs such as GLM-5, Kimi-k2.5, Llama 3.1, Phi-4, and DeepSeek R1 through the NVIDIA NIM API to save main agent tokens and use specialized model capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d-wwei](https://clawhub.ai/user/d-wwei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to delegate prompts for summarization, long-form explanation, and reasoning to NVIDIA NIM-hosted models from OpenClaw or a direct command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included API helper disables HTTPS certificate and hostname verification while sending prompts and the NVIDIA API key.

Mitigation: Review before installing, avoid sensitive prompts or files, enable normal TLS verification before use on untrusted networks, and rotate the NVIDIA API key if this helper has already been used in risky network conditions.

## Reference(s):

- [NVIDIA Build](https://build.nvidia.com/)
- [NVIDIA NIM Chat Completions API endpoint](https://integrate.api.nvidia.com/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/d-wwei/skills/openclaw-nim-skill)
- [Publisher profile](https://clawhub.ai/user/d-wwei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown responses with command-line and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls external NVIDIA NIM-hosted chat completion models and the helper limits responses to 2048 tokens.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
