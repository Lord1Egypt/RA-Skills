## Description:

Maps podcast topics across sampled public Apple Podcasts and Spotify shows and episodes using Crawlora, while preserving source identity, sampling limits, and the distinction between descriptions and verified content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast editors and researchers use this skill to compare topic coverage across selected shows, assemble a source-linked episode evidence ledger, and create a listening shortlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and podcast identifiers are sent to Crawlora's external API.

Mitigation: Avoid confidential topics and share only the queries and identifiers needed for the task.

Risk: API credentials and unbounded requests can expose a key or incur unnecessary usage.

Mitigation: Keep CRAWLORA_API_KEY private and set explicit call, page, and credit limits.

Risk: Discovery samples and episode descriptions can be mistaken for exhaustive coverage or verified spoken content.

Mitigation: Report sampling limits and coding sources; verify claims against episode content before presenting them as spoken facts.

## Reference(s):

- [Podcast topic landscape endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/podcast-topic-landscape)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown show-by-topic matrix, episode evidence ledger, and listening shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links, episode dates, coding basis, sample denominators, and uncertainty notes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
