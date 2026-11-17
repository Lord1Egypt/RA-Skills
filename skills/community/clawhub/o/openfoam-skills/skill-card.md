## Description:

Generate, review, debug, and recover OpenFOAM case files for CFD workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzj1214](https://clawhub.ai/user/fzj1214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, review, debug, and recover OpenFOAM CFD cases, including solver selection, boundary conditions, turbulence fields, numerics, validation, and cluster execution setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Slurm parallel-run template uses forced decomposition and can overwrite existing decomposition outputs.

Mitigation: Review the target case directory before execution, deliberately back up or remove stale processor directories, and confirm scheduler tasks match decomposeParDict.

Risk: Generated or repaired OpenFOAM dictionaries may contain incorrect case assumptions if the solver family, fields, boundary patches, or turbulence model are mismatched.

Mitigation: Review generated case files before running, keep 0/, constant/, and system/ files consistent, and run mesh and solver preflight checks such as checkMesh.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fzj1214/skills/openfoam-skills)
- [OpenFOAM Case Setup](references/case-setup.md)
- [OpenFOAM Solver Selection](references/solver-selection.md)
- [OpenFOAM Boundary Condition Playbook](references/boundary-condition-playbook.md)
- [OpenFOAM Turbulence Boundary Recipes](references/turbulence-bc-recipes.md)
- [OpenFOAM Turbulence And Numerics](references/turbulence-and-numerics.md)
- [OpenFOAM Case Recipes](references/case-recipes.md)
- [OpenFOAM Function Object Recipes](references/function-object-recipes.md)
- [OpenFOAM Validation, Parallel, And Observability](references/validation-parallel-and-observability.md)
- [OpenFOAM Cluster Execution Playbook](references/cluster-execution-playbook.md)
- [OpenFOAM Error Recovery](references/error-recovery.md)
- [OpenFOAM Mesh And blockMeshDict Manual](references/mesh-and-blockmeshdict-manual.md)
- [OpenFOAM Heat-Transfer And Compressible Cases](references/heat-transfer-and-compressible-cases.md)
- [OpenFOAM fvSolution And Residual Control](references/fvsolution-and-residual-control.md)
- [OpenFOAM Field And Dictionary Matrix](references/field-and-dictionary-matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with OpenFOAM dictionary snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should state solver and physics family, files touched, validation commands run or needed, stability risks, and recovery steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
