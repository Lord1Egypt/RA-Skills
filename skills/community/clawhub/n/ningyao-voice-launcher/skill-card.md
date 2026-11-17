## Description:

Install and configure a local browser-based Chinese voice chat launcher with the Ning Yao persona, including one-click Windows launchers, browser speech I/O, screen awareness, and a safe terminal panel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwannian](https://clawhub.ai/user/jiwannian)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to install a local Chinese voice companion launcher, configure model access, and run browser-based speech input, speech output, screen awareness, and a restricted terminal panel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat history and shared screen content can be sent to the configured model provider.

Mitigation: Use only with trusted providers, share only intended screen content, and keep API keys out of shared folders or version control.

Risk: The local web server exposes sensitive APIs, including a browser terminal panel.

Mitigation: Bind the server to loopback, add per-launch authentication, and disable or remove the terminal endpoint before broader use.

Risk: The security guidance calls out file-read and HTML rendering issues.

Mitigation: Fix the file-read and innerHTML issues before production or shared-machine use.

Risk: Dependencies may need regeneration from a trusted source.

Mitigation: Regenerate dependencies from a trusted registry and review the lockfile before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiwannian/skills/ningyao-voice-launcher)
- [Publisher Profile](https://clawhub.ai/user/jiwannian)
- [Skill README](README.md)
- [Local Launcher README](assets/voice-chat-local/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline PowerShell and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and configuration steps for a local browser voice chat launcher.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
