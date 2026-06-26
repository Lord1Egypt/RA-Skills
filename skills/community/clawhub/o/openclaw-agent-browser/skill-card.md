## Description: <br>
Agent Browser provides headless browser automation commands for agents to navigate sites, interact with elements, capture pages, extract data, test web apps, download files, and automate browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bodietron](https://clawhub.ai/user/bodietron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to drive browser sessions for web interaction, testing, data extraction, screenshots, downloads, and stateful login workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-driven browser automation can affect accounts, browser sessions, local files, uploads, downloads, and account-changing forms. <br>
Mitigation: Use an isolated browser profile, enable domain and action limits, and require explicit approval for logins, saved auth state, file access, uploads, downloads, and submitting account-changing forms. <br>
Risk: The setup script installs a global npm package and Chromium dependencies. <br>
Mitigation: Pin or verify the npm package before installation and run setup only in an environment intended for browser automation. <br>
Risk: Large or unbounded page output can flood an agent context or expose untrusted content. <br>
Mitigation: Enable content boundaries and output limits such as AGENT_BROWSER_CONTENT_BOUNDARIES and AGENT_BROWSER_MAX_OUTPUT. <br>


## Reference(s): <br>
- [agent-browser command reference](artifact/references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/bodietron/openclaw-agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with bash command examples and command-reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create browser state, screenshots, PDFs, downloads, and extracted page text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
