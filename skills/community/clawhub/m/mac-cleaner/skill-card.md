## Description: <br>
Analyze and safely clean disk space on macOS. Use when the user asks about Mac storage, "System Data" taking too much space, disk cleanup, freeing up space, or managing storage on macOS. Covers caches, iOS simulators, Xcode data, trash, logs, and browser caches. Safe for everyday Mac users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apprithm](https://clawhub.ai/user/apprithm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Mac users and support agents use this skill to inspect disk usage, identify common macOS storage consumers, and run guided cleanup steps for caches, Xcode data, browser caches, old logs, and Trash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clean mode can permanently delete caches, Trash contents, and old system logs after confirmation. <br>
Mitigation: Run analyze mode first and only run clean mode when the user accepts permanent deletion of those items. <br>
Risk: Old log cleanup may require an administrator password and can remove logs that are useful for troubleshooting, compliance, or incident review. <br>
Mitigation: Skip or modify log cleanup when recent or historical logs need to be preserved. <br>


## Reference(s): <br>
- [Apple: Check storage space on your Mac](https://support.apple.com/guide/mac-help/check-storage-space-mchlc03eb677/mac) <br>
- [Apple: Free up storage space on your Mac](https://support.apple.com/en-us/HT202083) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and terminal output from the cleanup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyze mode is read-only; clean mode prompts before deleting rebuildable caches, old logs, and Trash contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
