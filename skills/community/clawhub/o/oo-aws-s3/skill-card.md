## Description:

Manage AWS S3 buckets and objects through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list buckets and objects, inspect and download objects, and upload or delete objects through a connected AWS account. It can also generate pre-signed URLs for object access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pre-signed upload or delete links may be treated as safe reads, although they can change or remove S3 data.

Mitigation: Require approval after reviewing each link's target, method, recipient, and expiration.

Risk: First-time setup instructions can execute an installer without verification, and the remote implementation and installer are unaudited.

Mitigation: Install a reviewed, pinned CLI separately and inspect its automatic skill-sync settings.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Text]

**Output Format:** [CLI commands with JSON inputs and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific S3 results and metadata, subject to the connected AWS permissions.]

## Skill Version(s):

1.0.7 (source: frontmatter, server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
