## Description:

Uploads local files to Alibaba Cloud OSS and returns an accessible URL under the configured bindHost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjicode](https://clawhub.ai/user/renjicode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to upload selected local files to a configured Aliyun OSS bucket, return a public URL, and optionally apply lifecycle expiration for the upload prefix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected local files to the configured Aliyun OSS bucket.

Mitigation: Use a least-privilege AccessKey limited to the intended bucket and prefix, avoid sharing credentials in prompts or logs, and run dry-run before uploading.

Risk: Optional lifecycle synchronization can modify bucket lifecycle rules for the upload prefix.

Mitigation: Grant lifecycle permissions only when needed, review prefix, days, and rule ID with dry-run, and avoid enabling automatic lifecycle sync unless expiration is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renjicode/skills/keplerjai-oss-uploader)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Skills config documentation](https://docs.openclaw.ai/tools/skills-config)
- [Aliyun OSS lifecycle rules](https://help.aliyun.com/zh/oss/user-guide/overview-13)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown link plus shell command output lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns object_key and public_url when configured; dry-run prints the planned key, content type, and URL without uploading.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
