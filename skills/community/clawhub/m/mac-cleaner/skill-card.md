## Description:

Analyze and safely clean disk space on macOS. Use when the user asks about Mac storage, "System Data" taking too much space, disk cleanup, freeing up space, or managing storage on macOS. Covers caches, iOS simulators, Xcode data, trash, logs, and browser caches. Safe for everyday Mac users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apprithm](https://clawhub.ai/user/apprithm)

### License/Terms of Use:


## Use Case:

External macOS users and developers use this skill to inspect disk usage, identify common storage-heavy locations, and run or review cleanup steps for caches, Xcode data, browser caches, logs, trash, and related storage items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup mode and manual examples include broad deletion commands that can remove user data if paths are misunderstood or copied without review.

Mitigation: Run analyze mode first, review the exact paths and backup folders, and only execute cleanup or manual deletion commands after confirming the data is no longer needed.

Risk: Some cleanup paths involve administrator privileges, old system logs, Time Machine snapshots, or Terminal Full Disk Access.

Mitigation: Avoid privileged or snapshot deletion commands unless the recovery impact is understood, and grant Full Disk Access or enter an administrator password only after reviewing the requested action.

## Reference(s):

- [Apple: Check Your Storage Space](https://support.apple.com/guide/mac-help/check-storage-space-mchlc03eb677/mac)
- [Apple: Free Up Storage Space on Your Mac](https://support.apple.com/en-us/HT202083)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text terminal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include macOS cleanup guidance, read-only analysis steps, and confirmation-gated cleanup commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
