## Description:

Kuai Shou Ai Feed helps agents search public Kuaishou videos by keyword, fetch creator public posts, and retrieve video comments as structured JSON for content research and competitor monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, MCN teams, and analysts use this skill to collect public Kuaishou data for topic discovery, competitor monitoring, KOL screening, trend analysis, and comment insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, request parameters, and GUAIKEI_API_TOKEN are sent to a third-party API provider.

Mitigation: Confirm approval for the third-party API provider before installation and avoid submitting sensitive targets or unauthorized data.

Risk: Generated logs can contain sensitive research targets, request parameters, and analysis outputs.

Mitigation: Protect the logs directory with appropriate access controls and delete exported results when they are no longer needed.

Risk: The skill is limited to public Kuaishou data and can fail on private, hidden, deleted, or login-required content.

Mitigation: Use only public Kuaishou keywords, creator profiles, and video links; treat empty or error JSON statuses as non-results rather than evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/kuai-shou-ai-feed)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON status objects with request metadata and results, plus local JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports keyword search, creator posts, and video comments with limits up to 10000 records where supported.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
