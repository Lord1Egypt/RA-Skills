## Description:

Queries public Xigua video data through MaxHub for video details, playback links, comments, search, creator profiles, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External content researchers and creators can use the skill to review public Xigua videos, comments, search results, and creator profiles for topic research and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because scanners report update behavior and local compliance records beyond the stated read-only query purpose; some references could not be resolved.

Mitigation: Review the update and local-record workflows and resolve the missing references before use; limit filesystem and credential access to what is needed.

Risk: The security guidance reports incomplete notices about information sent to aconfig.cn; requests may include credentials, IDs, keywords, URLs, or optional cookies and tokens.

Mitigation: Confirm what data each request sends, use only authorized inputs, minimize personal data, and keep API keys and session credentials out of logs and prompts.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-xigua)
- [MaxHub API service](https://www.aconfig.cn)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-xigua-pro)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown, Guidance]

**Output Format:** [Structured API data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields depend on the selected video, comment, search, or creator endpoint.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
