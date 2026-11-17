## Description:

Uploads an existing local file to OUS object storage using a provided OUS token, choosing single-file or multipart upload and returning the final CDN URL only after successful status confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatonionlee](https://clawhub.ai/user/fatonionlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload a user-selected local file to OUS object storage when they already have an ousToken, globalDomain, and blockSize. It is intended for controlled file-transfer workflows that need MD5 calculation, optional multipart upload, status polling, and a confirmed CDN URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A readable local file could be uploaded to a caller-supplied storage domain unintentionally.

Mitigation: Require an explicit user-selected local path, confirm the destination domain before upload, and stop when the path is missing, unreadable, or ambiguous.

Risk: Sensitive files such as credentials, keys, env files, or private configs could be exposed through an uploaded CDN URL.

Mitigation: Screen the chosen path for sensitive file types, ask for confirmation before uploading private material, and return url or uploadKey only after a confirmed successful status.

Risk: The ousToken is a secret and may fail or be misused if reused, logged, or sent to an unexpected domain.

Mitigation: Treat ousToken as confidential, avoid logging it, use only known OUS domains, and surface token errors clearly without continuing the upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fatonionlee/skills/ous-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown or text with upload status, troubleshooting details, and final JSON-like result fields when successful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns url and uploadKey only after status 5; may include taskId, obsTaskId, and md5 for troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
