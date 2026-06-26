## Description: <br>
Vision-driven Android device automation using Midscene that controls visible Android UI from screenshots through ADB-backed commands for taps, swipes, text input, app launches, screenshots, assertions, and shell operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanru](https://clawhub.ai/user/quanru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate Android app workflows, inspect visible mobile UI state, and verify behavior on an emulator or connected test device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a connected Android device. <br>
Mitigation: Use an emulator or dedicated test device with test accounts, avoid sensitive screens, and keep the target app visually confirmed before automation. <br>
Risk: Raw ADB shell commands, installs, uninstalls, deletion, settings changes, purchases, form submissions, or actions affecting real accounts can have high impact. <br>
Mitigation: Require explicit user approval before running those operations, and prefer bounded UI actions or assertions when lower-level device control is not necessary. <br>
Risk: The skill requires model API credentials for Midscene. <br>
Mitigation: Keep API keys private, use local environment configuration, and do not expose credentials in prompts, screenshots, logs, or generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanru/midscene-android-automation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/quanru) <br>
- [Midscene.js](https://midscenejs.com) <br>
- [Midscene model configuration](https://midscenejs.com/model-common-config) <br>
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional generated report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference screenshots, logs, and Midscene report files produced during Android automation runs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
