## Description:

Collects public Douyin search results, creator posts, video comments, and real-time hotlist data as structured JSON for audience research, competitive analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, marketers, and analysts use this skill to query public Douyin content, inspect creator output, retrieve video comments, and check current hotlist topics for internal research and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous short-video research requests may invoke Douyin collection even when the user did not explicitly name Douyin.

Mitigation: Ask for explicit Douyin confirmation before running the skill when the target platform is unclear.

Risk: Douyin queries, target URLs, and authenticated requests are sent to www.guaikei.com.

Mitigation: Use the skill only for approved public-data research, avoid sensitive inputs, and ensure the GUAIKEI_API_TOKEN is authorized for the task.

Risk: The security review flagged credential and error-handling behavior as inconsistent with the skill's own safety claims.

Mitigation: Stop on token or authorization errors, review stderr before sharing outputs, and require publisher remediation for runtime contact or promotional messages.

Risk: Collected results and query targets can be written to local JSON logs.

Mitigation: Review local logs after use and retain or remove them according to the user's data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-audience-voice-reader)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Usage documentation](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration]

**Output Format:** [JSON on stdout with logs and status messages on stderr; task results may also be saved as local JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN environment variable; single requests can ask for up to 10000 items where supported.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
