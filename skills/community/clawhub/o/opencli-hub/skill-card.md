## Description:

OpenCLI helps agents use website command-line commands and browser automation for public APIs, logged-in site workflows, and selected external CLIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensu1234](https://clawhub.ai/user/chensu1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to run OpenCLI commands for website search, feeds, rankings, page interaction, screenshots, scraping, and supported external CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive a logged-in Chrome session, inspect pages, take screenshots, click controls, and type into websites.

Mitigation: Use it in a constrained environment and require user confirmation before sensitive browser, account, payment, posting, or data-changing actions.

Risk: The skill can trigger installation of missing external command-line tools.

Mitigation: Require explicit approval before installation and review the tool source, package manager action, and requested permissions first.

Risk: Browser automation and scraping may expose private account data or page content in agent-visible outputs.

Mitigation: Limit use to appropriate accounts and pages, avoid sensitive sessions, and redact private content before sharing outputs outside the local workflow.

## Reference(s):

- [OpenCLI ClawHub skill page](https://clawhub.ai/chensu1234/skills/opencli-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with inline shell commands; some OpenCLI commands may return JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include command results, browser state summaries, scraped page content, screenshots, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
