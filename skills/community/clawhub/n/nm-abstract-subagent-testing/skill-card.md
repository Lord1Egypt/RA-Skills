## Description:

Test skills via TDD in fresh subagents

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to evaluate whether a skill changes agent behavior by comparing baseline and with-skill results, then testing guardrails in fresh subagent instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test comparisons may be misleading if baseline and with-skill runs use different prompts or instance conditions.

Mitigation: Use identical prompts in fresh instances, record the test setup, and repeat runs to check reproducibility.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-abstract-subagent-testing)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown with test prompts, response records, and scoring templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
