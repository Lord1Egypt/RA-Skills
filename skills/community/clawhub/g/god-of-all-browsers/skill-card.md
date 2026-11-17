## Description:

A browser automation CLI for AI agents that uses a persistent Chromium session, multi-tab management, DOM snapshots, and command-line actions to navigate, interact with, and extract content from websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mathanmithun1999](https://clawhub.ai/user/mathanmithun1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to drive a local Chromium browser for web navigation, interaction, search, authentication checks, and data extraction workflows. It is intended for stateful browser automation where tags, tabs, cookies, screenshots, and extracted page data help an agent complete browsing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores browser login state, cookies, screenshots, recordings, and session data that can contain sensitive information.

Mitigation: Use an isolated environment with a disposable browser profile, avoid logging into sensitive accounts, treat session and recording files as secrets, and clear chrome_profile, session.json, and recordings after use.

Risk: The eval command can run arbitrary JavaScript in a persistent browser context.

Mitigation: Run only trusted inline code or script files, review agent-generated scripts before execution, and watch for network request patterns that could expose data.

Risk: The browser automation flow uses weak containment and bot-evasion techniques that may be inappropriate for some sites or policies.

Mitigation: Review the target site's rules before automation, keep the browser in a constrained environment, and update or constrain the Puppeteer dependency chain before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mathanmithun1999/skills/god-of-all-browsers)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)
- [Puppeteer documentation](https://pptr.dev/)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local browser profiles, session cookies, screenshots, snapshot JSON, eval results, and debug logs during operation.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact package.json and _meta.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
