## Description:

Provides concise, link-first guidance for API documentation, authentication, base URLs, OpenAI-compatible calls, model names, platform differences, comparisons, and integration examples across major model platforms such as Kimi, DashScope, SiliconFlow, DeepSeek, and OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huixiaheyu](https://clawhub.ai/user/huixiaheyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find current model-platform API documentation, compare provider-specific authentication and base URL requirements, and draft concise integration examples. It is especially useful for OpenAI-compatible migration, provider selection, and capability checks that require official documentation links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated curl, Python, or Node.js examples can send prompts and request data to third-party model providers.

Mitigation: Confirm the destination provider is approved for the use case and avoid sending secrets, regulated data, or private user content unless that provider is authorized.

Risk: Model availability, prices, preview status, rate limits, and feature support can change quickly.

Mitigation: Use the skill's live-check policy and verify current provider documentation before making claims about latest models or capabilities.

Risk: OpenAI-compatible integrations can fail when the API key, base URL, endpoint path, or model name is copied for the wrong provider.

Mitigation: Review provider-specific authentication, base URL, endpoint, and model-name requirements before running generated examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huixiaheyu/skills/model-platform-guide)
- [Document Entry Index](references/index.md)
- [Dynamic Verification Policy](references/live-check-policy.md)
- [Model, Search, and Embeddings Checklist](references/model-search-embedding-checklist.md)
- [Platform Capability Matrix](references/capability-matrix.md)
- [Platform Comparison](references/comparison.md)
- [Python Recipes](references/python-recipes.md)
- [Node.js Recipes](references/nodejs-recipes.md)
- [curl Recipes](references/curl-recipes.md)
- [OpenAI Migration Template](references/openai-migration.md)
- [Moonshot / Kimi Documentation](https://platform.kimi.com/docs/overview.md)
- [Alibaba Cloud Model Studio API Reference](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)
- [SiliconFlow Documentation](https://docs.siliconflow.cn/)
- [DeepSeek API Documentation](https://api-docs.deepseek.com/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [BigModel Documentation](https://docs.bigmodel.cn/)
- [Volcengine Ark Documentation](https://www.volcengine.com/docs/82379)
- [Tencent Hunyuan Documentation](https://cloud.tencent.com/document/product/1729)
- [Baidu Qianfan Documentation](https://cloud.baidu.com/doc/qianfan/index.html)
- [MiniMax Documentation](https://platform.minimaxi.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with links, tables, inline code, and short Python, Node.js, or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend live verification against official provider documentation for model lists, prices, rate limits, preview status, and fast-changing capabilities.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
