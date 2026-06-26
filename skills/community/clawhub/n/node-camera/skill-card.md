## Description: <br>
Controls a paired Android Node device's USB camera for single-frame capture, streaming frame delivery, stopping streams, and closing camera callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxx328](https://clawhub.ai/user/lxx328) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to capture one-off images or stream JPEG frames from a paired Node device for remote monitoring, troubleshooting, and vision analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera capture and streaming can expose private spaces or sensitive visual data. <br>
Mitigation: Install only where camera monitoring is intended, prefer single-frame capture when possible, and avoid capturing sensitive spaces unless the Node network and image URLs are trusted. <br>
Risk: Live streaming and retained image URLs can continue consuming bandwidth, power, or exposing recent images if left running. <br>
Mitigation: Start streaming only when needed, call camera.stopStreaming or camera.close after use, and rely on the skill's documented recent-image cleanup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxx328/node-camera) <br>
- [Publisher profile](https://clawhub.ai/user/lxx328) <br>
- [Server provenance](unavailable) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, shell commands] <br>
**Output Format:** [Markdown guidance with JSON command examples and optional helper script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Camera capture and stream events return JPEG image URLs hosted by the Node device; the bundled helper can download URLs or inspect frame JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
