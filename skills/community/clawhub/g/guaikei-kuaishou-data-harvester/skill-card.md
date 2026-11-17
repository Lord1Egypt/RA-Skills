## Description:

Collects public Kuaishou data through Guaikei API-backed commands for keyword video search, creator post retrieval, and video comment extraction, returning structured JSON for content research, competitor monitoring, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and analysts use this skill to collect public Kuaishou videos, creator posts, and comments for topic research, competitor monitoring, KOL review, and marketing analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, URLs, request parameters, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only when that third-party data flow is acceptable, and avoid sharing tokens outside the intended runtime environment.

Risk: Collected comments and creator data are public but still privacy-relevant.

Mitigation: Use collected data only for permitted analysis, follow applicable platform and legal rules, and avoid redistributing datasets without authorization.

Risk: Run results may be saved locally under logs/.

Mitigation: Periodically clear local logs when retained Kuaishou datasets are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-data-harvester)
- [Guaikei API access and support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON responses with status, request metadata, and result arrays; successful runs may also save JSON files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, URL or user_id inputs with optional sort, time, duration, and limit filters.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
