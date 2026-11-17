## Description:

Retrieves public Xiaohongshu data for note search, note details, comment retrieval, and creator post listings when a user needs Xiaohongshu-specific research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, brand marketers, market analysts, and agents use this skill to retrieve structured public Xiaohongshu data for topic research, competitor monitoring, KOL screening, trend tracking, and comment sentiment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu links, keywords, and the Guaikei API token to www.guaikei.com.

Mitigation: Install and run it only when that third-party data flow is acceptable, and rotate the API token if exposure is suspected.

Risk: Generated logs may contain research targets, returned content, and xsec_token-bearing URLs.

Mitigation: Treat the logs directory as sensitive; restrict access, delete logs when no longer needed, and avoid sharing raw log files.

Risk: The skill is scoped to public Xiaohongshu data and does not support private, hidden, login-state, or cross-platform content.

Mitigation: Confirm the user request is for public Xiaohongshu data and ask for clearer input when the platform, keyword, or URL type is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comments-for-sentiment)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Structured JSON from Node.js CLI commands with human-facing guidance for parameter selection and error handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save returned data and execution logs under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
