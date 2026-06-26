## Description: <br>
Build, review, and debug FEniCS or DOLFINx PDE scripts for finite-element workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzj1214](https://clawhub.ai/user/fzj1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to translate PDEs into FEniCS or DOLFINx implementations, choose finite-element spaces and solver settings, apply boundary conditions, prepare cluster runs, and debug common FEM runtime failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included Slurm template can run user-selected scripts on cluster resources. <br>
Mitigation: Before execution, review the script path, rank count, time limit, output location, and active cluster environment so the job uses only intended files and resources. <br>
Risk: Incorrect PDE formulation, boundary conditions, or solver choices can produce misleading simulation results. <br>
Mitigation: Review generated or repaired solver code against the PDE, weak form, boundary conditions, and expected output before relying on results. <br>


## Reference(s): <br>
- [FEniCS Runtime Selection](references/runtime-selection.md) <br>
- [DOLFINx Boundary Workflow](references/dolfinx-boundary-workflow.md) <br>
- [FEniCS UFL And Solver Patterns](references/ufl-and-solver-patterns.md) <br>
- [FEniCS PDE Template Cookbook](references/pde-template-cookbook.md) <br>
- [FEniCS Time-Dependent And Nonlinear Patterns](references/time-dependent-and-nonlinear-patterns.md) <br>
- [FEniCS Implementation Skeletons](references/implementation-skeletons.md) <br>
- [FEniCS And DOLFINx PETSc Solver Playbook](references/petsc-solver-playbook.md) <br>
- [Mixed Problems And Output](references/mixed-problems-and-output.md) <br>
- [FEniCS Cluster Execution Playbook](references/cluster-execution-playbook.md) <br>
- [FEniCS Boundary, IO, And Error Recovery](references/boundary-io-and-errors.md) <br>
- [DOLFINx Gmsh, MeshTags, And Refinement Manual](references/gmsh-meshtags-and-refinement.md) <br>
- [DOLFINx IO, Visualization, And Writer Manual](references/io-visualization-and-writers.md) <br>
- [DOLFINx Parallel And MPI Caveats](references/parallel-and-mpi-caveats.md) <br>
- [FEniCS Space, Boundary, And Output Matrix](references/space-boundary-output-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite reusable Python and Slurm templates from assets/templates for concrete solver or cluster-run scaffolds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
