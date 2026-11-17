## Description:

Open Ended Goal Discovery helps an agent generate candidate goals from capabilities, user-interest signals, pursued goals, and preferences, then rank the top suggestions by value, novelty, feasibility, and alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add proactive goal discovery to long-horizon agents, idle-time workflows, or suggestion systems that answer what the agent could usefully do next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local usage and preference history.

Mitigation: Use it only where persistent local profiling is acceptable, keep the learner pointed at the skill's own directory, and periodically delete or reset learned_patterns.json when cross-session history is not desired.

Risk: The artifact describes automatic updates to its own SKILL.md after repeated feedback patterns.

Mitigation: Require human review before applying any instruction-file rewrite or learned optimization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/open-ended-goal-discovery)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented inputs or outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked Top-N goal suggestions and may maintain local preference history when the learner module is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
