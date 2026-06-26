## Description: <br>
Use when the user wants a local visual operations dashboard for OpenClaw, with a cute robot presentation, live status visibility, chat access, efficiency trend monitoring, and optional recovery helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasZH7](https://clawhub.ai/user/LucasZH7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solo builders, and operators use this skill to install, run, configure, and present a local dashboard for supervising one OpenClaw agent. It supports live status review, chat access, trend monitoring, and optional recovery helpers for local single-agent supervision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer creates persistent macOS background services while referenced runtime files are not included for review. <br>
Mitigation: Prefer foreground or non-persistent local startup with ./run_monitor.sh or ./start_bg.sh; review install_launchd.sh before enabling launchd persistence. <br>
Risk: Persistent services may remain active after installation. <br>
Mitigation: Use uninstall_launchd.sh to remove the LaunchAgents when persistence is no longer intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/LucasZH7/openclaw-studio) <br>
- [Publisher Profile](https://clawhub.ai/user/LucasZH7) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
