## Description: <br>
Plans Huawei Cloud CCE container migrations by inventorying source clusters, mapping dependencies, designing migration batches, assessing risks, and generating rollback and validation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud migration engineers use this skill to assess Huawei Cloud CCE source clusters, inventory workloads and cloud dependencies, design migration batches, and produce risk, rollback, and validation plans before executing a migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawHub security scan reports that the package is presented as a read-only CCE migration planner but exposes broader administrative actions and credential-return paths than the stated purpose requires. <br>
Mitigation: Review the package before installation, use tightly scoped read-only Huawei Cloud credentials, and restrict use to the listed inventory and planning actions. <br>
Risk: Sensitive Huawei Cloud credentials, raw data, kubeconfig data, or output files could be exposed if unsafe dispatcher options are enabled. <br>
Mitigation: Avoid passing AK/SK values as command parameters and do not enable include_data, include_raw, output_file, kubeconfig export, or mutating actions unless they have been independently audited and constrained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-container-migration-planner) <br>
- [Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON-style migration planning sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces inventory summaries, dependency matrices, migration batches, risk lists, rollback plans, validation plans, and manual confirmation checklists.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
