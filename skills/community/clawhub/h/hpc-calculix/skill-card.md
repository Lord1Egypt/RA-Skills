## Description:

Build, review, debug, and automate CalculiX finite-element workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzj1214](https://clawhub.ai/user/fzj1214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, review, debug, and run CalculiX finite-element input-deck workflows, including materials, sections, steps, boundary conditions, solver failures, cluster execution, and post-processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CalculiX input decks or SLURM scripts may consume cluster time or overwrite result artifacts if submitted without review.

Mitigation: Review generated .inp decks and SLURM scripts before submission, confirm writable output locations, and preserve previous result sets when iterating.

Risk: Incorrect keyword, set, step, load, or output choices can produce failed solves or misleading finite-element results.

Mitigation: Validate decks with small parsing or representative runs first, then check materials, sections, sets, boundary conditions, step compatibility, and requested outputs against the included references.

## Reference(s):

- [CalculiX Input-Deck Manual](references/input-deck-manual.md)
- [CalculiX Keyword And Step Matrix](references/keyword-and-step-matrix.md)
- [CalculiX Mesh, Boundary, And Output](references/mesh-boundary-and-output.md)
- [CalculiX Cluster Execution Playbook](references/cluster-execution-playbook.md)
- [CalculiX Error Recovery](references/error-recovery.md)
- [CalculiX Error Pattern Dictionary](references/error-pattern-dictionary.md)
- [CalculiX Element, Section, And Material Matrix](references/element-section-material-matrix.md)
- [CalculiX Step, Load, And Output Matrix](references/step-load-output-matrix.md)
- [CalculiX Thermal And Coupled Procedures](references/thermal-and-coupled-procedures.md)
- [CalculiX Time Control And Amplitudes](references/time-control-and-amplitudes.md)
- [CalculiX Result Files And Post-Processing](references/result-files-and-postprocessing.md)
- [CalculiX SLURM Template](assets/templates/calculix-ccx-slurm.sh)
- [ClawHub Skill Page](https://clawhub.ai/fzj1214/skills/hpc-calculix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CalculiX .inp deck structure, SLURM submission scripts, solver diagnostics, and post-processing guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
