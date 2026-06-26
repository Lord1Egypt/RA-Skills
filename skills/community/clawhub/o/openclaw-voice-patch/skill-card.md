## Description: <br>
Patch OpenClaw Control UI to add hold-for-continuous voice input through one mic button, with short click for auto-send and a 3-second hold for continuous mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elzershark](https://clawhub.ai/user/elzershark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to patch the local OpenClaw Control UI after updates or when voice input needs auto-send and continuous recording behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies installed OpenClaw Control UI application files, which can break the UI if the target file or OpenClaw version does not match the expected patterns. <br>
Mitigation: Confirm the exact OpenClaw install path, create a backup of the target JavaScript file, verify the documented compatibility patterns before editing, and restore from backup if verification fails. <br>
Risk: Permission changes used to access installed files can be broader than necessary. <br>
Mitigation: Avoid broad chown or chmod commands; prefer copying the target file into the workspace for patching or granting the narrowest needed write access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elzershark/openclaw-voice-patch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through local file discovery, backup, compatibility checks, patch application, verification, restart, and rollback.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
