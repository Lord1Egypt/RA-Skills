## Description:

A Node.js command skill that retrieves public Xiaohongshu keyword results, note details, comments, and creator posts through the Guaikei API for structured content, competitor, KOL, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketing teams, and analysts use this skill to retrieve public Xiaohongshu keyword, note, comment, and creator-post data for topic research, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu links, search keywords, and API-token-authenticated requests to guaikei.com.

Mitigation: Install only if this data sharing is acceptable, keep the GUAIKEI_API_TOKEN value out of terminals and logs, and avoid shared or CI workspaces.

Risk: Command outputs are saved under logs/ and may contain Xiaohongshu links, keywords, comments, and other collected public data.

Mitigation: Treat generated logs as sensitive and delete them when no longer needed.

## Reference(s):

- [Guaikei API site](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-insight)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON with status, error_code, message, request, skill_metadata, and results fields; successful task results are also saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package/frontmatter report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
