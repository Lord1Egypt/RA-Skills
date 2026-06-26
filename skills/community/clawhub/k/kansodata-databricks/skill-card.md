## Description: <br>
Execute conservative read-only Databricks SQL through the Databricks plugin and provide safe planning output for unsupported workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to prepare or run conservative read-only Databricks SQL analysis against approved workspace, warehouse, catalog, schema, and table scopes. For unsupported Databricks workflows, it provides planning output only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized read-only queries can still expose sensitive Databricks data if the workspace, warehouse, catalog, schema, or table scope is too broad. <br>
Mitigation: Confirm the Databricks runtime tool is read-only and configured with the intended workspace, SQL warehouse, catalog, schema, and table allowlists before use. <br>
Risk: Unsupported requests such as Jobs API execution, Unity Catalog lineage API calls, or mutating SQL operations may be mistaken for executable actions. <br>
Mitigation: Treat unsupported workflows as planning guidance only and review any proposed SQL or operational steps before using separate Databricks tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kansodata/kansodata-databricks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with SQL snippets and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes assumptions, read-only SQL drafts, validation checklists, risk notes, and rollback signals.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
