## Description:

Configures Clawdbot for headless browser automation with Playwright-managed Chromium on WSL/Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install Chromium dependencies, configure Clawdbot's browser executable, and enable headless browser automation in WSL/Linux or container-like environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future browser sessions may run with Chromium sandboxing disabled.

Mitigation: Enable sandboxing when the host supports it and run browser automation under a low-privilege account.

Risk: Setup may run unpinned npm/Playwright code and privileged package-manager commands.

Mitigation: Pin the Playwright version and review package-manager commands before running setup.

Risk: The skill can persistently change Clawdbot browser configuration.

Mitigation: Inspect the proposed configuration patch and keep a restorable copy of the previous Clawdbot browser settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/playwright-headless-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata; matches target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
