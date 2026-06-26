## Description: <br>
A Maxwell 2D finite element simulation assistant for motor and magnetic-circuit workflows, including solver setup, boundary conditions, parametric sweeps, result extraction, and post-processing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan Maxwell 2D FEA studies for BLDC/PMSM motors and magnetic circuits, configure geometry, materials, mesh, solver, and sweep settings, and generate checklists or post-process exported result arrays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The post-processing script can produce demo results while appearing to analyze user CSV data. <br>
Mitigation: Verify or modify the script to read declared input files before relying on its output, and clearly label whether results are demo data or simulation-derived results. <br>
Risk: Simulation guidance and reference parameters may be mistaken for validated engineering decisions. <br>
Mitigation: Treat the material tables, mesh settings, and solver templates as starting points; validate them against project requirements, mesh-convergence checks, and trusted Maxwell outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yongjie666888/maxwell-fea-simulation) <br>
- [Maxwell common material parameter library](references/material_library.md) <br>
- [Maxwell mesh setup guidelines](references/mesh_guidelines.md) <br>
- [Maxwell 2D simulation parameter templates](references/simulation_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional Python script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The post-processing script may write PNG plots in the current working directory when plotting is enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
