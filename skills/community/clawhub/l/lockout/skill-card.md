## Description:

Lockout is a shell-based local record manager for lockout/tagout-related entries, status checks, search, export, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for shell commands and guidance around a local CLI that records, searches, removes, exports, and reports on lockout/tagout-related notes. It should not be treated as an authoritative lockout/tagout safety control, compliance system, or source of truth for whether equipment is safely isolated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the local note utility for a lockout/tagout safety control or compliance source of truth.

Mitigation: Document and review it as an informal local record utility only; require separate authoritative safety procedures and records for operational decisions.

Risk: Records may be deleted, overwritten, or malformed without controls expected for safety-sensitive logs.

Mitigation: Do not store authoritative safety records in this skill unless scope limits, backups, deletion confirmation, and robust data encoding are added and reviewed.

## Reference(s):

- [Lockout ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/lockout)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe commands that read and write local files under LOCKOUT_DIR and export JSON or CSV records.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
