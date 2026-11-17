## Description:

Magnetic Circuit Calculator helps agents estimate air-gap flux, flux-density distribution, permanent-magnet working points, and leakage coefficients for motor design using magnetic equivalent circuit methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor engineers use this skill for early-stage permanent-magnet motor magnetic-circuit estimates, parameter checks before Maxwell simulation, pole-slot comparison, leakage coefficient review, and design reasonableness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Magnetic-circuit estimates can be inaccurate for real motor design because the skill uses simplifying assumptions and the security evidence notes calculation reliability issues.

Mitigation: Treat outputs as preliminary screening results and verify numerical conclusions with Maxwell static-field simulation or independent engineering review before making design decisions.

Risk: The skill is a Chinese-language engineering tool, so users who are not comfortable with the language may misunderstand inputs, assumptions, or recommendations.

Mitigation: Have a qualified reader confirm parameter meanings, assumptions, and output interpretation before applying results.

## Reference(s):

- [Steel and permanent magnet materials reference](references/steel_pm_materials.md)
- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/magnetic-circuit-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with calculation summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are preliminary engineering estimates and may include recommendations for magnet thickness, material selection, and follow-up simulation.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
