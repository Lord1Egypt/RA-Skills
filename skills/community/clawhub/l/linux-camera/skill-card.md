## Description:

Capture photos, record video clips, list cameras, and live stream on Linux. Uses V4L2 and ffmpeg. Supports USB webcams and RTSP/IP cameras.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnynunez](https://clawhub.ai/user/johnnynunez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics operators use this skill to inspect Linux camera devices, capture still images, record short clips, and expose a live camera stream from USB webcams or RTSP/IP cameras.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The streaming server can expose live camera feeds and local files to anyone who can reach the port.

Mitigation: Run the skill only on trusted machines and networks, bind viewing to localhost where possible, and add authentication before remote access.

Risk: HLS streaming is called out by the security guidance as unsafe until a path traversal issue is fixed.

Mitigation: Do not enable HLS in production or shared environments until the path traversal issue has been remediated and rescanned.

Risk: Camera captures, clips, and live streams may contain sensitive visual data.

Mitigation: Use the skill only with consent and store generated media in approved locations with appropriate access controls.

## Reference(s):

- [linux-camera ClawHub Skill](https://clawhub.ai/johnnynunez/skills/linux-camera)
- [johnnynunez Publisher Profile](https://clawhub.ai/user/johnnynunez)
- [soarm-control Skill](https://clawhub.ai/yuyoujiang/soarm-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; scripts can produce JSON device listings, JPEG images, MP4 clips, MJPEG streams, HLS streams, RTSP streams, and status JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Camera outputs may contain sensitive visual data and depend on local Linux device access, ffmpeg, and v4l-utils.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
