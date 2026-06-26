## Description: <br>
生成或编辑可灵 Omni-Video 视频，支持文生视频、图生视频、视频编辑和视频参考工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gayyzxyx](https://clawhub.ai/user/gayyzxyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to ask an agent to submit Kling Omni-Video generation or editing jobs, poll for completion, and report the downloaded MP4 file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image or video inputs are uploaded to a hosted API. <br>
Mitigation: Use only prompts and media approved for that service, and treat generated output and returned URLs as externally processed content. <br>
Risk: The skill requires a sensitive HSAI_API_KEY credential. <br>
Mitigation: Provide the key through environment variables or secret management, avoid exposing it in logs or shell history, and rotate it if disclosed. <br>
Risk: The script performs network requests and downloads a generated MP4 to a user-selected local path. <br>
Mitigation: Review command options and output paths before execution, and scan downloaded media according to local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gayyzxyx/kling-omni-video) <br>
- [Publisher profile](https://clawhub.ai/user/gayyzxyx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with inline bash commands, status text, and local MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HSAI_API_KEY, curl, and python3; generated videos are downloaded as MP4 files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
