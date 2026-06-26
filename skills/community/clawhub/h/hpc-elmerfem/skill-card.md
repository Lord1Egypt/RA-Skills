## Description: <br>
Build, review, debug, and automate ElmerFEM workflows for `.sif` solver input files, mesh directories, equation and material blocks, multiphysics coupling, boundary conditions, transient controls, ElmerSolver execution, and output issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzj1214](https://clawhub.ai/user/fzj1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, review, debug, and run ElmerFEM workflows centered on `.sif` files, mesh directories, solver blocks, boundary mappings, transient controls, and cluster execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited ElmerFEM inputs may use incorrect `.sif` syntax, solver blocks, mesh paths, or body and boundary IDs. <br>
Mitigation: Review the `.sif`, mesh directory, ID mappings, solver settings, and output filenames before running ElmerSolver. <br>
Risk: Cluster submissions can waste allocation time or overwrite expected logs when Slurm resources, working directories, or output paths are wrong. <br>
Mitigation: Run a small validation solve first and check Slurm resource settings, working directory, and log destinations before production submission. <br>


## Reference(s): <br>
- [ElmerFEM SIF Workflow Manual](references/sif-workflow-manual.md) <br>
- [ElmerFEM Block And Equation Matrix](references/block-and-equation-matrix.md) <br>
- [ElmerFEM Mesh, Boundary, And Output](references/mesh-boundary-and-output.md) <br>
- [ElmerFEM Cluster Execution Playbook](references/cluster-execution-playbook.md) <br>
- [ElmerFEM Error Recovery](references/error-recovery.md) <br>
- [ElmerFEM Solver Controls And Linear Systems](references/solver-controls-and-linear-systems.md) <br>
- [ElmerFEM Transient And Timestep Control](references/transient-and-timestep-control.md) <br>
- [ElmerGrid And Mesh Conversion Manual](references/elmergrid-and-mesh-conversion.md) <br>
- [ElmerFEM Simulation, Body, And Solver Matrix](references/simulation-body-solver-matrix.md) <br>
- [ElmerFEM Physics And Output Matrix](references/physics-output-matrix.md) <br>
- [ElmerFEM Error Pattern Dictionary](references/error-pattern-dictionary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and structured workflow summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries typically cover physics family, mesh assumptions, solver and equation blocks, body and boundary mapping, and expected result files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
