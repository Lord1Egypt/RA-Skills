## Description:

Use Playwright to browse websites with a real, non-headless browser and extract rendered page content or network responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elijahxb](https://clawhub.ai/user/elijahxb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to open browser sessions, navigate web pages, extract rendered DOM text and links, click matching links, search page content, capture API responses, and save browser outputs when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network response capture can collect sensitive content from logged-in or private browsing sessions.

Mitigation: Use the skill only in a sandbox or non-sensitive browser session, and avoid logged-in or private sites when response capture is enabled.

Risk: Bundled workflows read local attendance files and write reports, images, or screenshots to local paths.

Mitigation: Remove or separate the attendance, Sina image, and 12306 scripts unless those workflows are intentionally required, and review output paths before running them.

Risk: Browser automation can navigate to arbitrary or hard-coded external sites.

Mitigation: Validate URLs, constrain allowed domains for planned tasks, and follow the target site's terms before navigation or data extraction.

Risk: The dependency declaration is not fully pinned.

Mitigation: Pin dependencies and re-scan the release before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elijahxb/skills/playwright-browser)
- [ClawHub publisher profile](https://clawhub.ai/user/elijahxb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; helper scripts may emit JSON, screenshots, downloaded images, or Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network capture can include response bodies; some bundled workflows write files to local user paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
