## Description:

Publishes a Markdown file to an S3-compatible bucket and returns a public share link rendered by a Docsify viewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbenben](https://clawhub.ai/user/rockbenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users who need to share Markdown publicly use the skill to publish a document through their S3-compatible bucket and receive a share link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence, but coverage is incomplete at 46.7%, including partial inspection of upload.js.

Mitigation: Review the shipped release before installation and start with bucket-scoped credentials in a dedicated bucket.

Risk: Publishing makes the Markdown publicly accessible; viewer setup replaces shared bucket-root files, and optional expiry changes the bucket lifecycle policy.

Mitigation: Screen documents for sensitive content and authorize setup or retention changes explicitly; use a dedicated bucket to limit impact.

Risk: Credentials can be stored in plaintext in ~/.md-web/config.json.

Mitigation: Use the environment variables for keys when practical, restrict local config permissions, and keep credentials out of shared output and version control.

Risk: The viewer renders Markdown as HTML, and inline HTML can add page elements.

Mitigation: Review unfamiliar markup before publishing and treat published pages as untrusted content.

## Reference(s):

- [Cloudflare R2 token permissions](https://developers.cloudflare.com/r2/api/tokens/#permissions)
- [Amazon S3 lifecycle configuration API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html)

## Skill Output:

**Output Type(s):** [Text, Public share URL, Configuration guidance]

**Output Format:** [Text response with a public URL and concise Markdown guidance when setup or errors require it.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes the supplied Markdown as a public document; viewer setup and optional retention changes are separate operations.]

## Skill Version(s):

1.3.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
