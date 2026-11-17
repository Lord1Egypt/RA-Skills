## Description:

Schedules macOS application launches and quits by translating natural-language or cron-style timing requests into launchd LaunchAgent plist files and launchctl actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skkypy](https://clawhub.ai/user/skkypy)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users and automation developers use this skill to preview, create, inspect, trigger, and remove scheduled application start and quit jobs. It is suited for user-level LaunchAgent automation where commands and plist changes should be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent LaunchAgent operations could overwrite or delete unintended plist files or run unintended local code if validation is insufficient.

Mitigation: Require dry-run previews, avoid --yes, use only trusted application paths and simple labels, and verify remove operations target only this skill's own com.user.launch.* plist files.

Risk: The server security verdict is suspicious due to unsafe validation around persistent scheduling behavior.

Mitigation: Install only after the publisher fixes validation and review every write, load, unload, and remove action before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skkypy/skills/launchctl)
- [Publisher profile](https://clawhub.ai/user/skkypy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and launchd plist snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or preview LaunchAgent plist content and launchctl commands; dry-run preview is expected before write, load, unload, or remove actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
