## Description:

Searches public Xiaohongshu notes by keyword or URL and retrieves note details, comments, creator post lists, and engagement data for content research and competitor monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, analysts, and operations teams use this skill to gather public Xiaohongshu search results, note details, comments, and creator activity for topic research, content planning, competitor monitoring, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note links, profile links, and the Guaikei API token to the third-party Guaikei service.

Mitigation: Install only when that data sharing is acceptable, confirm the API authorization scope, and avoid private or sensitive URLs.

Risk: Retrieved social-media data and links containing xsec_token values may be saved in generated logs.

Mitigation: Treat logs as sensitive research records, clean them up when no longer needed, and redact saved xsec_token links before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-track-creator-for-monitor)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; CLI commands return structured JSON and may write local log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer, GUAIKEI_API_TOKEN, and network access to the third-party Guaikei service.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
