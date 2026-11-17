## Description:

Play Local Music helps an agent control local audio playback with commands to play, pause, resume, stop, list songs, and report status from a configured music directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awspace](https://clawhub.ai/user/awspace)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to operate a local music player through a single command interface. It is intended for trusted local environments where an agent may start playback, select songs, and manage playback state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local background server opens a localhost control port and accepts playback commands without authentication.

Mitigation: Use only in a trusted local-user environment and prefer a hardened version with authenticated control requests.

Risk: The default lock file is written under /tmp with world-writable permissions.

Mitigation: Configure a private per-user runtime directory and restrictive lock-file permissions.

Risk: Song selection depends on local paths and configured music directories.

Mitigation: Validate song names and constrain playback to the intended music directory.

Risk: Server shutdown guidance may rely on broad process-matching commands.

Mitigation: Prefer targeted server-stop behavior and avoid running the skill with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awspace/skills/play-music)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
