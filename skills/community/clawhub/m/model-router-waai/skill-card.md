## Description:

Model Router provides parallel multi-LLM invocation with result merging for comparing model outputs and producing a consolidated answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to invoke multiple LLMs in parallel, compare their responses, and merge successful outputs into a final result. It is suited to tasks where answer comparison or ensemble-style synthesis is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact describes real multi-model routing, but the included implementation simulates provider calls.

Mitigation: Review behavior before relying on outputs and confirm with the publisher whether simulation is intentional.

Risk: A future real-routing version may send prompts to multiple external LLM providers.

Mitigation: Avoid secrets, regulated data, and private code unless each provider is approved for that data.

Risk: The installation command is unpinned.

Mitigation: Use a pinned, verified install path and avoid elevated privileges during installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaibuer/skills/model-router-waai)
- [OpenAI Chat Completions API](https://api.openai.com/v1/chat/completions)
- [Anthropic Messages API](https://api.anthropic.com/v1/messages)
- [Moonshot Chat Completions API](https://api.moonshot.cn/v1/chat/completions)
- [DeepSeek Chat Completions API](https://api.deepseek.com/v1/chat/completions)
- [Qwen DashScope Compatible API](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)
- [Baidu ERNIE API](https://qianfan.baidubce.com/v3/chat/ernie-4.0-8k)
- [Google Gemini API](https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python objects and markdown guidance, including merged text plus per-model source results and timing metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. The included code currently simulates provider calls rather than performing real API routing.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata; artifact frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
