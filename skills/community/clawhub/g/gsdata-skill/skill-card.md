## Description:

Use GSData open platform via a local adapter script for account, content, ranking, public-sentiment, and NLP queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyuwen-bri](https://clawhub.ai/user/yangyuwen-bri)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to query GSData for public sentiment, hot events, platform rankings, account data, and social content from sources such as Xiaohongshu, Weibo, and Douyin. It helps agents discover endpoint capabilities, run bounded read-only searches, summarize results, and prepare explicitly approved write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GSData credentials may authorize access to account, content, ranking, public-sentiment, and NLP API data.

Mitigation: Use least-privileged GSData credentials, keep them in environment variables or a protected credentials file, and do not hardcode or share them.

Risk: Raw endpoint access and custom base URLs can broaden where signed requests are sent.

Mitigation: Disable or tightly restrict gsdata_raw, avoid custom base URLs, and require an HTTPS allowlisted GSData endpoint before installation.

Risk: Some operations can modify warning rules, ranking groups, accounts, or notification recipients.

Mitigation: Run dry-run checks first, require explicit user confirmation for write-like actions, and use --allow-write only for the confirmed operation.

Risk: Large query responses can expose more data than intended in chat contexts.

Mitigation: Use small size parameters for conversational responses, respect the API's 20-item page limit, and paginate deliberately after checking the result count.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyuwen-bri/skills/gsdata-skill)
- [GSData API gateway](http://databus.gsdata.cn:8888/api/service)
- [GSData tool mapping](artifact/gsdata_tool_mapping_v1.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GSDATA_APP_KEY and GSDATA_APP_SECRET credentials. Chat-facing queries should use small result sizes, and larger result sets require pagination.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
