## Description:

Helps agents inspect and manage Cloudflare R2 buckets, objects, access settings, and event notifications through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use it to inspect R2 accounts and buckets, manage objects and bucket settings, and configure access or event notifications from an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Object transfers and signed access URLs can move data or grant access without clear approval.

Mitigation: Require explicit authorization for the target, permitted operation, recipient, and expiry; confirm transit-storage retention and deletion terms before handling sensitive objects.

Risk: The CLI installer and automatic skill synchronization can modify installed agent skills, and the remote installer and hosted connector implementation were not verified.

Mitigation: Review and verify the installer and synchronization behavior before installation, and use narrowly scoped R2 credentials.

## Reference(s):

- [Cloudflare R2 API documentation](https://developers.cloudflare.com/r2/api/s3/api/)
- [Cloudflare R2](https://www.cloudflare.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub listing](https://clawhub.ai/oomol/skills/oo-cloudflare-r2)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [JSON action payloads and connector results, with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Cloudflare R2 account and selected action.]

## Skill Version(s):

1.0.12 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
