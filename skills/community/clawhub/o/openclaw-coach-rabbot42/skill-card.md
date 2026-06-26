## Description: <br>
OpenClaw Coach syncs OpenClaw documentation into an Obsidian knowledge base, schedules daily OpenClaw usage tips, prompts the user to choose future tip topics, and reports version updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabbot42](https://clawhub.ai/user/rabbot42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to keep a local Obsidian OpenClaw knowledge base current and receive scheduled learning prompts, daily tips, and version update notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled scripts can overwrite files in the user's Obsidian OpenClaw folder. <br>
Mitigation: Back up the Obsidian folder and review the sync path and document list before enabling automatic sync. <br>
Risk: The messaging scripts send recurring OpenClaw messages to a fixed recipient identifier. <br>
Mitigation: Confirm the target identifier belongs to the intended user or replace it with user-controlled configuration before running the scripts. <br>
Risk: The skill fetches documentation and release data from GitHub during scheduled runs. <br>
Mitigation: Only enable scheduled sync if network access to the referenced OpenClaw GitHub endpoints and automatic updates are acceptable. <br>


## Reference(s): <br>
- [OpenClaw docs source](https://raw.githubusercontent.com/openclaw/openclaw/main/docs) <br>
- [OpenClaw latest release API](https://api.github.com/repos/openclaw/openclaw/releases/latest) <br>
- [ClawHub skill page](https://clawhub.ai/rabbot42/openclaw-coach-rabbot42) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown notes, JSON state, shell command output, and OpenClaw messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes OpenClaw docs and tip state under the user's Obsidian OpenClaw folder and sends recurring OpenClaw messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
