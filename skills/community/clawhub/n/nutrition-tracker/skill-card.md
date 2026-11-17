## Description:

Track daily calories and macros in Obsidian, with profile initialization (sex/height/weight/goal) and goal-based target checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstract-sum](https://clawhub.ai/user/abstract-sum)

### License/Terms of Use:


## Use Case:

External users use this skill to initialize nutrition profiles, log meals, and check daily calorie and macro targets in an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input-handling flaws in the scripts could execute local code or write outside the intended Obsidian folder.

Mitigation: Review before installing, use only trusted inputs, validate language/date/numeric fields, quote heredocs, and ensure generated paths stay inside the intended vault.

Risk: Nutrition profile and meal data are stored persistently and may sync through the user's Obsidian setup.

Mitigation: Use a controlled vault and confirm the vault's sync and access settings before logging sensitive health-related data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstract-sum/skills/nutrition-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands that create or update Obsidian meal logs and a JSON nutrition profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports zh-CN and en-US localized script output.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
