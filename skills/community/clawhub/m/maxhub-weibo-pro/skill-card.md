## Description:

This read-only skill helps agents search and analyze public Weibo posts, comments, profiles, trends, and video feeds through MaxHub, a third-party data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and content teams use it to monitor public discussion, follow trending topics, assess content reach, and summarize Weibo activity. Use it only for data processing you are authorized to perform under applicable law and platform terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and credentials are sent to MaxHub, a third-party data service, and returned content may include personal information or user-generated content.

Mitigation: Use only authorized, minimum-necessary data; never use another person's cookies or tokens; keep API keys and personal data out of logs, prompts, and public outputs.

Risk: The skill documentation says the data service is not Weibo's official API and is not officially authorized by Weibo, which creates platform-terms and legal risk.

Mitigation: Check applicable law and Weibo's terms, prefer the official Weibo Open Platform where suitable, and avoid prohibited collection, storage, or reuse.

Risk: The security review notes an unpinned installer, local compliance records, and partial analysis coverage due to missing or ambiguous references.

Mitigation: Inspect the installer and source before use, confirm what consent state and audit data are written and where, and complete review with the referenced materials available.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-weibo)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-weibo-pro)
- [Endpoint allowlist](references/endpoints_whitelist.yaml)
- [Parameter mappings](references/param-mappings.md)
- [Recipe index](references/recipes/_index.md)
- [Weibo Open Platform](https://open.weibo.com)
- [MaxHub service](https://www.aconfig.cn)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Concise text or Markdown summaries with query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query and analysis; results can contain user-generated content and personal information.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
