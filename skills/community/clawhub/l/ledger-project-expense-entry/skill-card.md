## Description: <br>
Record natural-language project expense messages into ledger JSONL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People tracking project spending use this skill to turn short expense messages into local ledger entries. It parses project, description, amount, date, currency, direction, and tags, then appends the entry through the configured ledger script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short expense messages can be ambiguous, and the skill does not require a separate confirmation before appending a ledger entry. <br>
Mitigation: Review the parsed amount, currency, direction, tags, returned file path, and one-line summary after each entry so incorrect records can be corrected promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shing19/ledger-project-expense-entry) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and a short ledger-entry summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the month file path and a one-line summary after appending an entry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
