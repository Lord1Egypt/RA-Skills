## Description:

Collects public Douyin data through CLI commands for keyword search, creator post lists, video comments, and real-time hot rankings, returning structured JSON for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and content teams use this skill to gather public Douyin keyword results, creator posts, comments, and hot-ranking data for content research, competitor analysis, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, target URLs, and the GUAIKEI service token to www.guaikei.com; security evidence also notes the token is sent in URL query strings.

Mitigation: Install only when that data sharing is acceptable, treat GUAIKEI_API_TOKEN as sensitive, restrict access to environments that contain it, and rotate the token if it may have been exposed.

Risk: Collected results are saved locally by default and may include creator, commenter, and media URL data.

Mitigation: Review stored log files before sharing, redact or delete sensitive outputs when no longer needed, and restrict workspace access for users who do not need the collected data.

Risk: Security evidence marks the release suspicious because it contradicts its auth-error safety promise and broad inferred requests may collect more data than intended.

Mitigation: Review the skill before execution, avoid broad inferred requests, stop on authentication errors, and ask users to confirm narrowed parameters for large or ambiguous data-collection tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-bulk-videos-fetch)
- [GUAIKEI token and help page](https://www.guaikei.com)
- [Usage guide](artifact/readme.md)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [CLI JSON schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON results on stdout, diagnostic logs on stderr, and JSON log files under the skill logs directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; commands support keyword, URL, sorting, time, duration, content-type, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
