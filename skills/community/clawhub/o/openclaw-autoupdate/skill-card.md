## Description:

Automates OpenClaw updates by checking installed versions, downloading the latest OpenClaw release, updating the menu bar app and CLI, restarting the gateway, and logging the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmieting](https://clawhub.ai/user/jimmieting)

### License/Terms of Use:


## Use Case:

Developers and operators who use OpenClaw can invoke this skill to update the local OpenClaw CLI, macOS menu bar application, and gateway service from the latest available release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can replace the installed OpenClaw application and global CLI without interactive review.

Mitigation: Require explicit approval before each update and confirm that the user intends to update both the app and CLI.

Risk: The updater downloads release artifacts and installs the npm package from mutable remote sources.

Mitigation: Pin or verify release artifacts and npm versions before execution.

Risk: The updater removes the existing macOS application before installing the replacement.

Mitigation: Keep a rollback copy of the existing OpenClaw app and CLI before running the update.

Risk: The updater installs a macOS application artifact.

Mitigation: Confirm the expected macOS signing identity before accepting the installed app.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmieting/skills/openclaw-autoupdate)
- [OpenClaw latest release API endpoint used by the updater](https://api.github.com/repos/openclaw/openclaw/releases/latest)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill invokes a shell updater that writes execution logs to ~/.openclaw/logs/autoupdate.log.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
