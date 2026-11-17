## Description:

Office Automation Toolkit helps agents choose and install CLI tools and Python packages for office document, PDF, browser automation, web scraping, and messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and office-automation agents use this skill to identify appropriate tools for Excel, CSV, Word, PowerPoint, PDF, browser, web, and messaging tasks and to bootstrap those tools when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap script may install Python packages, operating-system packages, and Playwright browser assets.

Mitigation: Run the script with --check-only first, review the package list, and approve installation only in an appropriate environment.

Risk: Some installation paths use package managers that may request elevated privileges.

Mitigation: Avoid running with elevated privileges unless the environment requires it and the requested packages have been reviewed.

Risk: Messaging integrations may bind available Feishu, WeCom, or DingTalk credentials from environment variables.

Mitigation: Confirm the intended messaging identity and environment variables before enabling messaging automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/skills/office-automation-toolkit)
- [Tool quick reference](artifact/references/tool-quick-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline install commands, tool tables, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or run a bootstrap script that checks and installs office automation dependencies.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
