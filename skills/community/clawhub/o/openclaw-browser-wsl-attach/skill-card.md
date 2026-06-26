## Description: <br>
Automatically prepares, repairs, and attaches an OpenClaw-controlled Chromium browser in WSL, root-run, or headless Linux environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenzheke](https://clawhub.ai/user/shenzheke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure attachOnly Chromium browser automation for OpenClaw and diagnose startup, CDP, and browser status failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow can change ~/.openclaw/openclaw.json and restart browser-related services. <br>
Mitigation: Review the configuration change first, keep the generated backup, and approve restarts only when browser repair is intended. <br>
Risk: The browser startup script can clean up Chromium processes using the configured remote debugging port. <br>
Mitigation: Confirm no important browser work is using the target port before running the startup script. <br>
Risk: Running Chromium with no-sandbox weakens Chromium isolation when required for root-run environments. <br>
Mitigation: Use no-sandbox only in the documented WSL, root-run, or headless repair context and prefer a non-root browser setup when available. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local diagnostic and setup guidance for OpenClaw browser attachment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
