## Description: <br>
Capture photos, record video clips, list cameras, and live stream on Linux. Uses V4L2 and ffmpeg. Supports USB webcams and RTSP/IP cameras. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnynunez](https://clawhub.ai/user/johnnynunez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics users use this skill to capture images, record video, enumerate Linux camera devices, and stream camera feeds from USB webcams or RTSP/IP cameras. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Streaming mode can expose live camera video on the network without authentication. <br>
Mitigation: Use streaming only on trusted networks, firewall the selected ports, avoid public or shared hosts, and prefer localhost binding if modifying the server. <br>
Risk: RTSP input URLs can include credentials that may appear in command lines or logs. <br>
Mitigation: Avoid placing sensitive RTSP credentials in shared shell history, command logs, or public examples. <br>


## Reference(s): <br>
- [linux-camera ClawHub page](https://clawhub.ai/johnnynunez/linux-camera) <br>
- [Publisher profile](https://clawhub.ai/user/johnnynunez) <br>
- [soarm-control Skill](https://clawhub.ai/yuyoujiang/soarm-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script outputs; scripts produce JPEG images, MP4 video, JSON camera listings, MJPEG/HLS/RTSP streams, and status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux camera access plus ffmpeg and v4l-utils.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
