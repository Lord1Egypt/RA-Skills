## Description:

Capture a fresh webcam image on macOS, Windows, or Linux, preferring direct ffmpeg camera capture over screen-recording, accessibility, or UI automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurc2004](https://clawhub.ai/user/laurc2004)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when an assistant needs to capture a fresh image from a local webcam and return it as a media file. It supports direct camera capture across macOS, Windows, and Linux, with a macOS app-window screenshot fallback when direct capture is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a local camera and may capture sensitive visual information.

Mitigation: Install and run it only in environments where camera access is expected, and rely on operating-system camera permission prompts and user consent.

Risk: The macOS fallback can capture an app window or the whole screen and requires Screen Recording, Accessibility, and Automation permissions.

Mitigation: Prefer the direct ffmpeg webcam path and use the fallback only when direct capture fails or a visible camera-app UI is explicitly required.

Risk: The macOS fallback has unsafe AppleScript argument handling according to the security evidence.

Mitigation: Do not pass untrusted app names or delay values to fallback scripts, and review the skill before installation or deployment.

## Reference(s):

- [Photo Capture Skill on ClawHub](https://clawhub.ai/laurc2004/skills/photo-capture)
- [FFmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [files, shell commands, markdown, guidance]

**Output Format:** [Markdown response with MEDIA path references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local PNG or JPEG image file under the workspace tmp directory when capture succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
