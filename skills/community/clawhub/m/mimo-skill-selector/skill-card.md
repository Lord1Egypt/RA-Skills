## Description:

This Chinese-language skill recommends the top installed skills for a user's request, using keyword and semantic matching to provide ranked options with reasons and suitable scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they know the task they want to complete but need help choosing which already installed skill to load. It ranks up to three matching skills, explains why each fits, and asks a short clarification question when the request is too broad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad skill-selection phrases and inspect installed skill descriptions to make recommendations.

Mitigation: Use it only when skill-selection help is desired, and review the recommendation before choosing a skill to load.

## Reference(s):

- [Skill selector details](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-skill-selector)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Chinese Markdown recommendation list with ranked skill names, reasons, suitable scenarios, and clarification prompts when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are limited to installed skills and should be reviewed before loading the selected skill.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
