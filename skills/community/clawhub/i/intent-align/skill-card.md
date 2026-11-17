## Description:

Intent-alignment orchestration for OpenClaw agent teams across diverse host environments. Use when work must stay anchored to user goals while allowing flexible execution: (1) coding with repos/PRs/issues, (2) multi-phase delivery with checkpoints, (3) multi-agent or multi-repo coordination, (4) evolving requirements needing structured re-alignment and user clarification loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers, engineering leads, and agent operators use this skill to keep multi-phase OpenClaw work aligned with user goals across repositories, pull requests, issues, trackers, and evolving requirements. It provides structured checkpoints for ambiguity handling, adapter selection, verification gates, and final alignment reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate multi-step work that creates planning artifacts, edits project files, runs verification commands, or updates external records when access is granted.

Mitigation: Use stricter confirmation settings for sensitive repositories or public-facing trackers, and review planned changes and verification output before applying high-impact updates.

## Reference(s):

- [Core Contract](references/core-contract.md)
- [Alignment Hub Schema](references/alignment-hub-template.md)
- [Realignment Protocol](references/realignment-protocol.md)
- [Verification Gates](references/verification-gates.md)
- [Capability Taxonomy](references/capability-taxonomy.md)
- [Adapter Template](references/adapters/adapter-template.md)
- [GitHub Adapter](references/adapters/github.md)
- [Local Repository Adapter](references/adapters/local-repo.md)
- [Tracker Generic Adapter](references/adapters/tracker-generic.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, structured YAML blocks, Mermaid diagrams, action plans, verification reports, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local planning artifacts, propose or edit project files, run verification commands, and update GitHub or tracker records when the agent has relevant access.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
