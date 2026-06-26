## Description: <br>
kkclaw helps OpenClaw users add a persistent desktop interaction layer with a fluid glass UI, emotional state feedback, voice features, setup guidance, diagnostics, model switching, and Gateway monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk43994](https://clawhub.ai/user/kk43994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, and operate kkclaw as a desktop companion and operations helper for OpenClaw. It is most relevant for users who want visible task state, voice feedback, easier model and provider switching, and Gateway diagnostics during long-running agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and running an external desktop application can introduce local execution, persistence, configuration, and logging risks. <br>
Mitigation: Review the linked repository or release before installation, install from trusted sources, and confirm where configuration and logs are stored. <br>
Risk: Model provider and TTS setup may require API keys or other sensitive configuration. <br>
Mitigation: Use scoped and revocable API keys, avoid sharing credentials in logs or screenshots, and rotate keys if exposure is suspected. <br>
Risk: Resident Gateway or desktop helper behavior can continue running after setup. <br>
Mitigation: Confirm how to stop, disable, or uninstall kkclaw and any Gateway helper before relying on it for long-running use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kk43994/kkclaw) <br>
- [Setup Guide](references/setup.md) <br>
- [v3.1.2 Release Notes](references/v3-1-2.md) <br>
- [Why kkclaw](references/why-kkclaw.md) <br>
- [GitHub Repository](https://github.com/kk43994/kkclaw) <br>
- [GitHub Releases](https://github.com/kk43994/kkclaw/releases) <br>
- [Online Demo](https://kk43994.github.io/kkclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may reference external desktop application installation, OpenClaw Gateway configuration, model and provider settings, TTS setup, and diagnostics.] <br>

## Skill Version(s): <br>
3.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
