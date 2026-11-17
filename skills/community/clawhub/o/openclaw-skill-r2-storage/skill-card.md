## Description:

Manage Cloudflare R2 object storage operations, including upload, download, listing, deletion, and presigned URL generation, through a boto3 S3-compatible CLI and Python module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage Cloudflare R2 buckets and objects from an agent workflow or command line. It supports common storage tasks such as moving files, listing object metadata, deleting objects, and creating temporary download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the package ships hard-coded Cloudflare R2 credentials and silently falls back to a specific account.

Mitigation: Do not use bundled credentials; require the publisher to revoke and remove them, and set your own least-privilege R2 credentials explicitly in the environment.

Risk: Delete operations can remove stored data.

Mitigation: Use credentials scoped to the minimum required buckets and review delete targets before execution.

Risk: Presigned URLs can expose stored objects for the configured lifetime.

Mitigation: Generate URLs only for intended objects, keep expirations short, and avoid sharing links beyond the intended audience.

## Reference(s):

- [Cloudflare R2 API Reference](references/r2-api.md)
- [Cloudflare R2 Docs](https://developers.cloudflare.com/r2/)
- [Cloudflare R2 S3 API Compatibility](https://developers.cloudflare.com/r2/api/s3/api/)
- [boto3 S3 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Cloudflare R2 API calls when invoked with credentials.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
