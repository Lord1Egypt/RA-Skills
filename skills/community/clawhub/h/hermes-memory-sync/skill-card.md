## Description:

Extract daily conversation summaries from Hermes Agent session logs and persist them as readable memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up Hermes session-log memory persistence, backfill daily summaries, compare coverage gaps, and audit previous session history by topic or tool usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hermes session logs can contain secrets, personal data, customer data, or sensitive operational details.

Mitigation: Review the output before use, store generated memory in a private directory, and avoid committing or syncing generated memory files.

Risk: Broad backfills or scheduled runs can persist large amounts of historical conversation text without redaction or retention controls.

Mitigation: Start with a limited date range, review generated summaries, and enable cron only after confirming what the skill writes.

Risk: Copied Q&A and tool excerpts are historical content and may contain untrusted or outdated instructions.

Mitigation: Treat generated memory as reference material, not executable guidance, and review entries before relying on them.

## Reference(s):

- [Hermes Memory Sync ClawHub release](https://clawhub.ai/realpda/skills/hermes-memory-sync)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands and a Python script that writes daily Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Hermes JSON and JSONL session logs and writes plaintext summaries to workspace/memory/YYYY-MM-DD.md.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
