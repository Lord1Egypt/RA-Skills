## Description:

Upload files to MinIO object storage and generate shareable links with Markdown formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinute](https://clawhub.ai/user/sinute)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to upload selected local or downloaded files to a configured MinIO bucket and return shareable presigned links, with optional filenames, expiry settings, and Markdown or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected files to external MinIO object storage and return shareable presigned links.

Mitigation: Use tightly scoped MinIO credentials, confirm each upload or remote download before execution, and avoid uploading sensitive files unless explicitly approved.

Risk: The upload script exposes an insecure TLS bypass option.

Mitigation: Do not use the insecure option outside isolated testing; require valid TLS certificates for production MinIO endpoints.

Risk: The skill depends on the MinIO Python package at runtime.

Mitigation: Pin and review the minio dependency before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sinute/skills/minio-share)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain URL text by default, with documented Markdown and JSON output modes for share links and file metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces presigned download URLs and MinIO console preview URLs; link expiry defaults to 7 days and can be changed with an expiry argument.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
