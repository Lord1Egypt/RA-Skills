## Description: <br>
Captures an iMac camera view from the Photo Booth window when a user asks to open or view the camera or monitor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uni-huang](https://clawhub.ai/user/uni-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill on macOS to capture the current Photo Booth camera view, crop the window frame, and receive a local URL for viewing the captured image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures camera output from Photo Booth and saves it under /tmp. <br>
Mitigation: Require explicit consent before capture, store the image in a dedicated private location, and delete it after use. <br>
Risk: The skill starts an unauthenticated HTTP server on port 8765 that may expose the captured image or other /tmp files to the local network. <br>
Mitigation: Serve only a dedicated private directory or localhost-only URL, and stop the server when sharing is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uni-huang/imac-cam) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [PNG image file with terminal text containing a local HTTP URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the capture to /tmp/cam_capture.png and may start a background HTTP server on port 8765.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
