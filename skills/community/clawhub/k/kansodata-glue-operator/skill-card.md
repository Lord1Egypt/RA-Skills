## Description: <br>
Gestiona cambios contractuales en AWS Glue workflows y triggers mediante diagnostico, planificacion, propuesta y verificacion sin ejecutar cambios reales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data platform engineers use this skill to review, plan, and document conceptual changes to AWS Glue workflows and triggers. It helps produce structured diagnostics, reversible plans, contractual change proposals, and evidence-based verification without using AWS credentials or executing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake contractual apply-change output for a completed AWS change. <br>
Mitigation: Treat outputs as planning artifacts and require separate authorized AWS execution plus verification evidence before claiming a change occurred. <br>
Risk: Requests may include credentials, secrets, jobs, crawlers, or live AWS execution that the skill is not designed to handle. <br>
Mitigation: Reject those requests fail-closed and reformulate work within workflows and triggers using non-secret evidence. <br>


## Reference(s): <br>
- [Skill scope](docs/scope.md) <br>
- [Operational examples](docs/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured Markdown with YAML-style response blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No runtime AWS execution; responses must report ok, degraded, or rejected status and include validation, rollback, evidence, and next-step fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
