## Description:

Fetches public Kuaishou/Kwai video search results, creator works, and video comments through the Guaikei API for short-video research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, analysts, and agents use this skill to collect public Kuaishou/Kwai search, creator-work, and comment data for trend research, competitor monitoring, topic discovery, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, profile/video URLs, request parameters, and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only where this third-party data sharing is approved, and manage the token according to your team's credential handling policy.

Risk: Fetched comments and creator/video results may be saved locally in logs/.

Mitigation: Review generated logs and delete them when they are no longer needed, especially when the fetched data should not remain on the machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-creator-work-fetcher)
- [Guaikei API token portal](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [Structured JSON result envelopes with status, error_code, request metadata, skill metadata, and results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14+ and GUAIKEI_API_TOKEN; successful runs may save JSON logs locally under logs/.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, frontmatter, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
