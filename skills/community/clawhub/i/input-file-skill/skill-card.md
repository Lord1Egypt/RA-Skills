## Description: <br>
Generates CP2K input drafts for quantum chemistry calculations from local structure inputs, using documentation-driven references to apply conservative defaults and explain assumptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemon1044](https://clawhub.ai/user/lemon1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational chemists, and researchers use this skill to draft CP2K input files from natural-language requests and local .xyz structure files. It is intended to reduce setup effort while leaving scientific settings such as charge, spin, periodicity, basis choices, cutoffs, and convergence for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CP2K settings may be scientifically incomplete or unsuitable for production calculations. <br>
Mitigation: Review charge, spin, periodicity, basis and pseudopotential choices, cutoffs, and convergence before using generated inputs for production. <br>
Risk: The current workflow is limited to local structure inputs and may not handle external database retrieval or complex systems automatically. <br>
Mitigation: Use uploaded local structures and treat external databases as manual sources; ask for or record warnings when critical physical information is missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemon1044/input-file-skill) <br>
- [CP2K task map](references/cp2k-task-map.md) <br>
- [CP2K defaults](references/cp2k-defaults.md) <br>
- [CP2K kinds](references/cp2k-kinds.md) <br>
- [Ambiguity policy](references/ambiguity-policy.md) <br>
- [Job spec schema](references/job-spec-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, configuration, guidance] <br>
**Output Format:** [CP2K .inp draft plus Markdown explanation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-quality outputs generated from local user-provided structures; users should review scientific assumptions before production runs.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
