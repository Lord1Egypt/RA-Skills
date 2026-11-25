## Description:

Lists recent articles from named WeChat Official Accounts, exports selected articles and available comments as Markdown, and summarizes them in a weekly report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users can monitor recent posts from WeChat Official Accounts they specify, review available read and like counts, export selected article text and comments as Markdown, and prepare a per-account weekly report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use of the HTTP method requires an okdata API key, and API calls may incur charges.

Mitigation: Keep the key in OKDATA_API_KEY or the client's configuration, and review the documented call plan and prices before paid calls.

## Reference(s):

- [okdata WeChat Articles guide](https://okdata.online/skills/wechat-articles/?src=skill-okdata-wechat-articles)
- [okdata WeChat Articles guide (Chinese)](https://okdata.online/zh/skills/wechat-articles/?src=skill-okdata-wechat-articles)
- [okdata agent setup instructions](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Analysis]

**Output Format:** [A table of article details, exported article Markdown files, and a per-account weekly summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read counts, likes, and comments are included when available from the platform; unavailable figures are left blank.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
