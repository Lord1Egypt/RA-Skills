## Description:

Maxwell 2D finite element simulation assistant for brushless motors, permanent-magnet synchronous motors, magnetic circuit setup, boundary conditions, parametric sweeps, solver analysis, and result extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor engineers use this skill to plan Maxwell 2D FEA workflows, configure materials, meshes, boundaries, excitations, solver settings, and review post-processing approaches for motor and magnetic-circuit simulations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python helpers may need dependencies that conflict with an existing Python environment.

Mitigation: Run the scripts in a virtual environment with pinned dependency versions.

Risk: The post-processing helper includes demo workflows and should not be assumed ready for production CSV result ingestion.

Mitigation: Verify or implement real CSV loading before using it on production simulation results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/maxwell-fea-simulation)
- [Material library](references/material_library.md)
- [Mesh guidelines](references/mesh_guidelines.md)
- [Simulation templates](references/simulation_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration templates, and Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local checklist text or post-processing plot files when the bundled Python scripts are run.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
