## Description:

A Chinese-language power-electronics assistant for AC-DC, DC-AC, DC-DC, and AC-AC conversion analysis, local calculator checks, component-stress estimates, and Simulink setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanyinghao](https://clawhub.ai/user/shanyinghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select power-conversion topologies, calculate operating points and device stress, compare hand calculations with local Python calculator output, and prepare Simulink or Simscape simulation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may provide engineering estimates that are unsuitable as final design authority for real power-electronics hardware.

Mitigation: Independently validate calculations, simulations, component ratings, thermal margins, and safety requirements before applying results to hardware.

Risk: The skill requests broad read, write, and bash tool permissions for local reference lookup and calculator execution.

Mitigation: Review the requested actions before execution and keep script use limited to the local calculator workflows described by the artifact.

Risk: Simulation guidance can be mistaken for measured waveform data.

Mitigation: Treat Simulink sections as setup guidance and compare any generated waveforms against hand calculations, expected operating ranges, and measured or simulated results.

## Reference(s):

- [Four Conversions Overview](references/four-conversions.md)
- [Formula Reference](references/formulas.md)
- [Topology Selection](references/topologies.md)
- [Advanced Topics](references/advanced.md)
- [Worked Examples](references/examples.md)
- [Simulink and Simscape Templates](references/simulink-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown explanations with inline bash commands and JSON calculator results from local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculator outputs are engineering estimates and should be independently validated before real hardware use.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
