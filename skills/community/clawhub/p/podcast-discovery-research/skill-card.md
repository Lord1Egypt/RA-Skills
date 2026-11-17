## Description:

Discovers and compares public podcast shows, episodes, charts, rankings, and related programs using Apple Podcasts and Spotify Podcasts through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast researchers and other users discover shows and episodes, compare platform-specific charts, and assemble guest or partnership shortlists from public metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API requires a credential that could be exposed if shared or logged.

Mitigation: Keep CRAWLORA_API_KEY private and provide it only in authorized environments.

Risk: Podcast search queries are sent to a third-party API.

Mitigation: Avoid confidential names, internal project terms, and sensitive investigation targets in queries.

## Reference(s):

- [Podcast endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/podcast-discovery-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with platform-specific metadata and source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart comparisons should retain platform, market, category, date, and retrieval time.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
