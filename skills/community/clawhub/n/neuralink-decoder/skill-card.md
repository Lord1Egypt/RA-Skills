## Description:

Simulates and decodes neural spike activity into cursor movement for a synthetic brain-computer interface workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aadipapp](https://clawhub.ai/user/aadipapp)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run a local synthetic BCI simulation that generates neural spike counts, decodes them into 2D cursor velocity, and reports the resulting cursor trajectory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a synthetic simulation and not a real Neuralink or medical BCI integration.

Mitigation: Use the output for local educational or prototyping workflows only, and do not treat decoded values as medical, clinical, or device-control results.

Risk: The script depends on numpy in the local Python environment.

Mitigation: Install and run it in a normal local environment where that dependency is acceptable, and review local dependency policy before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aadipapp/skills/neuralink-decoder)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and console-style simulation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Python simulation that depends on numpy and produces synthetic spike, velocity, and cursor-position values.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
