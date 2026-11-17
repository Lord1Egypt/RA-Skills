## Description:

OpenClaw Security scans OpenClaw session content for sensitive personal data across ten regions and writes local NDJSON audit records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtoby8326](https://clawhub.ai/user/mtoby8326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit user input, prompts, conversation context, and knowledge base content for sensitive personal data while keeping a local audit trail for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs and .scan-cache.json may contain sensitive audit metadata and masked PII previews.

Mitigation: Treat audit output as sensitive local data, restrict access to the audit directory, and use retention cleanup.

Risk: File and directory deletion features can remove unintended data if pointed at broad or unrelated paths.

Mitigation: Use --delete-after-read only for scan-specific temporary files and run cleanup.py with --dry-run before deleting audit data.

Risk: Passing PII with --text can expose sensitive content through process metadata.

Mitigation: Use --file for automated or background scans and remove temporary input files after the scan.

## Reference(s):

- [Detection Patterns Reference](artifact/references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/mtoby8326/skills/openclaw-security-mtoby8326)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; CLI status text or JSON summaries; local NDJSON audit records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local audit records and .scan-cache.json; input is capped at 32,768 characters.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
