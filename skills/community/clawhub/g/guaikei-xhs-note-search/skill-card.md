## Description:

A command skill for searching public Xiaohongshu notes, retrieving note details and comments, and collecting public creator posts for content research, competitor analysis, KOL screening, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, marketers, content creators, and analysts use this skill to query public Xiaohongshu content by keyword, note URL, or creator profile URL and receive structured results for follow-on analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the GUAIKEI_API_TOKEN, search terms, and Xiaohongshu URLs to the Guaikei service.

Mitigation: Use a limited and rotatable token, confirm authorization for submitted queries and links, and avoid sensitive business research when third-party transmission is not acceptable.

Risk: Successful runs may save public-content results and request parameters as local JSON logs.

Mitigation: Protect the logs/ directory, delete generated logs when no longer needed, and avoid sharing logs that contain sensitive research targets or retrieved content.

Risk: Security evidence marks the release suspicious because users should review credential handling and saved results before installation.

Mitigation: Review the skill and scan findings before deployment, configure the token through the environment, and run only with intended public Xiaohongshu inputs.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-search)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON responses with concise Markdown guidance and saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs may save request parameters and results under logs/.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
