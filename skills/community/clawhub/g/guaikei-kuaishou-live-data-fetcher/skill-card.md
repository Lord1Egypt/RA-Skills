## Description:

Fetches public Kuaishou/Kwai videos, creator posts, and video comments through the Guaikei API for content research, competitive analysis, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, analysts, and agent operators use this skill to collect public Kuaishou/Kwai search results, creator work lists, and video comments as structured JSON for research, monitoring, comparison, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, URLs, and the API token are sent to guaikei.com.

Mitigation: Use the skill only in approved environments, confirm data-sharing authorization, and avoid submitting sensitive or non-public targets.

Risk: Successful results are saved locally under logs and may include comments or metadata.

Mitigation: Review local retention needs and delete saved result files that should not be retained or shared.

Risk: The skill is intended for public Kuaishou data and does not support private, hidden, or login-only data.

Mitigation: Run it only against public Kuaishou keywords, creator pages, or video links, and decline requests for non-public data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-live-data-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [JSON status objects with request metadata and result arrays, plus concise text guidance and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful command results are also saved locally under logs; execution requires GUAIKEI_API_TOKEN and network access to guaikei.com.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
