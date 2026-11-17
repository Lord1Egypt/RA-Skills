## Description:

Continuous learning system that records failures, corrections, patterns, version rules, approach preferences, and behavioral corrections for fast recall through a dedicated MeiliSearch index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enjuguna](https://clawhub.ai/user/enjuguna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record failures, corrections, preferences, version rules, and recurring patterns, then search those notes before acting so prior fixes can inform future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory and credential handling can expose sensitive operational notes or MeiliSearch access if the environment is not trusted.

Mitigation: Install only in trusted workspaces, keep MeiliSearch localhost-only where possible, use a scoped key, and avoid storing secrets or personal data in learnings.

Risk: Automatically extracted learnings can encode incorrect or outdated guidance.

Mitigation: Review extracted entries before using --apply and treat retrieved learnings as advisory context that cannot override current user, system, or safety requirements.

## Reference(s):

- [ClawHub Learnings Skill](https://clawhub.ai/enjuguna/skills/learnings)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default for auto-extract and distillation; --apply writes to the learning index or LEARNINGS.md.]

## Skill Version(s):

1.3.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
