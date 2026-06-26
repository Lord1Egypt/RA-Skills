## Description: <br>
查询主流大模型开放平台的 API 文档入口与精简调用要点，适用于月之暗面 Kimi、阿里云百炼、硅基流动、DeepSeek、OpenRouter 等平台，用于回答鉴权方式、base URL、OpenAI 兼容调用、聊天补全、模型名、常见差异、多平台对比与文档入口。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huixiaheyu](https://clawhub.ai/user/huixiaheyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find official API documentation, authentication details, base URLs, OpenAI-compatible migration notes, and minimal examples for major model platforms. It is also useful for comparing platform capabilities and drafting concise integration guides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may call external model-platform APIs and send prompts or other input to third-party services. <br>
Mitigation: Use test prompts first, keep API keys out of source code, and confirm each provider's privacy and retention policies before using real data. <br>
Risk: Model names, prices, preview states, and feature support can change quickly. <br>
Mitigation: Verify current capabilities, pricing, and deprecation status against official provider documentation before relying on guidance. <br>
Risk: Copied API examples can expose sensitive credentials if keys are hard-coded or checked into repositories. <br>
Mitigation: Use environment variables or a secrets manager, avoid committing credentials, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huixiaheyu/model-platform-guide) <br>
- [Reference index](references/index.md) <br>
- [Capability matrix](references/capability-matrix.md) <br>
- [Platform comparison](references/comparison.md) <br>
- [Live check policy](references/live-check-policy.md) <br>
- [Model, search, and embeddings checklist](references/model-search-embedding-checklist.md) <br>
- [OpenAI migration template](references/openai-migration.md) <br>
- [Python recipes](references/python-recipes.md) <br>
- [Node.js recipes](references/nodejs-recipes.md) <br>
- [curl recipes](references/curl-recipes.md) <br>
- [Moonshot / Kimi reference](references/moonshot.md) <br>
- [Aliyun Bailian / DashScope reference](references/aliyun-bailian.md) <br>
- [SiliconFlow reference](references/siliconflow.md) <br>
- [DeepSeek reference](references/deepseek.md) <br>
- [OpenRouter reference](references/openrouter.md) <br>
- [BigModel reference](references/bigmodel.md) <br>
- [Volcengine Ark reference](references/ark.md) <br>
- [Tencent Hunyuan reference](references/hunyuan.md) <br>
- [Baidu Qianfan reference](references/qianfan.md) <br>
- [MiniMax reference](references/minimax.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include official documentation links, API base URLs, environment variable names, minimal request examples, migration notes, and comparison tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
