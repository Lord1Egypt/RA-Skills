## Description:

Manages agent memory by pruning old or low-relevance entries, compressing duplicates, and reporting storage costs with safe defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuge897](https://clawhub.ai/user/jiuge897)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect, prune, compress, and configure agent memory so older, duplicate, or low-relevance entries do not accumulate unchecked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared memory-pruner shell CLI is not included in the artifact, so executable behavior cannot be verified for a tool that may delete or rewrite agent memory.

Mitigation: Review the package before installing and ask the publisher to include the executable plus clear trigger and scope rules.

Risk: Automatic pruning can remove or rewrite useful agent memory if enabled without guardrails.

Mitigation: Use dry-run mode, explicit confirmation, backups, and a narrow memory directory before allowing pruning actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuge897/skills/memory-pruner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose deletion, compression, backup, and retention-policy actions for memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
