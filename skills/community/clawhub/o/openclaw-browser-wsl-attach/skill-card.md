## Description:

Automatically prepare, repair, and attach an OpenClaw-controlled Chromium browser in WSL or Linux environments where OpenClaw runs as root or in a headless session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenzheke](https://clawhub.ai/user/shenzheke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure, start, and diagnose a reusable Chromium attachOnly browser session in WSL, root-run, or headless Linux environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill weakens browser isolation by configuring Chromium for root or headless operation with no sandbox.

Mitigation: Prefer running Chromium as an unprivileged user with sandboxing enabled when possible, and review the configuration before applying it.

Risk: The configuration script persistently modifies ~/.openclaw/openclaw.json.

Mitigation: Review the generated settings first and keep the timestamped backup so the previous configuration can be restored.

Risk: The startup script may kill existing Chromium processes using the configured CDP port.

Mitigation: Save active browser work before running it, or use OPENCLAW_BROWSER_CDP_PORT to avoid a port already used by another session.

Risk: A reusable browser profile can retain session state from browser automation.

Mitigation: Keep the OpenClaw browser profile separate from sensitive personal or production browsing sessions.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/shenzheke/skills/openclaw-browser-wsl-attach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and script execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local configuration changes, Chromium startup, browser health checks, and troubleshooting diagnostics.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
