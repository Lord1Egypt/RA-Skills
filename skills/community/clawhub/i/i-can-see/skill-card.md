## Description:

i-can-see gives OpenClaw visual perception by capturing an ESP32-CAM image when a user asks it to look, take a photo, or describe what it sees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaibuzai](https://clawhub.ai/user/libaibuzai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent capture a real-world camera image, inspect the saved photo with a vision tool, and answer questions about the visible scene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture real-world photos through broad natural-language triggers.

Mitigation: Narrow the trigger wording and require explicit user confirmation before each camera capture.

Risk: The camera endpoint is hardcoded and unauthenticated.

Mitigation: Secure or isolate the ESP32-CAM network and install only when the configured endpoint is trusted.

Risk: Saved photos may contain private or sensitive visual information.

Mitigation: Define where images are stored, who can access them, and when they should be deleted.

Risk: Vision responses may be incorrect or misleading.

Mitigation: Validate important image-analysis results before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libaibuzai/skills/i-can-see)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and saved JPEG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves photos to a caller-provided local path; requires Python requests and access to the configured ESP32-CAM endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
