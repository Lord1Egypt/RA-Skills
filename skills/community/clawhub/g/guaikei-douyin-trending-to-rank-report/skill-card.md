## Description:

This skill helps agents collect public Douyin data for keyword search, creator post lists, video comments, and real-time trending topics for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather structured public Douyin data for short-video topic research, competitor account analysis, comment review, and trend monitoring. It is not intended for publishing videos, editing content, downloading watermarked media, private data access, or non-Douyin collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires GUAIKEI_API_TOKEN and can create retained research logs.

Mitigation: Use a low-privilege, rotatable token and handle generated logs as retained research data that may need review before sharing or deletion.

Risk: Broad trigger rules can cause Douyin collection during generic content research when the platform is not explicit.

Mitigation: Invoke the skill only after confirming that Douyin public-data collection is intentionally in scope.

Risk: Authentication failures may display promotional contact information despite documentation saying runtime errors are neutral.

Mitigation: Review runtime stderr before exposing logs to users, and treat authentication failures as a stop condition requiring token configuration review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trending-to-rank-report)
- [README](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei token and usage site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [JSON on stdout with stderr status messages and optional timestamped JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or later and GUAIKEI_API_TOKEN; command outputs follow the JSON schemas bundled under assets/.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md, and src/config/constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
