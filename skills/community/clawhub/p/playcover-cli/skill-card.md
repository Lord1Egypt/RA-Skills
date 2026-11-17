## Description:

Guides agents in using PlayCover's command-line interface to manage iOS apps and related settings without the GUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dustink66](https://clawhub.ai/user/dustink66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this guide to install, launch, sign, export, and manage PlayCover apps from shell scripts, CI, or remote Macs. It also helps troubleshoot CLI invocations that open the GUI instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uninstall, cleanup, or reset commands can remove app data, keymaps, or settings.

Mitigation: Verify bundle IDs and paths and back up app data, keymaps, and settings before running these commands.

Risk: Downloaded IPA files or user dylibs may come from untrusted sources.

Mitigation: Use trusted IPA and dylib sources and review files before installation or injection.

Risk: Global configuration can suppress prompts or clear data during uninstall.

Mitigation: Review affected configuration keys and their effects before changing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dustink66/skills/playcover-cli)
- [PlayCover CLI contribution](https://github.com/PlayCover/PlayCover/pull/2238)
- [PlayCover CLI build downloads](https://github.com/maclub-net/PlayCover/releases)
- [App lifecycle commands](references/app-lifecycle.md)
- [CLI conventions](references/conventions.md)
- [Global configuration](references/config.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Text]

**Output Format:** [Markdown with shell examples and JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files or applications are modified by the guide itself.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
