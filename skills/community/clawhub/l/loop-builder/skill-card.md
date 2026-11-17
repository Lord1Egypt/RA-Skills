## Description:

Loop Builder helps agents design bounded Agent Loop workflows from low-information requests by identifying evidence gates, feedback signals, stopping rules, and human approval points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow designers use Loop Builder to turn rough automation requests into controllable prompts, checklists, human-in-the-loop flows, full Loop packages, specialized Agents, or reusable Skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow designs could be treated as approval to edit files, run commands, publish content, touch credentials, or create durable state.

Mitigation: Review generated workflows before approving them and require separate action-specific approval for risky or irreversible steps.

Risk: A loop may continue after feedback stops producing useful evidence or when required context is missing.

Mitigation: Use the skill's explicit evidence gates, derived iteration limits, early-stop rules, and circuit breakers before continuing.

Risk: Generated reusable agents or skills could accidentally capture project secrets, account data, private thresholds, or business records.

Mitigation: Keep sensitive and business-specific data outside reusable skill artifacts and review packages before deployment.

## Reference(s):

- [Loop Builder homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/engineering/loop-builder)
- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/loop-builder)
- [Loop Pattern Reference](references/loop-patterns.md)
- [Loop Checklists](references/checklists.md)
- [Scenario Defaults](references/scenarios.md)
- [Specialized Loop Agent Package](references/agent-package.md)
- [Specialized Skill Generation Contract](references/skill-generation-contract.md)
- [Loop Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow cards, reusable artifact templates, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are gated by context sufficiency, workflow confirmation, bounded iteration limits, stopping rules, and action-specific human approval for risky steps.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
