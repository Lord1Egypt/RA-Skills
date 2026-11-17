## Description:

Pearl Calc is a paid calculator skill that evaluates math expressions through Pearl payments at $0.01 per expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misteeka](https://clawhub.ai/user/misteeka)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users can use Pearl Calc to evaluate math expressions when they accept the Pearl payment flow and the per-expression charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup delegates to an external Pearl skill and mutable instructions.

Mitigation: Review the Pearl skill, dependency installation, payment limits, and requested commands before approving setup.

Risk: Calculator expressions are sent to a paid remote service.

Mitigation: Avoid submitting sensitive formulas or private business data, and confirm the $0.01 per-expression charge before use.

## Reference(s):

- [Pearl](https://pearlcash.ai)
- [Pearl Calc on ClawHub](https://clawhub.ai/misteeka/skills/pearl-calc)
- [misteeka publisher profile](https://clawhub.ai/user/misteeka)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text calculator result with Markdown setup and usage commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Pearl setup, network access to pearlcash.ai, and user-approved paid execution.]

## Skill Version(s):

0.9.20 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
