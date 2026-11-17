## Description:

A friendly greeting skill that provides personalized and time-based greetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistant developers use this skill to generate personalized generic or time-aware greetings in a Clawd/OpenClaw assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic greeting triggers may activate the skill unintentionally.

Mitigation: Review trigger configuration and invoke the skill only when a greeting response is intended.

Risk: Installable Node/TypeScript dependencies can change over time.

Mitigation: Use pinned, reproducible installs and review dependency updates before deployment.

## Reference(s):

- [Greeting Skill README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/greeting-skill)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text greeting string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a name parameter; time-based greetings use the local current hour.]

## Skill Version(s):

1.0.0 (source: skill.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
