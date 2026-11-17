## Description:

Queries WeChat Channels and Official Account data through MaxHub, including search, video details, comments, articles, and user information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to query and analyze WeChat Channels videos and Official Account articles, comments, and user data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, including broad or ambiguous requests, are sent to MaxHub; the security analysis was partial and does not establish that the skill is safe.

Mitigation: Review each query before execution, especially requests involving sensitive information, and use a reviewed, fixed version of the installer and skill.

Risk: The skill sends its configured MAXHUB_API_KEY to the MaxHub API.

Mitigation: Use the key only with the documented MaxHub service and keep its value out of prompts and responses.

## Reference(s):

- [Publisher source repository](https://github.com/XieWxx/maxhub-wechat)
- [MaxHub API service and API key setup](https://www.aconfig.cn)
- [Channels API reference](references/api-channels.md)
- [Official Account API reference](references/api-mp.md)
- [API parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Markdown, Guidance]

**Output Format:** [Markdown responses with concise summaries, tables, and key data fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language; third-party API data is for reference only.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
