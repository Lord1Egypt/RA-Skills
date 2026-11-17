## Description: <br>
Photo Webcam Tool Free helps an agent manage webcam favorites, fetch current public webcam snapshots by URL or saved ID, and save downloaded images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users and developers use this skill to help agents fetch public webcam images for travel views, weather, road checks, and saved camera lists. It supports favorites stored as JSON, direct image URLs, single-camera downloads, and small batch snapshot retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Snapshot retrieval contacts public webcam pages and image URLs, which may be unavailable, rate limited, or changed by the source site. <br>
Mitigation: Use trusted public camera sources, prefer direct image URLs when available, and expect temporary failures for offline or changed cameras. <br>
Risk: User-selected output paths can write snapshot files to locations the agent can access. <br>
Mitigation: Prefer temporary output paths such as /tmp and avoid paths that target sensitive or important files. <br>
Risk: An optional callback_url may receive result data after processing. <br>
Mitigation: Only provide callback_url values for trusted destinations and omit callbacks when result forwarding is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/photo-webcam-tool-free) <br>
- [foto-webcam.eu public webcam platform](https://www.foto-webcam.eu/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets; JPG snapshot files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or edit a favorites JSON file, download public webcam images, and write snapshot files to user-specified paths; optional callback_url can receive result data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
