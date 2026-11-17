## Description:

Analyze crypto news and social media sentiment for bullish, bearish, or neutral market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbrc20](https://clawhub.ai/user/alexbrc20)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to summarize cryptocurrency market sentiment for specific coins and to inform, but not replace, their own trading research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coin symbols and retrieved social/news text may be processed by Twitter/6551 and Dashscope services when credentials are configured.

Mitigation: Configure credentials only in approved environments and avoid submitting confidential information as query terms or source text.

Risk: Public posts can manipulate or distort sentiment analysis, and the skill may produce buy/sell-style signals.

Mitigation: Treat generated signals as informational only and require independent review before making financial decisions.

Risk: Some advertised features, including alerts, Reddit/news breadth, and pro functionality, were not implemented in the inspected code.

Mitigation: Validate needed workflows in the installed artifact before relying on them in production or customer-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbrc20/skills/news-sentiment)
- [Publisher profile](https://clawhub.ai/user/alexbrc20)
- [Twitter search API endpoint](https://ai.6551.io/open/twitter_search)
- [Dashscope text generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text sentiment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured third-party API credentials for full API-backed analysis; otherwise the artifact includes a keyword-based fallback.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and README state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
