## Description:

Secrets-safe encrypted OpenClaw backups to S3/R2/B2/MinIO with lean modes, opt-in scheduling, verification, retention, and staged restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obuchowski](https://clawhub.ai/user/obuchowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to back up and restore OpenClaw state to S3-compatible storage, including AWS S3, Cloudflare R2, Backblaze B2, DigitalOcean Spaces, MinIO, and custom endpoints. It is intended for explicit OpenClaw backup or restore requests that need encrypted archives, cloud upload, verification, retention, and staged recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive OpenClaw backups may be published without encryption through an under-disclosed plaintext bypass.

Mitigation: Review before installing and block or avoid the --force-plaintext path; require encrypted backups with a configured passphrase file or secret reference.

Risk: Cloud credentials or passphrases stored in plaintext OpenClaw config can be copied into the backups they protect.

Mitigation: Use bucket-scoped credentials, store S3 keys in an AWS profile or operator-managed environment, keep passphrase files owner-only, and avoid plaintext OpenClaw config secrets.

Risk: Prune and retention behavior can delete local or remote backup objects.

Mitigation: Treat prune and retention as destructive operations and review dry-run delete plans before confirming them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/openclaw-cloud-backup)
- [Project homepage](https://github.com/obuchowski/openclaw-cloud-backup)
- [Credentials](references/credentials.md)
- [Security threat model and restore safety](references/security.md)
- [First-time setup flow](references/setup-flow.md)
- [AWS S3 provider guide](references/providers/aws-s3.md)
- [Cloudflare R2 provider guide](references/providers/cloudflare-r2.md)
- [Backblaze B2 provider guide](references/providers/backblaze-b2.md)
- [DigitalOcean Spaces provider guide](references/providers/digitalocean-spaces.md)
- [MinIO provider guide](references/providers/minio.md)
- [Other S3-compatible provider guide](references/providers/other.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit status, dry-run, backup, verify, prune, schedule, and restore command output; state-changing actions require explicit user confirmation.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
