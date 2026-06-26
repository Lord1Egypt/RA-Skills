## Description: <br>
Analyzes crypto news and social media sentiment to produce bullish, bearish, or neutral scores and trading-signal guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbrc20](https://clawhub.ai/user/alexbrc20) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to summarize cryptocurrency market sentiment from social/news inputs, monitor coins, and generate informational trading-signal guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends crypto search terms and retrieved social/news content to external services including 6551.io and DashScope. <br>
Mitigation: Use scoped API tokens, avoid private or regulated content, and install only when those external data flows are acceptable. <br>
Risk: Generated buy, sell, or hold signals may be misleading if treated as financial advice. <br>
Mitigation: Treat outputs as informational sentiment summaries and review them alongside independent market research and risk controls. <br>
Risk: LLM or keyword-based sentiment classification can be stale, incomplete, or inaccurate. <br>
Mitigation: Review source posts and news items before acting on sentiment scores, especially for volatile assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbrc20/news-sentiment) <br>
- [6551.io Twitter search API endpoint](https://ai.6551.io/open/twitter_search) <br>
- [DashScope text generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style text with sentiment scores, labels, and suggested actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, curl, DASHSCOPE_API_KEY, and a Twitter token for external API-backed analysis; falls back to keyword sentiment when DashScope is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and README list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
