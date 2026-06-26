## Description: <br>
Converts natural language queries into KWDB-specific SQL for time series data, relational data, and cross-model analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwdb](https://clawhub.ai/user/kwdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert natural language questions into KWDB SQL for IoT time-series, relational, and cross-model queries. It can guide schema discovery, SQL generation, validation, and optional KWDB execution when an MCP connection is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can be incorrect when table names, column names, or time ranges are assumed. <br>
Mitigation: Verify schema through MCP or user-provided table definitions, include assumptions in the output, and review the generated SQL before use. <br>
Risk: Optional live KWDB execution can expose data or change database state, especially for write or destructive statements. <br>
Mitigation: Require explicit execution approval, use a least-privilege database account, and avoid approving write or destructive SQL unless those changes are intended. <br>


## Reference(s): <br>
- [Query Scenarios](references/scenarios.md) <br>
- [KWDB MCP Server Integration](references/mcp-integration.md) <br>
- [Time Series DDL Reference](references/ts-ddl.md) <br>
- [Downsampling Query Reference](references/ts-downsampling.md) <br>
- [Interpolation Query Reference](references/ts-interpolation.md) <br>
- [Latest Value Query Reference](references/ts-latest-value.md) <br>
- [Window Events Reference](references/ts-window-events.md) <br>
- [Relational Query Reference](references/relational.md) <br>
- [Cross-Model Query Reference](references/cross-model.md) <br>
- [Time-Series Functions Reference](references/ts-functions.md) <br>
- [Relational Functions Reference](references/relational-functions.md) <br>
- [Output Template](assets/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and optional result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include intent, assumptions, field mappings, a validation checklist, and optional KWDB execution results.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
