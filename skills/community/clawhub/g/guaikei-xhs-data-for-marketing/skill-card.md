## Description:

Retrieves public Xiaohongshu data for keyword search, note detail, comment extraction, and creator-post monitoring to support marketing research and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, creators, analysts, and operations teams use this skill to gather public Xiaohongshu posts, creator activity, note details, and comments for content planning, competitor monitoring, KOL screening, trend research, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu research inputs and the GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Install and use only when that data sharing is acceptable; treat the token as sensitive and monitor or rotate it after use.

Risk: Local logs may retain research targets, result data, or token-bearing Xiaohongshu URLs.

Mitigation: Review, protect, or delete the logs/ directory before sharing the workspace or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-data-for-marketing)
- [Guaikei service website](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Skill changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Files]

**Output Format:** [JSON command output with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful and failed command results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata, package.json, and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
