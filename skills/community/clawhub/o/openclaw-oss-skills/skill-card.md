## Description: <br>
Upload generated artifacts from an OpenClaw workspace to an Alibaba Cloud OSS bucket using credentials from environment variables, then return a temporary signed download link in the conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenghuanluck](https://clawhub.ai/user/zhenghuanluck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload generated files, directories, reports, media, archives, or build outputs from an OpenClaw workspace to Alibaba Cloud OSS and return a temporary signed download link to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local artifacts to Alibaba Cloud OSS and return signed links, including when invoked by sharing workflows. <br>
Mitigation: Confirm the exact files before upload and install the skill only when OSS artifact sharing is intended. <br>
Risk: Overbroad or long-lived OSS credentials can increase exposure if a workspace or signed link is mishandled. <br>
Mitigation: Use least-privilege or temporary OSS credentials and set an appropriate signed URL expiration. <br>
Risk: Uploaded artifacts may contain sensitive or regulated data. <br>
Mitigation: Avoid uploading sensitive or regulated data unless intentional, and clean up uploaded objects or temporary zip files when retention matters. <br>


## Reference(s): <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [ClawHub skill page](https://clawhub.ai/zhenghuanluck/openclaw-oss-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with signed URL, expiration time, and optional JSON output from the uploader] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud OSS credentials and can upload a file directly or zip multiple files or directories before upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
