## Description:

Automates web browser interactions through natural-language CLI commands for browsing, navigation, data extraction, screenshots, form filling, clicks, and web application interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q262045312-ui](https://clawhub.ai/user/q262045312-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to direct a browser with natural-language CLI commands for website navigation, form interaction, screenshots, data extraction, and web application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can preserve cookies, passwords, and other session state in a persistent browser profile.

Mitigation: Use isolated profiles, avoid sensitive accounts unless explicitly required, and clear stored browser data after use.

Risk: Screenshots and downloads may be saved locally and can contain sensitive or untrusted content.

Mitigation: Protect and periodically clear screenshot and download directories, and review downloaded files before opening them.

Risk: The browser can access internal sites and network resources available from the runtime environment.

Mitigation: Run the skill in an environment with only the network access needed for the task.

Risk: The skill can switch to Browserbase automatically when Browserbase API keys are present.

Mitigation: Confirm environment variables and API keys before use so browser sessions run in the intended local or remote environment.

## Reference(s):

- [Openclaw Browser Automation 1.0.1 on ClawHub](https://clawhub.ai/q262045312-ui/skills/openclaw-browser-automation-1-0-1)
- [Browser Automation Examples](artifact/EXAMPLES.md)
- [Browser Automation CLI Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI JSON/file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser commands may save screenshots under ./agent/browser_screenshots/ and downloads under ./agent/downloads/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
