## Description:

AI图文视频理解与生文专家 uses LinkFox large-language models to generate text and analyze prompts with optional image or video URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to generate product copy, translations, summaries, data-analysis text, and image or video content analyses through LinkFox's asynchronous text-generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable LinkFox gateway can receive the API key, prompts, media URLs, and session metadata.

Mitigation: Use the skill only when LINKFOX_TOOL_GATEWAY is unset or explicitly points to a trusted HTTPS LinkFox gateway, especially with production keys.

Risk: Prompts and media URLs may be remotely processed by the LinkFox service.

Mitigation: Avoid submitting secrets, confidential prompts, or private media unless remote processing is acceptable for the use case.

Risk: Large outputs may be saved locally and reused in chained image or video workflows.

Mitigation: Review saved output paths and downstream parameters before chaining sensitive generated content into other AIGC skills.

## Reference(s):

- [AI 生文 API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-textgen)
- [LinkFox API Key Setup Guide](https://skill.linkfox.com/linkfoxskills/guide.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON response or plain text content, with large responses saved locally and summarized in a JSON envelope.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous task creation and polling; generated content has newline characters encoded as a single-line placeholder for chaining into downstream AIGC skills.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
