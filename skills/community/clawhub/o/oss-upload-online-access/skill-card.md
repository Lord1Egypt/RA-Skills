## Description:

Upload files to Aliyun OSS or Tencent COS and return public access URLs. Use when the user wants to upload files, access files online, upload to OSS, get remote file links, or any phrase implying "upload for online/remote access".

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhean2021](https://clawhub.ai/user/liuhean2021)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users upload a local file or an HTTP/HTTPS file to Aliyun OSS or Tencent COS and receive a publicly accessible link. The skill checks the returned link before presenting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan raised concerns about upload visibility, credential handling, and activation scope. Inspection was incomplete, so the available evidence does not establish that the skill is safe.

Mitigation: Review the full upload script before installation; run it only for an explicitly requested upload, and upload only files intended for public access.

Risk: Cloud access credentials are required to upload files.

Mitigation: Keep credential values private, use least-privilege credentials, and do not expose them in conversations, logs, or screenshots.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liuhean2021/skills/oss-upload-online-access)

## Skill Output:

**Output Type(s):** [Text, URLs]

**Output Format:** [Plain text containing a public HTTPS URL or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The URL is returned only after an accessibility check.]

## Skill Version(s):

1.7.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
