## Description:

Vision-driven Android device automation using Midscene that operates from screenshots to control Android devices with natural language commands over ADB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation agents use this skill to connect to Android devices or emulators, launch apps or URLs, inspect screenshots, perform UI actions, run assertions, and summarize mobile test results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over a connected Android device or emulator.

Mitigation: Use a dedicated test device or emulator and avoid sensitive accounts, private screens, and production data.

Risk: Raw ADB shell actions can make lower-level device changes outside visible UI automation.

Mitigation: Require explicit human confirmation before running raw ADB shell commands and review the exact command string.

Risk: Repeated npx -y execution can fetch mutable package code at runtime.

Mitigation: Prefer a pinned, audited Midscene package version or a locked project installation.

Risk: Screenshots and generated reports may capture sensitive screen content.

Mitigation: Store artifacts in controlled locations, review them before sharing, and delete unneeded screenshots, logs, and reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quanru/skills/midscene-android-automation)
- [ClawHub publisher profile](https://clawhub.ai/user/quanru)
- [Midscene.js](https://midscenejs.com)
- [Midscene model configuration](https://midscenejs.com/model-common-config)
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshot, report, log, or converted report file paths generated during Android automation runs.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
