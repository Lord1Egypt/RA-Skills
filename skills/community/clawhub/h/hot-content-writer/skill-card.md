## Description:

Generates AI-assisted social media copy from hot topics for Xiaohongshu, Douyin, WeChat public accounts, Weibo, and Zhihu, with local template fallback and optional DeepSeek-compatible API generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkt-agents](https://clawhub.ai/user/mkt-agents)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and marketing teams use this skill to turn topics or hot-list items into platform-specific drafts, titles, hashtags, and publishing tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send topics, audience notes, prompts, and API credentials to a configured LLM endpoint.

Mitigation: Use environment variables for API keys, avoid sensitive or regulated content, and only set a custom api_base when the endpoint is fully trusted.

Risk: Hot-list workflows execute neighboring skill scripts with weak scoping.

Mitigation: Review the installed hot-list skills before using --from-hot or daily_content.py, and run the workflow in a controlled workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mkt-agents/skills/hot-content-writer)
- [DeepSeek Platform](https://platform.deepseek.com)
- [Project Homepage](https://github.com/openclaw/hot-content-writer)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [JSON to stdout or file containing generated titles, copy, hashtags, and publishing tips; optional plain-text WeChat summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured OpenAI-compatible LLM endpoint and can fall back to local templates when no API key is configured.]

## Skill Version(s):

1.2.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
