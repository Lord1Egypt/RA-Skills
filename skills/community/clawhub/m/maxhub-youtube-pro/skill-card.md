## Description:

Query public YouTube video and channel data through the MaxHub API, including captions, comments, streams, search, trends, and related videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and analysts use the skill to research public YouTube videos and channels, review captions, comments, and trends, and prepare content or competitor reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API key and user-supplied identifiers, keywords, and URLs to the third-party MaxHub service; optional cookies or tokens may also be transmitted.

Mitigation: Review the service's privacy terms, use only authorized and necessary inputs, and keep credentials out of prompts and logs.

Risk: The skill instructions create persistent local compliance and audit records.

Mitigation: Restrict access to those records and apply a retention period appropriate to the data they contain.

Risk: The security review notes that consent wording is Chinese-only, which may leave some users unable to understand the disclosure.

Mitigation: Ensure users understand the consent and data-use disclosure in a language they can read before API use.

Risk: The documented installer command does not pin a release, and the security review flags this as an unpinned installer.

Mitigation: Verify the publisher and reviewed release, then pin the intended version when installing.

Risk: The security review reports partial scanner coverage because some references could not be resolved.

Mitigation: Review unresolved references and rerun security checks with complete inputs before deployment.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-youtube)
- [ClawHub skill release](https://clawhub.ai/xiewxx/skills/maxhub-youtube-pro)
- [Publisher profile](https://clawhub.ai/user/xiewxx)
- [MaxHub API service](https://www.aconfig.cn)
- [Recipe index](references/recipes/_index.md)
- [Endpoint allowlist](references/endpoints_whitelist.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Text or Markdown summaries and structured API results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on data available from YouTube and the MaxHub API; unavailable fields may be omitted.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
