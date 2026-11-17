## Description:

Capture frames or clips from RTSP/ONVIF cameras and local webcams, including USB pan/tilt/zoom control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to capture snapshots, short video clips, or motion events from configured RTSP/ONVIF cameras and local webcams, and to inspect or adjust supported PTZ cameras.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera credentials may be exposed if included directly in shell commands or left in an accessible configuration file.

Mitigation: Use a dedicated camera account, protect the local Camsnap configuration file, and avoid putting credentials in shared command history or logs.

## Reference(s):

- [Camsnap homepage](https://camsnap.ai)
- [Camsnap on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-camsnap)
- [Publisher profile: hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown instructions with inline shell commands and configuration examples; camera captures are image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and configuration depend on the selected camera and requested capture or PTZ operation.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
