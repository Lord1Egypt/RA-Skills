## Description: <br>
Operates MaybeAI spreadsheets through the maybeai-sheet CLI for workbook upload, inspection, worksheet reads and writes, row append or upsert, formulas, lineage tracing, and SQL result sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[no7dw](https://clawhub.ai/user/no7dw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and spreadsheet operators use this skill to inspect and modify MaybeAI workbooks, synchronize tabular data, build formula or SQL-backed result sheets, and manage export or sharing workflows through the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad MaybeAI spreadsheet API access through the user's token. <br>
Mitigation: Review before installing and use only a MaybeAI token whose workbook access is acceptable for agent use. <br>
Risk: Raw API calls, public sharing, editor grants, file or worksheet deletion, range clearing, and exports can change access or data state. <br>
Mitigation: Require explicit user confirmation before these actions and verify the affected workbook, worksheet, range, and permission target. <br>
Risk: Workbook profiling may send sample spreadsheet rows to an LLM-backed service. <br>
Mitigation: Confirm profiling with the user before using it on sensitive workbooks; use direct worksheet lists, headers, and reads when exact data extraction is sufficient. <br>
Risk: Spreadsheet writes can affect the wrong worksheet when the worksheet name or gid is omitted or guessed. <br>
Mitigation: Start with the workbook manifest or worksheet list, choose an explicit worksheet name or gid, and read back the target range after every write. <br>
Risk: SQL or formula result sheets can produce incorrect reports or overwrite cells if compiled or anchored incorrectly. <br>
Mitigation: Read headers first, compile SQL before writing, confirm the output range or spill area, recalculate when needed, and verify the result sheet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/no7dw/skills/maybeai-sheet-cli) <br>
- [Project Homepage](https://github.com/OmniMCP-AI/maybeai-uni) <br>
- [CLI Command Reference](references/cli-commands.md) <br>
- [Read/Write Reference](references/read-write.md) <br>
- [File Management Reference](references/file-management.md) <br>
- [Permission And Sharing Reference](references/permission-sharing.md) <br>
- [Formulas and SQL Reference](references/formulas-sql.md) <br>
- [Formula Lineage Trace Reference](references/lineage-trace.md) <br>
- [Workbook Profile Reference](references/workbook-profile.md) <br>
- [Charts and Formatting Reference](references/charts-formatting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, SQL, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAYBEAI_API_TOKEN and the maybeai-sheet CLI; write operations should be verified with read-back commands.] <br>

## Skill Version(s): <br>
0.8.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
