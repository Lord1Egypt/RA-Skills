## Description:

Harden Paperless cloud-folder intake with staging, provider gates, read checks, and safe retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[talonpoint](https://clawhub.ai/user/talonpoint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design, review, or repair Paperless intake workflows where files arrive through cloud-synced folders or other unreliable filesystem event paths. It helps agents recommend staging, provider classification, bounded read checks, deduplication, atomic delivery, retries, and Paperless-side ingestion verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-synced files can appear in folder listings before their bytes are locally readable, which can cause incomplete or failed Paperless intake.

Mitigation: Require bounded byte reads, staging outside Paperless consume, validation, deduplication, atomic delivery, and Paperless-native ingestion confirmation before treating a file as delivered.

Risk: Provider hydration and macOS privacy-gated automation can create an unnecessarily broad permission surface.

Mitigation: Classify the provider per path, limit automation to the intended source folder and Paperless consume path, and avoid granting broad privacy permissions to generic runtimes.

Risk: Leftover or unreadable files may be moved or deleted before their ingestion state is understood.

Mitigation: Keep leftovers pending until matched against Paperless records, successful task logs, checksums, or user confirmation, and require explicit approval before moving or deleting them.

## Reference(s):

- [Release Notes - 2.1.0](references/release-notes-2.1.0.md)
- [ClawHub Skill Page](https://clawhub.ai/talonpoint/skills/paperless-cloud-intake-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Safety-focused operational guidance; no executable code is shipped in the artifact.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
