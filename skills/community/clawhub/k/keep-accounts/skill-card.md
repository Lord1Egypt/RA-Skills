## Description: <br>
Tracks household income, expenses, transfers, balances, and monthly summaries in a local SQLite ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silent404](https://clawhub.ai/user/silent404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household finance maintainers use this skill to record transactions, inspect account balances, generate monthly summaries, and manage transfers across predefined household accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently store and display sensitive household financial records in a local SQLite database. <br>
Mitigation: Confirm the database location, access controls, and correction or deletion process before relying on the ledger. <br>
Risk: Broad natural-language triggers could cause income, expense, transfer, or ledger initialization actions when the user's intent is ambiguous. <br>
Mitigation: Require explicit confirmation before executing commands that add transactions, transfer funds between ledger accounts, or initialize a database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silent404/keep-accounts) <br>
- [Family finance database reference](artifact/references/finance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and local SQLite query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from or write to a local SQLite finance database when the generated shell commands are executed.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
