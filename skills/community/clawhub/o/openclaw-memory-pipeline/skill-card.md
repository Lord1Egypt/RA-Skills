## Description:

Install, repair, and validate a persistent memory workflow for OpenClaw-style agents using Markdown memory files plus recurring cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maiusless](https://clawhub.ai/user/maiusless)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up, audit, or repair a workspace memory pipeline that captures curated notes, archives them by date, summarizes important daily context, and promotes durable information into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent recurring jobs can continue changing long-term memory after installation.

Mitigation: Confirm each job payload, schedule, timezone, workspace path, logging, and disable or removal process; prefer manual runs or visible logs until the workflow is trusted.

Risk: Persistent memory files may retain sensitive conversation details or information that should not be remembered.

Mitigation: Use the curated capture rules, avoid full transcript storage by default, and do not store sensitive conversations unless retention is acceptable to the user.

Risk: Daily and weekly summarization can promote incorrect, duplicate, or short-lived information into durable memory.

Mitigation: Verify file outcomes after test runs, keep summaries concise and factual, deduplicate entries, and promote only durable preferences, decisions, project context, and workflow rules.

## Reference(s):

- [Directory layout](artifact/references/directory-layout.md)
- [Memory rules](artifact/references/memory-rules.md)
- [Cron spec](artifact/references/cron-spec.md)
- [Verification](artifact/references/verification.md)
- [Migration and repair](artifact/references/migration-and-repair.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file paths, command suggestions, and optional Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or verify workspace memory files and recurring cron-job configuration when the user requests installation or repair.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
