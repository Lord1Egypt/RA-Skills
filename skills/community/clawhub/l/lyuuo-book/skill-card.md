## Description: <br>
记账工具 helps an agent record personal income, expenses, transfers, accounts, categories, budgets, and financial reports through local SQLite-backed CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luo-jun-hub](https://clawhub.ai/user/luo-jun-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage personal bookkeeping records, including transaction capture, account and category management, budget status, and financial summaries. It is not intended for company financial analysis, stock analysis, software development, or database design tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, import, and export sensitive personal finance records. <br>
Mitigation: Require explicit user confirmation before destructive changes, imports, exports, or file-path based operations, and keep backups of the SQLite database. <br>
Risk: The setup instructions can install a global npm dependency. <br>
Mitigation: Prefer a local pinned dependency setup before use. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [ClawHub Release Page](https://clawhub.ai/luo-jun-hub/lyuuo-book) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on a local SQLite database and may import or export CSV or JSON finance records.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
