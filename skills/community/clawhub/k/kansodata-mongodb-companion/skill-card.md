## Description: <br>
A MongoDB companion skill for read-only query planning, analysis, evidence interpretation, and fail-closed rejection of mutation or administrative requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to plan and interpret read-only MongoDB inspections, document queries, samples, aggregations, and summaries while preserving fail-closed boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a separate mongodb plugin and cannot technically enforce database permissions. <br>
Mitigation: Configure the mongodb plugin with read-only MongoDB permissions before use. <br>
Risk: Ambiguous requests, limited samples, or heterogeneous schemas can lead to unsupported conclusions. <br>
Mitigation: Use explicit filters and limits, label confidence, and degrade to a permitted read-only next step when evidence is insufficient. <br>
Risk: Mutation, administrative, or operational workaround requests are outside the skill's read-only scope. <br>
Mitigation: Reject write and administration tasks, including manual write scripts and change-validation procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kansodata/kansodata-mongodb-companion) <br>
- [Publisher profile](https://clawhub.ai/user/kansodata) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown with structured read-only analysis sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include resultado, evidencia_observada, limites, nivel_confianza, estado_madurez, and siguiente_paso_permitido.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
