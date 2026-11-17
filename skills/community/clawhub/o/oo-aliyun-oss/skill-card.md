## Description:

Use Alibaba Cloud OSS through an OOMOL-connected account to list, inspect, download, upload, delete, and create pre-signed object URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud storage operators use this skill to manage Alibaba Cloud OSS buckets and objects through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation fallback and hosted connector implementation were not verified.

Mitigation: Review and approve CLI installation separately, or use an already installed, verified CLI.

Risk: Pre-signed URLs can grant upload or deletion rights to an OSS object.

Mitigation: Require approval for the URL's target and expiry before creating or using a URL with write or delete permissions.

Risk: OSS operations run through the OOMOL connector using the connected account's credentials.

Mitigation: Use narrowly scoped OSS credentials and account for OOMOL's role in processing each operation.

## Reference(s):

- [Alibaba Cloud OSS API reference](https://www.alibabacloud.com/help/en/oss/developer-reference/api-reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Alibaba Cloud OSS release on ClawHub](https://clawhub.ai/oomol/skills/oo-aliyun-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides action-specific guidance; results depend on the connected OSS account and service response.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
