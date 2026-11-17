## Description:

Preserves user-critical instructions across long sessions and context compaction by capturing anchors, rehydrating them during planning, and checking for drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to preserve explicit user constraints during long-running or compacted sessions. It helps an agent track high-priority instructions, resolve conflicts, and surface drift checks before final responses or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user-derived constraints into workspace memory files, which may retain sensitive, outdated, or overly broad instructions.

Mitigation: Use explicit opt-in for anchor creation, redact secrets and unnecessary personal data, inspect or clear the ledger regularly, and keep ledgers only in trusted workspaces.

Risk: Reloaded anchors may influence later planning without enough validation or user control.

Mitigation: Review active anchors before long or sensitive tasks, pause or delete stale anchors, and require fresh confirmation before destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/instruction-anchor-guard)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown anchor ledger entries, compact status blocks, and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to persist selected instruction anchors in workspace memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter mentions 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
