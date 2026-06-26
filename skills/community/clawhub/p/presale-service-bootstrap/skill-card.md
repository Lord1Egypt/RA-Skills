## Description: <br>
Scaffold a new presale service foundation (docs/config/plans/readiness) before coding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DTsiomo](https://clawhub.ai/user/DTsiomo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and presale automation teams use this skill to create the documentation, configuration, planning, launch, and readiness foundation for a new presale service before implementation begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references an optional PowerShell scaffold helper that was not included in the reviewed package. <br>
Mitigation: Only run that helper if it is present in the installed skill pack and has been inspected first. <br>
Risk: Scaffolded plans and readiness documents can encode incomplete scope, acceptance criteria, or verification steps. <br>
Mitigation: Review the generated docs, configuration files, verification matrix, and readiness checklist before starting implementation. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/DTsiomo/presale-service-bootstrap) <br>
- [Workflow](references/workflow.md) <br>
- [Required artifacts](references/artifacts.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with file paths, checklist items, configuration file names, and optional shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scaffolding instructions and quality gates; users review generated project files before coding.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
