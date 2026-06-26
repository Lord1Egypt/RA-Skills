## Description: <br>
Doubao Media helps agents use a logged-in Doubao browser session to call chat/completion, capture SSE and browser network responses, extract image and video asset URLs, and optionally download generated media files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangm199](https://clawhub.ai/user/huangm199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technically capable users use this skill to inspect Doubao web media-generation flows and retrieve generated image or video assets from API responses or browser network traffic. It is suited to workflows that need captured media URLs, downloaded assets, session readiness checks, or capture manifests from a logged-in Doubao web session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill acts through a logged-in Doubao browser session and handles browser cookies. <br>
Mitigation: Use a dedicated browser profile, enable Chrome remote debugging only while using the skill, and delete the saved session file when finished. <br>
Risk: Captured manifests, media URLs, and downloads may persist sensitive session-derived or user-generated content on disk. <br>
Mitigation: Choose the output directory carefully and remove capture manifests and downloaded files after review. <br>
Risk: The security evidence marks the release suspicious because session handling has weak scoping and plaintext persistence. <br>
Mitigation: Review the skill before installation and run it only in an environment where the logged-in Doubao session and generated media are acceptable to expose to the tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangm199/huangm-doubao-media) <br>
- [Doubao web application](https://www.doubao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON capture manifests, summary text, media URLs, and optional downloaded image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a logged-in browser session, Chrome remote debugging on port 18800 by default, and caller-selected output directories for captures and downloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
