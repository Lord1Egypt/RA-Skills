## Description:

Scans OpenClaw session content for sensitive personal data across multiple regions and writes masked local audit records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtoby8326](https://clawhub.ai/user/mtoby8326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to audit OpenClaw user input, prompts, context, and knowledge-base content for PII before or during session workflows. It is suited for local privacy checks that need masked findings, content hashes, and retained audit events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local worker receives sensitive session, prompt, context, or knowledge-base text.

Mitigation: Use the documented file-based workflow with delete-after-read, avoid command-line text for background scans, and restrict access to temporary files.

Risk: Masked audit records and content hashes are written to disk.

Mitigation: Keep the audit directory access-restricted and run cleanup according to the configured retention period.

Risk: The security guidance warns not to rely on the audit log as a perfect compliance trail under heavy concurrent scans until the file-lock weakness is fixed.

Mitigation: Treat logs as local audit evidence with known concurrency limits and avoid high-concurrency compliance workflows until locking is remediated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtoby8326/skills/openclaw-security-pii-audit)
- [README](artifact/README.md)
- [Detection Patterns Reference](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON/NDJSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes masked local audit records; raw sensitive values are not stored according to the provided security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
