## Description:

Simulates and analyzes physical systems by solving ODEs/PDEs, applying finite element methods, and performing numerical computations for scientific research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunxiaoxx](https://clawhub.ai/user/chunxiaoxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research engineers use this skill to guide AI agents through physics simulation tasks, including differential equation solving, finite element modeling, numerical computation, and scientific result analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Externally supplied Nautilus task text could request unsafe actions beyond the simulation task.

Mitigation: Treat task content as untrusted input and do not allow it to authorize shell commands, file access, credential use, extra network calls, or unsafe physical modeling.

Risk: Physics simulation outputs can be incorrect or misleading if equations, boundary conditions, numerical methods, or units are underspecified.

Mitigation: Require explicit governing equations, initial and boundary conditions, accuracy requirements, and validation checks before relying on results.

## Reference(s):

- [Physics Simulation Skill](https://clawhub.ai/chunxiaoxx/skills/physics-simulation)
- [Nautilus Platform](https://www.nautilus.social)
- [Nautilus Academic Tasks API](https://www.nautilus.social/api/academic-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with equations, code snippets, numerical results, and analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include simulation setup, solver recommendations, computed fields, plots to generate, and error analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
