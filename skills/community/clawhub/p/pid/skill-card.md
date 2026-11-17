## Description:

Pid is presented as a PID controller tuning and simulation tool, but the reviewed package behavior is a local record store for adding, listing, searching, removing, configuring, and exporting saved entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can invoke this skill's shell commands to maintain a small local JSONL datastore, inspect status and statistics, search records, configure simple key-value settings, and export data as JSON or CSV. It should not be used as a PID controller tuning or simulation authority without separate review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stated PID tuning purpose does not match the reviewed local record-store behavior.

Mitigation: Do not rely on this package for PID controller tuning or simulation unless a separate technical review confirms those capabilities.

Risk: The script writes records to PID_DIR or ~/.pid by default and includes a remove command that deletes saved records.

Mitigation: Run with an explicit sandboxed PID_DIR and back up records before remove or config operations.

Risk: CSV exports can contain values supplied through local entries.

Mitigation: Inspect or sanitize exported CSV before opening it in spreadsheet software, especially when entries came from untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/pid)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; script output is plain text, JSONL, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local data under PID_DIR or ~/.pid by default and can export pid-export.json or pid-export.csv in the working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
