## Description:

Calculates Medicare enrollment windows and estimates Part B and Part D late-enrollment penalties from a person's age, work, and coverage details, while flagging related Medigap, COBRA, employer-size, and HSA issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People approaching age 65, leaving active employer coverage, or helping a family member can use the navigator to review enrollment windows, estimate late penalties, and identify coverage-related deadlines. It is an educational planning aid; verify current figures and personal eligibility before acting.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Premium defaults change over time, and a general enrollment estimate may not reflect an individual's complete circumstances.

Mitigation: Verify current premiums and enrollment options at Medicare.gov and confirm individual decisions with Social Security or a qualified Medicare counselor.

## Reference(s):

- [Medicare Enrollment Windows](references/enrollment-windows.md)
- [Medicare.gov](https://www.medicare.gov/)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/medicare-enrollment-navigator)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text with dated enrollment windows, penalty estimates, warnings, and action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with supplied birth month, work and coverage details, and premium assumptions; includes a premium verification reminder.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
