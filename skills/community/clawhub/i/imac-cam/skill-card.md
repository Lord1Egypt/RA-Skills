## Description:

Captures the iMac camera view from the Photo Booth window, crops the window borders, and provides a captured image for viewing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uni-huang](https://clawhub.ai/user/uni-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill when they want an agent to open Photo Booth on an iMac, capture the camera view, and return a viewable capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webcam imagery can be captured and exposed through an unauthenticated network server.

Mitigation: Require explicit user confirmation before capture and restrict viewing to authenticated or localhost-only access.

Risk: Serving /tmp can expose unrelated temporary files on shared or networked machines.

Mitigation: Serve only a private directory containing the intended capture file and shut the server down automatically after use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Plain text status and a PNG image file served over HTTP]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates /tmp/cam_capture.png and may start an unauthenticated HTTP server on port 8765 rooted at /tmp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
