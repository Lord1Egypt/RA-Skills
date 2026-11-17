## Description:

Maintains a four-layer agent memory pipeline from write-ahead session logs to MEMORY.md, daily archives, and Obsidian sync, with Insight Miner analysis and backlink discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to maintain a persistent agent memory pipeline that records session state, extracts lessons, summarizes financial and task signals, and syncs selected archives into Obsidian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and summarizes sensitive personal and financial information across memory files and an Obsidian vault.

Mitigation: Require explicit approval for each data source and sync destination, keep sensitive summaries out of general agent memory where possible, and restrict vault access.

Risk: The workflow references external maintenance and sync scripts that are not bundled for review.

Mitigation: Inspect, pin, and approve each referenced script before enabling scheduled execution or Obsidian synchronization.

Risk: Automatic pruning and archive maintenance could remove useful memory entries or alter expected records.

Mitigation: Back up memory files and vault content before enabling pruning, and review retention rules before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adchina2025/skills/memory-system-2026)
- [Publisher profile](https://clawhub.ai/user/adchina2025)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file paths, schedules, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory maintenance instructions, archive structures, financial-summary fields, and sync workflow guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
