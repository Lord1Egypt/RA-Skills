## Description:

Automatically consolidates agent memory files after sessions by using an LLM to prune stale context, resolve contradictions, tighten remaining memory, and support persistent DM channels through session-gap detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchelldavis44](https://clawhub.ai/user/mitchelldavis44)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep persistent memory files concise and current by automatically consolidating stale, contradictory, or vague memory entries after enough sessions and time have passed. It also supports optional in-session capture of corrections, preferences, decisions, and other memory-worthy signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process memory files, recent conversation content, and transcript excerpts with an LLM.

Mitigation: Use it only in workspaces where that data access is acceptable, configure memoryFiles conservatively, and disable capture when recent conversation content should not be processed.

Risk: The skill automatically writes updates to persistent memory files.

Mitigation: Keep memory files under version control or backed up, and review memory changes before relying on them.

Risk: The security evidence reports under-disclosed data access and weak boundaries.

Mitigation: Review the skill carefully before installing and avoid workspaces containing sensitive conversations or credentials until path validation, disclosure, redaction, and review controls are improved.

## Reference(s):

- [Memory Dream README](artifact/README.md)
- [Memory Dream ClawHub page](https://clawhub.ai/mitchelldavis44/skills/openclaw-memory-dream)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, JSON]

**Output Format:** [Markdown memory-file updates and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Background consolidation and optional capture run according to configured session and time thresholds.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
