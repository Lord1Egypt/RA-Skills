## Description:

Memory-Dream helps OpenClaw agents consolidate recent daily memory journals into long-term memory by extracting durable facts, correcting stale entries, deduplicating repeated knowledge, and producing a concise consolidation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to keep agent long-term memory current by periodically reviewing recent memory journals and applying conservative edits to MEMORY.md. It supports manual triggers, heartbeat-driven runs, and optional nightly cron operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private memory journals and consolidate sensitive or incorrect information into long-term memory.

Mitigation: Review proposed MEMORY.md additions for secrets, private data, prompt-like instructions, and unverified claims before accepting them.

Risk: Nightly cron operation may modify long-term memory without an approval step.

Mitigation: Prefer manual or preview-only runs until the deployment has an explicit review and approval workflow.

## Reference(s):

- [Memory-Dream ClawHub page](https://clawhub.ai/wavmson/skills/memory-dream)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with proposed file edits and optional cron setup command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read recent memory/*.md journals, update MEMORY.md, optionally mark old journals as consolidated, and append a run log.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
