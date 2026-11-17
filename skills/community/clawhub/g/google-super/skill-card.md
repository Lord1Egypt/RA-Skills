## Description:

Unified Google services API integration with managed OAuth for Gmail, Calendar, Drive, Docs, Sheets, Slides, Meet, Tasks, Photos, Maps, Google Analytics, and Google Ads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect one Google account through ClawLink and operate across Google services from chat, including email, calendar, file, document, spreadsheet, meeting, task, photo, maps, analytics, and ads workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects broad Google access across sensitive services through a single OAuth flow.

Mitigation: Use a dedicated or low-risk Google account where possible, avoid connecting production email, Drive, Ads, or Analytics accounts unless the full bundle is required, and revoke the ClawLink Google OAuth grant when finished.

Risk: The install flow asks users to install and allowlist an unpinned third-party plugin.

Mitigation: Review the plugin install and allowlist commands before installation, and only enable the plugin in a trusted OpenClaw workspace.

Risk: Write, batch delete, clear value, and data erasure tools can modify or remove user data.

Mitigation: Confirm sensitive reads and all writes yourself, with extra review for batch deletes, clear operations, sharing changes, Ads mutations, and other high-impact actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-super)
- [Google Workspace APIs](https://developers.google.com/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-super)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JavaScript-style tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes representative tool names and workflows for Google service read, write, and delete operations.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
