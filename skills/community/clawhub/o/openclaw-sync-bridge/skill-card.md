## Description:

Automatically syncs local and cloud OpenClaw configuration through a private GitHub Gist with token-based setup, previews, backups, and overwrite synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure GitHub Gist-backed synchronization for OpenClaw workspace files across machines. It supports setup, push, pull, diff, status, and backup workflows with interactive confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipe-to-shell install commands can execute remote code before review.

Mitigation: Download and inspect the artifact locally before running installation commands.

Risk: Synced OpenClaw profile and skill files are uploaded to GitHub Gist and may contain private data.

Mitigation: Review the configured sync list and exclude any directory or file that may contain secrets or sensitive content.

Risk: GitHub tokens are stored in local sync configuration.

Mitigation: Use a minimal token limited to Gist access, protect the local configuration file, and rotate the token if exposure is suspected.

Risk: Pull operations can overwrite local workspace files.

Mitigation: Use the diff and preview steps first, keep automatic backups enabled, and pull only from Gists you control and trust.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayshna/skills/openclaw-sync-bridge)
- [GitHub Token Settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples and interactive CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration, backup files, synced workspace files, and private GitHub Gist contents when the user runs the provided commands.]

## Skill Version(s):

2.0.0 (source: server release metadata and openclaw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
