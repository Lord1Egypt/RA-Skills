## Description: <br>
Secrets-safe encrypted OpenClaw backups to S3/R2/B2/MinIO with lean backup modes, opt-in scheduling, staged restore, retention, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obuchowski](https://clawhub.ai/user/obuchowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they explicitly need to back up or restore OpenClaw state to an S3-compatible storage provider such as AWS S3, Cloudflare R2, Backblaze B2, DigitalOcean Spaces, MinIO, or another compatible service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain sensitive OpenClaw state and credentials. <br>
Mitigation: Use encrypted backups, keep credentials out of openclaw.json, and store the GPG passphrase in a mode-600 file or secret store. <br>
Risk: Cloud storage credentials can read, write, and delete backup archives. <br>
Mitigation: Use a dedicated least-privilege bucket-scoped key where supported, rotate it regularly, and keep it out of chat and source control. <br>
Risk: Restore, prune, configuration, and scheduling actions can overwrite state or remove archives. <br>
Mitigation: Require explicit confirmation, review dry-run output before first backup, restore, or prune, and create schedules only after showing the exact command. <br>
Risk: A lost GPG passphrase makes encrypted backups unrecoverable. <br>
Mitigation: Store a copy of the passphrase in a password manager and retain older passphrases until all archives encrypted with them have aged out. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/openclaw-cloud-backup) <br>
- [Project homepage](https://github.com/obuchowski/openclaw-cloud-backup) <br>
- [Credentials guide](references/credentials.md) <br>
- [Security guide](references/security.md) <br>
- [First-time setup flow](references/setup-flow.md) <br>
- [AWS S3 provider guide](references/providers/aws-s3.md) <br>
- [Cloudflare R2 provider guide](references/providers/cloudflare-r2.md) <br>
- [Backblaze B2 provider guide](references/providers/backblaze-b2.md) <br>
- [DigitalOcean Spaces provider guide](references/providers/digitalocean-spaces.md) <br>
- [MinIO provider guide](references/providers/minio.md) <br>
- [Custom S3-compatible provider guide](references/providers/other.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, Files] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup, verification, restore, prune, status, setup, and schedule command guidance; state-changing actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
