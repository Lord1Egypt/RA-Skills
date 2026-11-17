## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, monitors public creator posts, and returns structured data for trend discovery, competitor analysis, KOL screening, and comment insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market researchers, data analysts, and operations teams use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for content planning and social media analysis. It is not intended for login-gated data, publishing, liking, following, or other account interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, Xiaohongshu links, retrieved public content, and GUAIKEI_API_TOKEN are sent to Guaikei's API.

Mitigation: Use the skill only when that data sharing is acceptable, keep GUAIKEI_API_TOKEN secret, and avoid submitting tokenized Xiaohongshu URLs unless they are necessary for the task.

Risk: The generated logs directory can contain research history and full collected datasets.

Mitigation: Protect access to the logs directory, exclude it from unintended sharing, and delete stored results when they are no longer needed.

Risk: The authoritative security verdict is suspicious because the skill depends on a third-party data service.

Mitigation: Review the skill and service requirements before deployment, and limit use to approved public-data collection workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-trend-sheet)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; command stdout is structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes full task results to the local logs directory by default.]

## Skill Version(s):

1.0.0 (source: ClawHub server release metadata; artifact metadata and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
