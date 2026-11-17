## Description:

Control ONVIF Profile S/T IP cameras for PTZ, presets, discovery, and RTSP snapshot or recording workflows with auto-discovery and multi-camera support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltpop](https://clawhub.ai/user/ltpop)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and external users use this skill to configure and control ONVIF-compatible IP cameras, discover cameras on a local network, move PTZ cameras, manage presets, and capture RTSP snapshots or recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles camera credentials and live camera feeds.

Mitigation: Use a dedicated low-privilege camera account and install only in environments where access to those feeds and credentials is acceptable.

Risk: Camera configuration can store passwords and connection details locally.

Mitigation: Restrict permissions on the configuration file and avoid sharing configuration contents.

Risk: The stream-url command can expose a usable RTSP URL.

Mitigation: Do not share stream-url output and prefer workflows that avoid placing passwords directly in command-line arguments.

Risk: Installation uses an unpinned Python dependency.

Mitigation: Review or pin the dependency before running install.sh in a controlled or production environment.

Risk: Discovery and camera control operate on the local network and can move PTZ hardware or create local surveillance media.

Mitigation: Run discovery only on networks where camera scanning is authorized and store snapshots or recordings in approved local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ltpop/skills/ipcam)
- [Publisher profile](https://clawhub.ai/user/ltpop)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Camera commands can produce RTSP stream URLs and local snapshot or recording files when executed against configured cameras.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
