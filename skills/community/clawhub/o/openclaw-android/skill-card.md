## Description: <br>
Controls a rooted Android device through OpenClaw by running local shell commands for app management, screen input, screenshots, and package listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssrlxl123](https://clawhub.ai/user/ssrlxl123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, testers, and device operators use this skill to automate Android application workflows on rooted devices, including launching apps, tapping and swiping, entering text, taking screenshots, installing or removing packages, and inspecting installed apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root-level Android automation can clear app data, install or uninstall apps, list files, and control screen input. <br>
Mitigation: Install only on a dedicated test or managed device, and require explicit human approval before clear, install, uninstall, screenshot, or filesystem-listing actions. <br>
Risk: Typed text and command arguments may be persisted in device logs. <br>
Mitigation: Avoid entering secrets through the text command and review or clean logs written under /sdcard/Download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssrlxl123/openclaw-android) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended to run on an Android device with root access and write execution logs under /sdcard/Download.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
