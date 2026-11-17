## Description:

Private file storage for AI agents. Mount S3 as a filesystem via WebDAV. Use standard unix commands (ls, cat, grep, cp, rm). All persistent data in S3, small temporary read cache locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishek203](https://clawhub.ai/user/abhishek203)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use pidrive to mount private S3-backed storage through WebDAV so agents can read, write, search, share, and recover files with standard Unix commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI and an external S3-backed service for persistent storage.

Mitigation: Install only if the publisher is trusted, verify CLI release provenance before use, and use separate approval for secrets, regulated data, or sensitive workloads.

Risk: Public link shares can expose files to anyone with the URL.

Mitigation: Prefer private direct shares for sensitive data and reserve public links for content intentionally meant to be downloadable without authentication.

Risk: Normal shell commands can persist local files remotely and make them searchable through the service.

Mitigation: Use the mounted drive only for data intended to be stored, indexed, shared, and recovered through the external service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abhishek203/skills/pidrive)
- [pidrive Source Code](https://github.com/abhishek203/pi-drive)
- [pidrive GitHub Releases](https://github.com/abhishek203/pi-drive/releases)
- [pidrive Homebrew Tap](https://github.com/abhishek203/homebrew-pidrive)
- [pidrive Service](https://pidrive.ressl.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers CLI installation, registration, mounting, sharing, search, trash recovery, account commands, and storage behavior.]

## Skill Version(s):

1.9.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
