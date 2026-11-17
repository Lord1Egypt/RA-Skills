## Description:

Provides fitness and nutrition coaching guidance, meal planning, macro calculations, workout programming, and progress logging through reference materials and local scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekintkara](https://clawhub.ai/user/ekintkara)

### License/Terms of Use:


## Use Case:

External users use this skill for personal fitness and nutrition coaching, including macro-aware meal planning, workout programming, progressive overload tracking, and daily logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included log scripts may read or overwrite unintended JSON files if the date argument is not a real YYYY-MM-DD value.

Mitigation: Use only real YYYY-MM-DD dates and review or patch date validation before relying on the logging tools.

Risk: The skill stores fitness and nutrition logs locally under the user's home directory.

Mitigation: Install and run the scripts only when local storage of those logs is acceptable.

## Reference(s):

- [Common Food Calorie & Macro Reference](artifact/references/calorie-guide.md)
- [Exercise Database](artifact/references/exercise-database.md)
- [Personal Fitness Coach on ClawHub](https://clawhub.ai/ekintkara/skills/personal-fitness-coach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python command examples and JSON fitness logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local fitness logs under the user's home directory when its scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
