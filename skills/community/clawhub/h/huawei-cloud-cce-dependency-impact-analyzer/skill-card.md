## Description: <br>
Analyzes Huawei Cloud CCE Kubernetes service topology to trace Service, Ingress, Pod, and Node propagation paths and upstream and downstream blast radius. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SREs operating Huawei Cloud CCE clusters use this skill to map service dependencies, estimate incident blast radius, and generate evidence-backed impact reports for handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive Huawei Cloud and Kubernetes cluster data when given credentials. <br>
Mitigation: Use tightly scoped read-only credentials and avoid exposing broad production credentials. <br>
Risk: The server security review reports that bundled actions can perform live cloud or Kubernetes changes despite the read-only skill description. <br>
Mitigation: Review available actions before installation and do not enable confirm=true actions unless live infrastructure changes are intended. <br>
Risk: Report output paths could be misused to write files in unintended locations. <br>
Mitigation: Use explicit, controlled report paths and review generated files before relying on them. <br>


## Reference(s): <br>
- [Workflow pipeline and scoring rules](references/workflow.md) <br>
- [Output structure specification](references/output-schema.md) <br>
- [Read-only boundaries and handoff rules](references/risk-rules.md) <br>
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) <br>
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results and Markdown impact reports with evidence tables and topology details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save an optional report file when requested; requires scoped Huawei Cloud credentials and CCE cluster identifiers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence; artifact _meta.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
