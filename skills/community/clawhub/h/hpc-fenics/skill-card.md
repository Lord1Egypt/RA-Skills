## Description:

Build, review, and debug FEniCS or DOLFINx PDE scripts for finite-element workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzj1214](https://clawhub.ai/user/fzj1214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate PDEs into FEniCS or DOLFINx weak forms, choose finite-element spaces and boundary-condition patterns, configure solvers, and repair common FEM runtime failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster job templates can consume scheduled compute resources or write output in unsuitable locations if used unchanged.

Mitigation: Review and adapt SLURM paths, modules, ranks, thread counts, and output locations before running on a shared cluster.

Risk: Generated FEniCS or DOLFINx code may encode an under-constrained PDE, incompatible function space, or incorrect boundary condition.

Mitigation: Review the weak form, unknown space, boundary data, and solver settings against the mathematical problem before executing large cases.

## Reference(s):

- [FEniCS Runtime Selection](references/runtime-selection.md)
- [DOLFINx Boundary Workflow](references/dolfinx-boundary-workflow.md)
- [FEniCS UFL And Solver Patterns](references/ufl-and-solver-patterns.md)
- [FEniCS PDE Template Cookbook](references/pde-template-cookbook.md)
- [FEniCS Time-Dependent And Nonlinear Patterns](references/time-dependent-and-nonlinear-patterns.md)
- [FEniCS Implementation Skeletons](references/implementation-skeletons.md)
- [FEniCS And DOLFINx PETSc Solver Playbook](references/petsc-solver-playbook.md)
- [Mixed Problems And Output](references/mixed-problems-and-output.md)
- [FEniCS Cluster Execution Playbook](references/cluster-execution-playbook.md)
- [FEniCS Boundary, IO, And Error Recovery](references/boundary-io-and-errors.md)
- [DOLFINx Gmsh, MeshTags, And Refinement Manual](references/gmsh-meshtags-and-refinement.md)
- [DOLFINx IO, Visualization, And Writer Manual](references/io-visualization-and-writers.md)
- [DOLFINx Parallel And MPI Caveats](references/parallel-and-mpi-caveats.md)
- [FEniCS Space, Boundary, And Output Matrix](references/space-boundary-output-matrix.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PDE formulation notes, FEniCS or DOLFINx script scaffolds, PETSc solver options, SLURM launch snippets, and debugging guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
