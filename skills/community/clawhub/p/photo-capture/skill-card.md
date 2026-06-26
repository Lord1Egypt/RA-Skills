## Description: <br>
Capture a fresh webcam image on macOS, Windows, or Linux, preferring direct camera capture via ffmpeg so the workflow does not depend on screen-recording, accessibility, or UI automation permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laurc2004](https://clawhub.ai/user/laurc2004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent capture a live webcam image, save it in the workspace, and return the saved image path. It supports device selection and resolution settings, with a macOS app-window screenshot fallback only when direct ffmpeg capture is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The macOS fallback can automate camera apps and capture an app window or full screen, which may include visible desktop content beyond the camera image. <br>
Mitigation: Prefer the direct ffmpeg webcam path, use the fallback only when direct capture fails or the user explicitly requests visible app UI, and confirm the required Screen Recording, Accessibility, and Automation permissions are acceptable. <br>
Risk: Captured photos may contain people, private spaces, or other sensitive visual information and are saved as local image files. <br>
Mitigation: Confirm people in view consent before capture, save only to the intended workspace path, and delete saved images that are no longer needed. <br>
Risk: The skill depends on local ffmpeg and camera-device access, so capture may fail or select the wrong camera on multi-device systems. <br>
Mitigation: List available devices before capture when multiple cameras are present, pass an explicit device when needed, and verify the output file exists and is not empty. <br>


## Reference(s): <br>
- [Photo Capture Skill on ClawHub](https://clawhub.ai/laurc2004/photo-capture) <br>
- [ffmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown response with shell commands and a MEDIA path to a generated image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PNG or JPEG image files under a workspace path selected by the agent or user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
