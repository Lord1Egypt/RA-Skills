## Description: <br>
Builds, reviews, debugs, and automates CalculiX finite-element workflows for input decks, Abaqus-style keywords, materials, steps, contacts, boundary conditions, analyses, solving, and post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzj1214](https://clawhub.ai/user/fzj1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, review, debug, and run CalculiX finite-element workflows, including input-deck structure, supported keyword choices, scheduler-backed execution, result files, and recovery from common solve or post-processing failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduler-backed CalculiX jobs can consume cluster resources or use site-specific settings incorrectly. <br>
Mitigation: Before using the Slurm template, review the job name, time limit, working directory, module-loading lines, task count, and expected storage impact. <br>
Risk: Input-deck guidance can produce incorrect analysis behavior if unsupported keywords, mismatched sets, incompatible loads, or missing supports are not reviewed. <br>
Mitigation: Validate the deck on a small run, check keyword support and set naming, confirm the active step matches loads and outputs, and inspect solver errors before scaling execution. <br>


## Reference(s): <br>
- [CalculiX Input-Deck Manual](references/input-deck-manual.md) <br>
- [CalculiX Keyword And Step Matrix](references/keyword-and-step-matrix.md) <br>
- [CalculiX Mesh, Boundary, And Output](references/mesh-boundary-and-output.md) <br>
- [CalculiX Cluster Execution Playbook](references/cluster-execution-playbook.md) <br>
- [CalculiX Error Recovery](references/error-recovery.md) <br>
- [CalculiX Error Pattern Dictionary](references/error-pattern-dictionary.md) <br>
- [CalculiX Step, Load, And Output Matrix](references/step-load-output-matrix.md) <br>
- [CalculiX Result Files And Post-Processing](references/result-files-and-postprocessing.md) <br>
- [CalculiX Thermal And Coupled Procedures](references/thermal-and-coupled-procedures.md) <br>
- [CalculiX Time Control And Amplitudes](references/time-control-and-amplitudes.md) <br>
- [CalculiX Element, Section, And Material Matrix](references/element-section-material-matrix.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fzj1214/hpc-calculix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and structured review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize analysis type, materials and sections, set and boundary assumptions, step sequence, expected result files, and cluster execution checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
