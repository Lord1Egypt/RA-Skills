## Description:

Use when a user wants an AI agent to call Heyi's Xiaohongshu, Douyin, Kuaishou, or Bilibili HTTP APIs with a Bearer API Key, including endpoint discovery, point billing, balance checks, pagination, batching, error handling, retries, or usage reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyi-byte](https://clawhub.ai/user/heyi-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and external API users use this skill to have an agent discover and call Heyi's paid social-media data APIs, estimate point costs, handle pagination and retries, and reconcile usage against server point records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to a configurable API host if HEYI_API_BASE_URL is changed from the default.

Mitigation: Keep HEYI_API_BASE_URL at the default production host unless the alternate endpoint is fully trusted, and store HEYI_API_KEY only in a secret store or environment variable.

Risk: Paid or batch API calls can consume account points.

Mitigation: Require user confirmation before billable calls, check balance before batches, estimate maximum point use, and reconcile final charges with server point records.

Risk: The artifact includes maintainer publishing tooling that security evidence flags as risky for real tokens.

Mitigation: Publishers should pin the ClawHub CLI and fix temporary-file handling before using the release script with production tokens.

## Reference(s):

- [Heyi API homepage](https://api.01011.top)
- [Heyi API console and base URL](https://bot.01011.top)
- [API key setup guide](https://my.feishu.cn/wiki/SzpMwQQ1Piw3rck0NAPc7la1npe)
- [ClawHub skill listing](https://clawhub.ai/heyi-byte/skills/heyi-paid-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell or code snippets and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint choices, request parameters, billing estimates, and call-record references; secrets should not be included in outputs.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
