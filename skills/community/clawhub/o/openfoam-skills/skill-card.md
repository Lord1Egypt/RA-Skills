## Description: <br>
Generate, review, debug, and recover OpenFOAM case files for CFD workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzj1214](https://clawhub.ai/user/fzj1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assemble, review, validate, debug, and recover OpenFOAM CFD cases, including solver selection, boundary conditions, turbulence setup, numerics, observability, and cluster execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the included Slurm scaffold can execute an OpenFOAM solver in the wrong case directory or with an unintended solver name. <br>
Mitigation: Confirm the case directory, solver argument, OpenFOAM environment, and scheduler task count before submission. <br>
Risk: The parallel run scaffold uses forceful decomposition, which can overwrite existing processor directories. <br>
Mitigation: Use scratch space or backups for production cases and confirm whether existing processor* directories may be replaced. <br>
Risk: Generated OpenFOAM dictionaries can still be physically or numerically invalid for a specific mesh, solver, or turbulence model. <br>
Mitigation: Run blockMesh or the relevant mesh generator, run checkMesh, verify patch and field consistency, and perform a short startup run before long production execution. <br>


## Reference(s): <br>
- [OpenFOAM Skill Page](https://clawhub.ai/fzj1214/openfoam-skills) <br>
- [OpenFOAM Case Setup](artifact/references/case-setup.md) <br>
- [OpenFOAM Solver Selection](artifact/references/solver-selection.md) <br>
- [OpenFOAM Boundary Condition Playbook](artifact/references/boundary-condition-playbook.md) <br>
- [OpenFOAM Turbulence Boundary Recipes](artifact/references/turbulence-bc-recipes.md) <br>
- [OpenFOAM Turbulence And Numerics](artifact/references/turbulence-and-numerics.md) <br>
- [OpenFOAM Case Recipes](artifact/references/case-recipes.md) <br>
- [OpenFOAM Function Object Recipes](artifact/references/function-object-recipes.md) <br>
- [OpenFOAM Validation, Parallel, And Observability](artifact/references/validation-parallel-and-observability.md) <br>
- [OpenFOAM Cluster Execution Playbook](artifact/references/cluster-execution-playbook.md) <br>
- [OpenFOAM Error Recovery](artifact/references/error-recovery.md) <br>
- [OpenFOAM Mesh And blockMeshDict Manual](artifact/references/mesh-and-blockmeshdict-manual.md) <br>
- [OpenFOAM Heat-Transfer And Compressible Cases](artifact/references/heat-transfer-and-compressible-cases.md) <br>
- [OpenFOAM fvSolution And Residual Control](artifact/references/fvsolution-and-residual-control.md) <br>
- [OpenFOAM Field And Dictionary Matrix](artifact/references/field-and-dictionary-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with OpenFOAM dictionary snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces case summaries covering solver family, files touched, validation steps, stability risks, and recovery guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
