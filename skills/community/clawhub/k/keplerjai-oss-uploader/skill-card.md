## Description: <br>
Upload local files to Alibaba Cloud OSS and return an accessible URL under the configured bindHost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjicode](https://clawhub.ai/user/renjicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to upload selected local assets to Alibaba Cloud OSS and share the resulting public URL. It also supports configured object keys, dry runs, and optional lifecycle setup for expiring objects under the upload prefix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to a configured Alibaba OSS bucket. <br>
Mitigation: Install it only for agents that should upload to that bucket, and use least-privilege RAM credentials scoped to the intended bucket and operations. <br>
Risk: AccessKey credentials are required for upload and lifecycle operations. <br>
Mitigation: Inject credentials through environment variables or SecretRef and avoid placing secrets in skill text, chat transcripts, logs, or repository files. <br>
Risk: The optional lifecycle feature can expire objects under the configured upload prefix. <br>
Mitigation: Enable --sync-lifecycle or KEPLERJAI_OSS_SYNC_LIFECYCLE_ON_UPLOAD only when automatic deletion after the configured number of days is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renjicode/keplerjai-oss-uploader) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Skills config documentation](https://docs.openclaw.ai/tools/skills-config) <br>
- [Alibaba Cloud OSS lifecycle rules](https://help.aliyun.com/zh/oss/user-guide/overview-13) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and OSS URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns readable download links after successful uploads; dry-run mode prints the planned object key, content type, and public URL without uploading.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
