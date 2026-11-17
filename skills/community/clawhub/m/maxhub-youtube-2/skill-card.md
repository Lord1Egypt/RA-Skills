## Description:

Queries YouTube video, channel, search, comment, subtitle, and Shorts data through MaxHub's Web and V2 APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and analysts can use the skill to look up YouTube videos and channels, search content, and review comments, captions, and Shorts through MaxHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer command does not pin a release version.

Mitigation: Check the package source and release before installing, and use a reviewed version when available.

Risk: Query terms and target identifiers may be sent to MaxHub when making API requests.

Mitigation: Avoid sending sensitive terms or identifiers, and review the service's privacy terms before use.

Risk: The security scan had partial coverage because some referenced local paths could not be resolved.

Mitigation: Review the supplied skill and reference files before enabling API access.

## Reference(s):

- [MaxHub API service](https://www.aconfig.cn)
- [Server-resolved source repository](https://github.com/XieWxx/maxhub-youtube)
- [Server-resolved source commit](https://github.com/XieWxx/maxhub-youtube/commit/2d3536f835c2d2fb6b84bbe284e45a1081b4cb41)
- [Video API reference](artifact/references/api-video.md)
- [Channel API reference](artifact/references/api-channel.md)
- [Search API reference](artifact/references/api-search.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise text with Markdown tables and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in Chinese or English and formats large numbers for readability.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
