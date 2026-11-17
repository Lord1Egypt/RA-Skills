## Description:

S3-compatible object storage that branches with your database, so each branch gets its own copy of the files and the rows that point at them. Use when a user wants object storage, a bucket, blob/file storage, or somewhere to put uploads, images, documents, avatars, or user-generated files for their app or agent — especially when they already use (or are setting up) Lakebase Postgres and don't want to add a separate storage provider like AWS S3, Cloudflare R2, or Supabase Storage. Triggers include "object storage", "bucket", "blob storage", "file storage", "store uploads/images/files", "S3-compatible storage", "presigned URL", "where do I put files", "storage logs", "bucket logs", "CDN in front of object storage", "Neon Object Storage", "Neon Storage", and "storage that branches with my database".

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building apps on Neon use this skill to provision branch-scoped object storage and implement file upload, download, and serving flows with S3-compatible tools.

### Deployment Geography for Use:

Regions: aws-us-east-1, aws-us-east-2, aws-eu-central-1, and aws-ap-southeast-1.

## Known Risks and Mitigations:

Risk: Applying a storage configuration can change bucket resources on the selected branch.

Mitigation: Inspect the configuration plan and confirm the target project and branch before deployment.

Risk: Credential files can expose storage access if committed to version control.

Mitigation: Keep credential files out of version control and use the branch-scoped environment variables as intended.

Risk: Objects in public-read buckets are accessible to anonymous readers.

Mitigation: Use public-read access only for files intended for everyone; keep other objects private or share them with presigned URLs.

## Reference(s):

- [Neon Object Storage overview](https://neon.com/docs/storage/overview.md)
- [Get started with Neon Object Storage](https://neon.com/docs/storage/get-started.md)
- [Buckets](https://neon.com/docs/storage/buckets.md)
- [Objects](https://neon.com/docs/storage/objects.md)
- [Authentication](https://neon.com/docs/storage/authentication.md)
- [S3 compatibility](https://neon.com/docs/storage/s3-compatibility.md)
- [Files SDK Neon adapter](https://files-sdk.dev)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript, JavaScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may include commands that provision or modify buckets; review configuration plans before applying changes.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
