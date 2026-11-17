## Description:

Kimi WebBridge lets agents control a user's real browser to navigate pages, click, type, read content, take screenshots, upload files, capture network data, and save pages using existing browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgfuying](https://clawhub.ai/user/wgfuying)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill to automate real-browser website tasks that need an authenticated browser session, including navigation, content extraction, screenshots, form interaction, uploads, and PDF capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad authenticated browser control can interact with sensitive logged-in websites, submit forms, upload files, or save to custom paths.

Mitigation: Install only when this control is intended, avoid sensitive sites, and require explicit confirmation before using existing tabs, submitting forms, uploading files, or writing custom paths.

Risk: Persistent background browser automation behavior may continue across agent sessions or system restarts.

Mitigation: Review the daemon lifecycle before installation and keep browser automation limited to tasks the user has approved.

Risk: The artifact describes task cleanup that may close browser tabs or terminate Quark browser processes.

Mitigation: Warn the user before cleanup when they may have personal Quark windows open, and prefer session-only tab cleanup when process termination is not appropriate.

## Reference(s):

- [ClawHub listing: Kimi WebBridge](https://clawhub.ai/wgfuying/skills/kimi-webbridge)
- [Source repository: WGfuying/kimi-webbridge](https://github.com/WGfuying/kimi-webbridge)
- [Kimi WebBridge documentation](https://www.kimi.com/features/webbridge)
- [Operations guide](references/operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Files]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser screenshots or PDFs as local files when the user requests capture or export.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
