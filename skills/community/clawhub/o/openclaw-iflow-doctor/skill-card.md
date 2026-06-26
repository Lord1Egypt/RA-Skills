## Description: <br>
AI-powered auto-repair system for OpenClaw with iflow integration that automatically diagnoses and fixes crashes, configuration errors, and model issues, and falls back to iflow-helper when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kosei-echo](https://clawhub.ai/user/kosei-echo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw startup, gateway, memory, configuration, model, API, permission, and installation failures. It attempts automatic repair for common cases and provides reports, scripts, and iFlow-assisted guidance when manual intervention is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an always-on watchdog and persistent startup service. <br>
Mitigation: Use manual or diagnosis-only mode unless continuous OpenClaw auto-repair is intentional; avoid root or SYSTEM persistence unless operationally required. <br>
Risk: Generated repair scripts may make high-impact system or OpenClaw configuration changes. <br>
Mitigation: Review every generated .bat or .sh file before execution and back up OpenClaw configuration and memory data first. <br>
Risk: Logs and support context may contain API keys, settings, or other sensitive data. <br>
Mitigation: Redact raw API keys, settings files, and logs before sharing them in support chats or external tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kosei-echo/openclaw-iflow-doctor) <br>
- [README](artifact/README.md) <br>
- [Install Guide](artifact/INSTALL_GUIDE.md) <br>
- [iFlow Auth Guide](artifact/docs/iflow-auth-guide.md) <br>
- [Release Notes](artifact/RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, generated repair scripts, and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local diagnosis reports, repair scripts, watchdog logs, and OpenClaw configuration changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
