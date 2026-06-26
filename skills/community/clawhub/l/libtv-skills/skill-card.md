## Description: <br>
Uses LibTV's agent-im OpenAPI to create, edit, monitor, upload, and download AI-generated image and video work from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[316530790](https://clawhub.ai/user/316530790) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to send image or video creation and editing requests to LibTV, track session progress, upload reference media, and download generated results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and selected media to LibTV for third-party processing. <br>
Mitigation: Use it only for LibTV image or video work, and avoid uploading sensitive media unless third-party processing is acceptable. <br>
Risk: The skill requires a LIBTV_ACCESS_KEY and can use OPENAPI_IM_BASE or IM_BASE_URL to redirect requests. <br>
Mitigation: Use a LibTV key appropriate for this integration and do not set custom endpoint variables to untrusted hosts. <br>
Risk: Generated media is saved locally, using a default downloads directory when no output path is supplied. <br>
Mitigation: Specify an output directory when control over saved result locations is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/316530790/libtv-skills) <br>
- [Publisher profile](https://clawhub.ai/user/316530790) <br>
- [LibTV default API endpoint](https://im.liblib.tv) <br>
- [LibTV project canvas](https://www.liblib.tv/canvas?projectId=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, API calls, guidance] <br>
**Output Format:** [Markdown and JSON with shell command examples and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates LibTV sessions, uploads image or video inputs, polls for results, and downloads generated media to a local output directory.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
