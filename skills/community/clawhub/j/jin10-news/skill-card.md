## Description:

提供金十金融快讯及详情，支持本地缓存浏览和对港股、恒生科技及相关个股的影响分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[akinding](https://clawhub.ai/user/akinding)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting financial-news workflows use this skill to retrieve recent Jin10 updates, inspect item details, and generate impact analysis for Hong Kong equities and selected stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes unbundled absolute-path scripts whose actual behavior is not present in the reviewed artifact.

Mitigation: Install only after reviewing the scripts under /root/.openclaw/workspace/scripts and confirming they match the intended Jin10 fetch, cache, detail, and analysis behavior.

Risk: The documented background fetcher may make periodic network requests and write cache files under /tmp.

Mitigation: Run it only in an environment where those network requests and cache writes are expected, monitored, and allowed by local policy.

Risk: The artifact references a Jin10 access token but does not show how the token is stored or transmitted.

Mitigation: Verify token handling before use, keep credentials out of prompts and logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akinding/skills/jin10-news)
- [Publisher profile](https://clawhub.ai/user/akinding)
- [Jin10](https://jin10.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text financial-news summaries with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads recent news from local cache when available; detail and deep-analysis commands operate on selected news items.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
