## Description:

Searches Kuaishou public data by keyword, creator profile, or video URL to collect structured video, creator-post, and comment data for content research, competitor monitoring, KOL discovery, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, MCN operators, and analysts use this skill to collect public Kuaishou search results, creator post lists, and video comments for research workflows. It is suited to public-data trend research, competitor monitoring, KOL screening, and comment insight generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends Kuaishou keywords, profile URLs, video URLs, request parameters, and a third-party Guaikei API token to www.guaikei.com.

Mitigation: Use only approved public-data research inputs, confirm the Guaikei token is authorized for the workflow, and avoid submitting confidential campaign or customer information.

Risk: Generated result logs can retain collected Kuaishou data on the local machine.

Mitigation: Run the skill on trusted systems, protect or delete logs after use, and avoid collecting large comment sets on shared machines unless local retention is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/kuaishou-guaikei-content-research)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with runnable Node.js commands and structured JSON result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN. Successful runs emit JSON with status, request metadata, skill metadata, and results; runs may also persist local JSON logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
