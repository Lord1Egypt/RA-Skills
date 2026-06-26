## Description: <br>
Double-entry, full-cycle accounting suite built for AI agents that converts bank CSV, OFX, and QBO files into balanced local SQLite books and accounting reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[737999](https://clawhub.ai/user/737999) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
External users, developers, agents, and accounting practitioners use this skill to create local client books, import bank or AJE files, categorize transactions, manage accounting rules, and produce auditable financial statements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can import, delete, close, and modify financial records in local books.db files. <br>
Mitigation: Install only for a dedicated GRIDTRX_WORKSPACE, keep current backups, and require explicit approval before imports, deletes, rule changes, lock or ceiling changes, report layout edits, exports, or year-end rollover. <br>
Risk: Accounting data may contain sensitive financial information. <br>
Mitigation: Keep books.db and exported reports in approved local storage and do not share them by email or other insecure channels unless the user explicitly approves. <br>
Risk: Incorrect categorization or period changes can produce misleading books and reports. <br>
Mitigation: Confirm ambiguous transaction categories with the user, review suspense items, respect lock dates and fiscal-year ceilings, and verify the trial balance after write operations. <br>


## Reference(s): <br>
- [GridTRX on ClawHub](https://clawhub.ai/737999/gridtrx) <br>
- [GridTRX homepage](https://github.com/gridtrx/gridtrx) <br>
- [GridTRX demo](https://youtu.be/9mmHbgEB3PQ) <br>
- [CLI reference](CLI_README.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, plain-text CLI output, structured MCP JSON responses, and CSV or PDF report exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local books.db files inside GRIDTRX_WORKSPACE and may create or modify accounting records, import rules, lock dates, fiscal-year ceilings, and exported reports.] <br>

## Skill Version(s): <br>
0.1.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
