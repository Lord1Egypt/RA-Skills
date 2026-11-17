## Description:

Collects public Xiaohongshu note, author, interaction, and comment data through Guaikei API-backed command-line workflows for content research, KOL screening, competitor monitoring, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, and data analysts use this skill to search public Xiaohongshu notes, inspect note details and comments, and monitor public creator posts for market research and campaign decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Guaikei API token and request parameters are sent to the Guaikei service, and the security summary notes credentials are sent in URL query strings.

Mitigation: Install only when this data flow is acceptable, avoid exposing command output or logs, and rotate GUAIKEI_API_TOKEN if it may have been disclosed.

Risk: Collected Xiaohongshu URLs, search terms, returned data, and comments can be saved locally in generated logs.

Mitigation: Treat generated logs as sensitive, delete them when no longer needed, and avoid committing or sharing the package directory after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-data)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with status, request metadata, execution metadata, and results; guidance may include concise Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands may save returned results under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
