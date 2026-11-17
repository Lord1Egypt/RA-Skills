## Description:

Build, review, debug, and automate ElmerFEM workflows for Elmer `.sif` solver inputs, mesh directories, equation and material blocks, multiphysics coupling, boundary conditions, transient controls, and ElmerSolver execution or output issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzj1214](https://clawhub.ai/user/fzj1214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, review, repair, and run ElmerFEM simulation workflows centered on `.sif` files, mesh directories, solver blocks, boundary mappings, and cluster execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster submissions can consume scheduled compute resources and write solver logs in the run directory.

Mitigation: Review the Slurm template, run a small validation solve first, and confirm the run directory and output paths before submitting longer jobs.

Risk: Named SIF scaffold templates may be unavailable in the artifact.

Mitigation: Check available templates before relying on them and create missing SIF scaffolds from the documented workflow when needed.

Risk: Incorrect mesh, body, boundary, equation, or material ID mappings can produce failed or misleading ElmerFEM runs.

Mitigation: Map mesh, body, boundary, material, equation, and solver IDs explicitly before execution and review generated SIF changes before running ElmerSolver.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fzj1214/skills/hpc-elmerfem)
- [SIF Workflow Manual](references/sif-workflow-manual.md)
- [Block And Equation Matrix](references/block-and-equation-matrix.md)
- [Mesh, Boundary, And Output](references/mesh-boundary-and-output.md)
- [Cluster Execution Playbook](references/cluster-execution-playbook.md)
- [Error Recovery](references/error-recovery.md)
- [Solver Controls And Linear Systems](references/solver-controls-and-linear-systems.md)
- [Transient And Timestep Control](references/transient-and-timestep-control.md)
- [ElmerGrid And Mesh Conversion Manual](references/elmergrid-and-mesh-conversion.md)
- [Simulation, Body, And Solver Matrix](references/simulation-body-solver-matrix.md)
- [Physics And Output Matrix](references/physics-output-matrix.md)
- [Error Pattern Dictionary](references/error-pattern-dictionary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell command snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise ElmerFEM SIF scaffolds, solver settings, mesh and boundary mappings, result expectations, and Slurm launch templates for user review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
