## Description:

Analyzes images and video URLs with Zhipu GLM-V models to generate copy-ready prompts for text-to-image and text-to-video tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative operators use this skill to turn reference images or video URLs into prompts for AI image and video generation systems. It is suited for prompt engineering workflows that need visual analysis, prompt suggestions, and optional saved Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends provided images or video URLs to Zhipu's cloud API using the configured API key.

Mitigation: Use only media appropriate for Zhipu's service, avoid sensitive local images or private video URLs, and avoid broadly shared API keys.

Risk: The security summary notes that the documented default model appears inconsistent with the code.

Mitigation: Confirm the intended model explicitly with the model option when model choice affects output quality, cost, or policy requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/skills/glmv-prompt-gen)
- [GLM-V Prompt Gen Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-prompt-gen)
- [Zhipu Chat Completions API Documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
- [Zhipu API Key Management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with content analysis and prompt sections; optionally saved to a Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image, video, and auto modes; default max output token setting is 2048.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
