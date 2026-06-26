## Description: <br>
Access Claude, Gemini, Kimi, GLM and 100+ LLMs via inference.sh CLI using OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to discover and call OpenRouter-backed LLMs through the inference.sh CLI for coding, writing, analysis, chat, and agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick start uses a remote installer for the inference.sh CLI. <br>
Mitigation: Review the installer before running it, or use the documented checksum-based manual installation path. <br>
Risk: Prompts and inputs may be processed by OpenRouter and downstream model providers. <br>
Mitigation: Do not send secrets, private code, credentials, or sensitive personal data unless that provider handling is acceptable for the use case. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [Manual install checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [Agents Overview](https://inference.sh/docs/concepts/agents) <br>
- [Agent SDK](https://inference.sh/docs/api/agent/overview) <br>
- [Building a Research Agent](https://inference.sh/blog/guides/research-agent) <br>
- [ClawHub release page](https://clawhub.ai/okaris/llm-models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses infsh CLI commands that may send prompts and inputs to OpenRouter and downstream model providers.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
