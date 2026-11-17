## Description:

Coordinates learning signals, pattern promotion, and stage management for self-improving memory by monitoring corrections and preferences, identifying emerging patterns, and integrating with Memory Sync Enhanced through an adapter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate learning workflows across correction, preference, and memory tiers. It helps inspect learning stages, identify repeated correction patterns, promote or demote patterns, and report learning statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coordinator can read or create local files through a caller-controlled learning_rules_file path.

Mitigation: Install only in trusted workspaces, pin learning_rules_file to the intended ~/self-improving/learning.md path, and review configuration before enabling the skill.

Risk: Automatic file creation may create or modify local learning-rule state unexpectedly.

Mitigation: Consider setting auto_create to false or requiring explicit approval before first-run file creation.

Risk: Some learning actions are reported as incomplete, placeholder, or non-durable behavior.

Mitigation: Do not use emerging-pattern or promotion results for production decisions until the implementation is reviewed and the behavior is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/learning-coordinator)
- [Publisher profile](https://clawhub.ai/user/whoisme007)
- [Artifact skill documentation](artifact/SKILL.md)
- [Enhanced configuration example](artifact/config/enhanced_config.yaml)
- [Enhanced usage example](artifact/examples/enhanced_usage.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples, shell commands, YAML configuration, and JSON-like status dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns learning statistics, pattern lists, health status, and promotion results through the coordinator and adapter APIs.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
