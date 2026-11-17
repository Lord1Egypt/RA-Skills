## Description:

Collects public Kuaishou video, creator post, and comment data as structured JSON for competitor research, trend monitoring, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, marketers, MCN operators, and analysts use this skill to search Kuaishou public videos, inspect creator posts, fetch video comments, and turn the resulting JSON into competitor, trend, KOL, and audience-insight reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, URLs or IDs, selected options, and GUAIKEI_API_TOKEN are shared with the GuaiKei API service.

Mitigation: Use the skill only when that data sharing is acceptable for the task, account, and organization.

Risk: Fetched research data may be retained locally under logs.

Mitigation: Delete local logs when the collected Kuaishou research data should not be retained.

Risk: The skill is limited to public Kuaishou data and may return empty or error JSON for unavailable, private, deleted, rate-limited, or unsupported requests.

Mitigation: Check the returned status and error code before drawing conclusions or generating reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-competitor-research)
- [Guaikei Website](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Structured JSON with optional Markdown summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; fetched results may be saved locally under logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
