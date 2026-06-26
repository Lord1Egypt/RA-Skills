## Description: <br>
This skill uploads local MP4 videos to VolcEngine ARK and analyzes their scripts or structure with a large model, with optional custom prompts for Douyin and general video analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnview](https://clawhub.ai/user/gnview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to upload an MP4 video, receive a file ID, and request structured video analysis such as timestamped actions, events, dialogue, scenes, or risk flags. It is useful when an agent needs to produce shell commands or guidance for extracting video script data through VolcEngine ARK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script uploads user-selected MP4 files to VolcEngine ARK for processing, which can expose private, confidential, regulated, or third-party video content. <br>
Mitigation: Use only videos that are appropriate to send to VolcEngine ARK, confirm permission for third-party content, and avoid personal, confidential, or regulated media unless approved. <br>
Risk: The workflow requires an ARK API key, and leaking that key could allow unauthorized API use. <br>
Mitigation: Protect the API key, prefer a limited-scope key where available, avoid committing credentials, and run the script only in a trusted Python environment. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/gnview/gnview-script-extraction) <br>
- [VolcEngine ARK file upload API endpoint](https://ark.cn-beijing.volces.com/api/v3/files) <br>
- [VolcEngine ARK responses API endpoint](https://ark.cn-beijing.volces.com/api/v3/responses) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload and analysis command guidance; successful analysis is expected to return formatted JSON from the underlying script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
