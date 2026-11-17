## Description:

Huawei Cloud OBS SDK helps agents provide practical guidance, Python examples, and command snippets for using Huawei Cloud OBS object storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idiosyncraticdragon](https://clawhub.ai/user/idiosyncraticdragon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need agent assistance for Huawei Cloud OBS setup, bucket management, object upload and download, presigned URLs, lifecycle rules, CORS, versioning, and encryption examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can expose or overwrite OBS data when copied directly into production workflows.

Mitigation: Review commands and code before use, apply least-privilege OBS credentials, and test against non-production buckets before handling sensitive data.

Risk: Delete, lifecycle, and public-access examples may cause irreversible data loss or unintended public exposure.

Mitigation: Add explicit confirmations and policy review for destructive operations, lifecycle changes, and any public ACL or CORS configuration.

Risk: The folder download sample may write outside the intended download directory when object keys are not normalized and validated.

Mitigation: Do not use the folder download pattern with untrusted buckets until normalized paths are checked to remain inside the selected destination directory.

Risk: Unpinned dependency ranges can change behavior over time.

Mitigation: Pin reviewed versions of huaweicloud-sdk-python-obs and python-dotenv for production environments.

## Reference(s):

- [Skill page](https://clawhub.ai/idiosyncraticdragon/skills/huawei-obs-skill)
- [Bucket Operations Guide](references/bucket_operations.md)
- [Object Operations Guide](references/object_operations.md)
- [Advanced Features Guide](references/advanced_features.md)
- [Publisher profile](https://clawhub.ai/user/idiosyncraticdragon)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Huawei Cloud OBS SDK examples that require user-supplied credentials, bucket names, object keys, regions, and local paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
