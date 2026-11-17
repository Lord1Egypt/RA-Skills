## Description:

Automate iOS Simulator workflows (simctl + idb): create/boot/erase devices, install/launch apps, push notifications, privacy grants, screenshots, and accessibility-based UI navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to manage iOS Simulator devices, install and launch apps, capture screenshots and video, inspect accessibility UI state, and automate simulator interactions during iOS app testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulator clipboard contents, UI dumps, logs, app containers, screenshots, videos, and push payloads may contain sensitive test data.

Mitigation: Use the skill only in macOS/Xcode test environments, avoid production credentials or real user data, and review artifacts before sharing or storing them.

Risk: Erase, delete, privacy, push, clipboard, and open URL commands can alter simulator or app state.

Mitigation: Target an explicit simulator UDID when practical, review commands before execution, and reserve destructive erase/delete operations for intended test devices.

Risk: UI automation depends on idb and accessibility labels, so ambiguous or stale UI state can cause unintended taps or text entry.

Mitigation: Inspect UI summaries or trees before semantic taps, narrow query text for multiple matches, and verify idb-related dependencies in stricter environments.

## Reference(s):

- [iOS Simulator Skill on ClawHub](https://clawhub.ai/tristanmanchester/skills/ios-simulator)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI output that defaults to single-line JSON, with optional pretty JSON or short text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces simulator state files, screenshots, videos, app container paths, UI summaries, logs, and command result objects when the corresponding CLI commands are run.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
