## Description: <br>
GrabGrab helps an agent download video or audio from user-provided URLs across supported media platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxizhen](https://clawhub.ai/user/xuxizhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to submit a media URL to GrabGrab, parse the service response, and download the returned video, audio, or selected media items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided media URLs are sent to GrabGrab for processing. <br>
Mitigation: Avoid private, internal, expiring, or token-bearing URLs unless the user intends to share them with the service. <br>
Risk: Returned downloads may be saved to a local path chosen during the workflow. <br>
Mitigation: Use a safe download directory and filename, and review or scan downloaded files before opening them. <br>
Risk: Proxy download URLs require short-lived signatures and may fail if reconstructed manually. <br>
Mitigation: Use only the signed proxyUrl field returned by the GrabGrab API response. <br>


## Reference(s): <br>
- [GrabGrab](https://www.grabgrab.fun) <br>
- [GrabGrab download API endpoint](https://www.grabgrab.fun/api/download) <br>
- [ClawHub skill page](https://clawhub.ai/xuxizhen/grabgrab) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Markdown status text with JSON response handling and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save returned video, audio, or photo files to the current working directory or a user-specified path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
