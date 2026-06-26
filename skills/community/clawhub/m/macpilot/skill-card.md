## Description: <br>
Control macOS via CLI using MacPilot for automating UI actions, managing windows, handling file dialogs, capturing screenshots, and system tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adhikjoshi](https://clawhub.ai/user/adhikjoshi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use this skill to operate macOS applications through MacPilot CLI commands for UI automation, dialogs, window management, screenshots, OCR, clipboard workflows, and shell-driven desktop tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad desktop-level macOS control across apps, dialogs, screen capture, clipboard history, and shell commands. <br>
Mitigation: Install only when this level of desktop control is intended, use explicit approvals for sensitive actions, and revoke macOS permissions when no longer needed. <br>
Risk: Automated shell commands, file writes or overwrites, permission prompts, screenshots, recordings, and clicks in sensitive apps can cause unintended disclosure or changes. <br>
Mitigation: Require user confirmation for those actions, review proposed commands before execution, and avoid running the skill in sensitive apps without a clear task need. <br>
Risk: Clipboard history can retain sensitive content after automation completes. <br>
Mitigation: Stop and clear clipboard history when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adhikjoshi/macpilot) <br>
- [MacPilot project](https://github.com/adhikjoshi/macpilot) <br>
- [Vercel Labs skills CLI](https://github.com/vercel-labs/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operational guidance for MacPilot CLI usage; command outputs may include JSON when the documented --json flag is used.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
