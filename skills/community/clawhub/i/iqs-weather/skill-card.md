## Description:

Queries 7-day weather forecasts for cities using Alibaba Cloud IQS web search and page reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijian-github-20190615](https://clawhub.ai/user/lijian-github-20190615)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve city-level 7-day weather forecasts through Alibaba Cloud IQS, returning structured forecast data when known weather sites can be parsed and raw page text for agent interpretation otherwise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud processes the city query and fetched weather page URL.

Mitigation: Use the skill only when this data sharing is acceptable for the user and deployment context.

Risk: The skill describes modifying executable parser code after reading untrusted web page content.

Mitigation: Do not allow automatic edits to scripts/weather.mjs from raw page content; require human review and scanning before parser changes are used.

Risk: The API key may be stored in shell configuration or a local dotfile.

Mitigation: Store the key with restrictive permissions or a secret manager rather than shared dotfiles.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lijian-github-20190615/skills/iqs-weather)
- [Alibaba Cloud IQS Search Skill](https://skills.aliyun.com/skills/alibabacloud-iqs-search)
- [Aliyun IQS API Key Documentation](https://help.aliyun.com/zh/document_detail/3025781.html)
- [Aliyun UnifiedSearch Documentation](https://help.aliyun.com/zh/document_detail/2883041.html)
- [Aliyun ReadPageScrape Documentation](https://help.aliyun.com/zh/document_detail/2983380.html)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON weather results with optional raw text and guidance; Markdown instructions with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY and Node.js 18 or newer.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
