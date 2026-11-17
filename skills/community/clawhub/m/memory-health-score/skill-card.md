## Description:

Provides a 0-100 health score for an agent memory system across completeness, freshness, structure, density, and consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to evaluate memory-system hygiene, identify missing or stale memory artifacts, and generate concrete recommendations for improving memory quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring unattended runs may perform agent activity without active user review.

Mitigation: Run check-health.mjs manually or schedule only the audited checker until the recurring agent workflow has explicit approval and disable controls.

Risk: Automatic repair actions may change memory files or issue state without clear rollback controls.

Mitigation: Enable repair actions only after adding confirmation prompts, backups, and a documented rollback path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weidadong2359/skills/memory-health-score)
- [Publisher Profile](https://clawhub.ai/user/weidadong2359)
- [SKILL.md](SKILL.md)
- [Agent Amnesia Guide](agent-amnesia-guide.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON health score report with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled checker writes memory/health-score.json in the target workspace when run.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
