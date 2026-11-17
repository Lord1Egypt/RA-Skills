## Description:

Playwright CLI automates browser testing and web interaction through command-line controls for navigation, screenshots, form filling, clicking, code execution, session management, network interception, and video recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensu1234](https://clawhub.ai/user/chensu1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, testers, and agent builders use this skill to drive browser sessions from shell commands for web testing, data collection, screenshots, PDF export, network inspection, and repeatable UI interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable global tooling.

Mitigation: Use a pinned, reviewed package version and avoid running installation commands with elevated privileges.

Risk: Browser state files, cookies, localStorage, screenshots, PDFs, traces, videos, and network logs may contain sensitive information.

Mitigation: Run commands only on approved sites, avoid production authenticated sessions unless needed, and clean up generated artifacts and session data after use.

Risk: The skill exposes browser controls for storage changes, network interception, code execution, and destructive session operations.

Mitigation: Review planned commands before execution and scope them to intended test sessions, approved domains, and disposable browser profiles where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chensu1234/skills/playwright-cli-tool)
- [Publisher profile](https://clawhub.ai/user/chensu1234)
- [Playwright TodoMVC demo used in examples](https://demo.playwright.dev/todomvc/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, traces, videos, storage state files, and network logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
