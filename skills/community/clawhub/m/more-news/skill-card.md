## Description:

Aggregates and ranks AI and tech news from configured sources, filtering for recent articles and returning summaries with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compile a ranked AI and technology news digest from a maintained source list when they need recent headlines, short summaries, source links, and skipped-source notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts multiple public news websites when generating a digest.

Mitigation: Review or edit the source list before use to limit which sites the agent may fetch.

Risk: Some sources may be blocked, stale, or lack recent article metadata.

Mitigation: The skill reports skipped sources and should omit entries without enough article details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/more-news)
- [Publisher profile](https://clawhub.ai/user/goog)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown news digest with ranked entries, summaries, links, counts, and skipped-source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public news websites from the configured source list and may skip blocked, stale, or article-free sources.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
