## Description:

Collects public Xiaohongshu content, note details, creator posts, and comments through Guaikei-backed command-line workflows for trend monitoring and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, brand marketers, market researchers, and analysts use this skill to retrieve public Xiaohongshu search results, note details, creator posts, and comments for topic research, competitor monitoring, KOL screening, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and the Guaikei API token to the Guaikei service.

Mitigation: Install and run it only where that data transfer is approved, and avoid submitting URLs that contain reusable tokens unless necessary.

Risk: Generated logs can contain retrieved content, request details, keywords, or URLs.

Mitigation: Treat the logs/ directory as sensitive output: review, protect, or delete it after use, and avoid committing generated logs.

Risk: The server security verdict is suspicious because token handling and saved results should be reviewed before installation.

Mitigation: Review the skill and scan results before deployment, limit use to public Xiaohongshu data, and keep usage within approved internal or commercial workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-blogger-list)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with status, request, skill metadata, and results; successful runs also save JSON files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands query public Xiaohongshu data through Guaikei and return success, empty, or error status objects.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
