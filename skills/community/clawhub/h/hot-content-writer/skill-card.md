## Description: <br>
Hot Content Writer generates platform-specific Chinese social-media copy from a topic, with optional DeepSeek/OpenAI-compatible API mode and hot-list driven daily content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq853632587](https://clawhub.ai/user/qq853632587) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, social media operators, and marketing teams use this skill to draft topic-driven posts, scripts, titles, hashtags, and daily hot-topic content for Xiaohongshu, Douyin, WeChat public accounts, Weibo, and Zhihu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode may reuse an existing OPENAI_API_KEY and send requests to the configured DeepSeek/OpenAI-compatible endpoint. <br>
Mitigation: Use a dedicated low-privilege DeepSeek key, verify OPENAI_API_BASE before API runs, and unset unrelated OPENAI_API_KEY values when they should not be used. <br>
Risk: A local config.json can store an API key for this skill. <br>
Mitigation: Keep config.json local-only, avoid committing secrets, and prefer environment variables or a secret manager when available. <br>
Risk: Hot-topic modes execute companion hot-list skill scripts and consume their results. <br>
Mitigation: Use hot-list integrations only with companion skills that have been reviewed and trusted in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qq853632587/hot-content-writer) <br>
- [DeepSeek Platform](https://platform.deepseek.com) <br>
- [DeepSeek API Endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Generated social-media copy and titles as JSON or plain text, plus command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated content to a user-specified output file; API mode sends prompts to the configured OpenAI-compatible endpoint.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
