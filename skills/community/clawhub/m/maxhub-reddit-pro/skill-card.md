## Description:

Helps agents query and summarize public Reddit community, post, comment, user, feed, and search data through the MaxHub API in read-only workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to query and summarize public Reddit discussions for community research, topic monitoring, competitor feedback, and content insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API credentials and query inputs to a third-party service, and Reddit posts or comments may contain personal or sensitive information.

Mitigation: Use only authorized, necessary data; protect credentials and avoid sending optional cookies or tokens; minimize and safeguard returned user-generated content.

Risk: The security review notes an unpinned installer, local compliance or account-preference lookups, broad recipe triggers, and incomplete scan coverage because some references could not be resolved.

Mitigation: Verify the installer source and version, review local file access and trigger behavior, and inspect unresolved references before use.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-reddit)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-reddit-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Reddit API documentation](https://www.reddit.com/dev/api)
- [Recipe index](references/recipes/_index.md)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results may contain user-generated content or personal details; missing fields should be reported explicitly.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
