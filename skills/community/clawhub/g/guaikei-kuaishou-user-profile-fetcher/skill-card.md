## Description:

Retrieves public Kuaishou/Kwai data for keyword video search, creator post monitoring, and video comment analysis through the GuaiKei data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, market researchers, data analysts, and agents use this skill to collect public Kuaishou search results, creator posts, and video comments for trend research, competitor monitoring, KOL screening, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou keywords, video or profile URLs, request parameters, and GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use the skill only when the user is comfortable sharing those inputs with the GuaiKei service, and avoid submitting confidential research targets or sensitive identifiers.

Risk: Returned public comments, creator data, and business research results are saved to a local logs directory.

Mitigation: Review and delete local logs after use when outputs contain sensitive business research, personal data from public comments, or data that should not be retained.

Risk: The skill is limited to public Kuaishou data and does not support private, hidden, login-gated, or non-Kuaishou content.

Mitigation: Confirm that the user request involves public Kuaishou keywords, video links, profile links, or user IDs before running commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-user-profile-fetcher)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei API Service](https://www.guaikei.com)
- [Complete Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json, guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and structured JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful, empty, and error responses include status, error_code, request metadata, skill metadata, and results; command results are also written to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
