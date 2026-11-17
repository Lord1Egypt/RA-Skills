## Description:

Routes medication-channel messages through a deterministic local tracker for taken, missed, or extra dose events, timestamp-grounded confirmations, and avoiding reminder-related false logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to log Discord medication reports through a deterministic script path instead of relying on freeform model judgment. It is intended for timestamp-grounded medication history tracking, not clinical decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive medication history and Discord identifiers in a local plaintext CSV log.

Mitigation: Use the skill only in a workspace with appropriate file permissions, define retention and deletion practices before real use, and avoid storing the log in shared or synced locations unless that is intentional.

Risk: Unclear or unknown medication messages can be written into the medication log.

Mitigation: Add code-side rejection for unknown events before relying on the tracker, and ask for clarification rather than logging ambiguous messages.

Risk: CSV log contents may be opened in spreadsheet tools.

Mitigation: Sanitize CSV fields before spreadsheet use and review exported logs for formula-like values.

Risk: Installer behavior can change over time if installed without pinning.

Mitigation: Prefer a pinned installer version and verify artifact hashes against the release evidence before deployment.

## Reference(s):

- [Medication Channel Rules](references/CHANNEL_RULES.md)
- [Medication Channel Reference](references/README.md)
- [ClawHub Skill Page](https://clawhub.ai/cdmichaelb/skills/medication-channel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text confirmations, JSON rows, CSV files, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local CSV medication log and deduplicates entries by source Discord message ID.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
