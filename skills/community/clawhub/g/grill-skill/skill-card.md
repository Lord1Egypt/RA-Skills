## Description:

Interviews skill authors to design eval tasks, then uses Caliper results to test and improve their skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edonadei](https://clawhub.ai/user/edonadei)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors and developers use this skill to design evaluation tasks, run Caliper tests, and identify changes that improve skill reliability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and edit selected skill files and write evaluation specifications.

Mitigation: Use it in a trusted project and review generated evaluation YAML before confirming writes.

Risk: Caliper tests may execute task setup or cleanup commands and load local agent customizations.

Mitigation: Review test commands and use isolated Caliper mode for portable or shared results.

## Reference(s):

- [Grill Skill on ClawHub](https://clawhub.ai/edonadei/skills/grill-skill)
- [Grill Skill Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown guidance and YAML evaluation specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes test results and comparisons when Caliper is run.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
