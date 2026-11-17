## Description:

Headless browser automation CLI for AI agents. Use when interacting with websites: navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, scraping, testing web apps, downloading files, or automating browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bodietron](https://clawhub.ai/user/bodietron)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate browser workflows such as web navigation, form submission, application testing, screenshots, downloads, data extraction, and session reuse through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a browser, submit forms, download files, and run page JavaScript through the agent-browser CLI.

Mitigation: Use domain allowlists, action policies, content boundaries, and human review for sensitive browsing or form-submission workflows.

Risk: The skill supports credential handling and reusable browser state, which can expose accounts if saved state files are mishandled.

Mitigation: Avoid saving credentials or auth state unless needed, store state files securely, and treat saved state like passwords.

Risk: The skill can connect to existing Chrome profiles and access local files when those modes are enabled.

Mitigation: Use an isolated browser profile and avoid attaching the skill to an everyday Chrome profile or broad local file paths.

Risk: The setup script installs agent-browser globally with npm and downloads Chromium without a pinned package version.

Mitigation: Review the installer before use or install a pinned, isolated version in a controlled environment.

## Reference(s):

- [Agent Browser ClawHub Page](https://clawhub.ai/bodietron/skills/openclaw-agent-browser)
- [agent-browser Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser snapshots, screenshots, PDFs, downloaded files, saved session state, extracted page text, and command output when the CLI is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
