## Description:

Connects to and controls an Acasis Flow HID dock on Windows, including connection checks, page switching, report reads, and raw payload sends for the device VID=0x35e6 PID=0xa4ac.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facaihero](https://clawhub.ai/user/facaihero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control a physically connected Acasis Flow HID dock from a Windows host, including switching dock views, verifying the target device, reading reports, and sending raw payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an unverified Windows executable from GitHub.

Mitigation: Install only after trusting the publisher and release; prefer a release with a published SHA-256 checksum or code signature.

Risk: The executable runs as the Windows user and can interact with the target HID device.

Mitigation: Use it only with the intended Acasis Flow dock and review commands before sending raw payloads.

Risk: The HID device may be unavailable if another application has exclusive access.

Mitigation: Close other dock-control software before running connection, read, or view-switching commands.

## Reference(s):

- [ClawHub Hid Dock skill page](https://clawhub.ai/facaihero/skills/hid-dock)
- [Publisher profile: facaihero](https://clawhub.ai/user/facaihero)
- [hid-dock Windows x64 release archive](https://github.com/facaiHero/hid-dock/releases/download/v1.0.0/hid-dock-win-x64.zip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; commands target a fixed HID VID/PID and may run a downloaded executable.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
