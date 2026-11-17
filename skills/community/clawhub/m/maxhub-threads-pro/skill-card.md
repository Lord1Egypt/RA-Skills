## Description:

Queries Threads posts, comments, profiles, timelines, and search results to support social content research and interaction analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, researchers, and content teams use the skill to look up Threads content and summarize public discussions, account activity, and topic trends through MaxHub. Use it for authorized, narrowly scoped data research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the API key and user-supplied identifiers, keywords, and URLs to MaxHub, a third-party service; the security assessment also flags URL sharing.

Mitigation: Use authorized data, submit only what the query needs, and keep MAXHUB_API_KEY out of prompts and logs.

Risk: The documented workflow writes compliance confirmations and API-call audit records to local files.

Mitigation: Review the local record location and retention policy, and limit access to those files.

Risk: Security guidance notes an unpinned installer, error-triggered upgrade advice, and partial scanner coverage.

Mitigation: Review the package source and version before installing or upgrading, and inspect the skill’s permissions and data handling.

## Reference(s):

- [Server-resolved GitHub source (commit 79447332cd95579372dc0a95487577cc9fb38f6c)](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-threads)
- [MaxHub API](https://www.aconfig.cn)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-threads-pro)
- [Threads platform documentation](https://developers.facebook.com/docs/threads)
- [Endpoint whitelist](artifact/references/endpoints_whitelist.yaml)
- [Field mappings](artifact/references/param-mappings.md)
- [Recipe index](artifact/references/recipes/_index.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Analysis]

**Output Format:** [JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups; paginated results may be summarized for the requested scope.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
