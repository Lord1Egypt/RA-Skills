## Description:

Searches public Kuaishou videos by keyword and retrieves creator posts and video comments for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use the skill to find popular Kuaishou videos, review public creator posts, and examine video comments for research and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, profile or video URLs, and the API token are sent to guaikei.com.

Mitigation: Use only when the requested data and token may be shared with this third-party service.

Risk: Saved results in logs/ may contain sensitive queried targets or returned comments.

Mitigation: Review and remove local logs when the queried targets or comments are sensitive.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/kuaishou-videos-search)
- [Guaikei API and token information](https://www.guaikei.com)
- [Skill options](artifact/references/options.md)

## Skill Output:

**Output Type(s):** [Structured data, Text]

**Output Format:** [JSON results with status and optional text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are also saved locally in logs/.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
