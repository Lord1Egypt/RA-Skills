## Description: <br>
Interact with the user's Ledgi personal finance data. Use when the user asks about their accounts, balances, net worth, holdings, investments, ISA allowances, pensions, snapshots, or wants to add/update financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelsongallardo](https://clawhub.ai/user/nelsongallardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to query Ledgi personal finance records, summarize accounts, holdings, net worth, ISA usage, and snapshots, and prepare account, holding, snapshot, or ISA deposit updates through the Ledgi CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change sensitive personal finance records. <br>
Mitigation: Use a limited-scope API key when available, and require the agent to summarize and obtain explicit approval before running any write command. <br>
Risk: The documented installation path runs a remote installer script. <br>
Mitigation: Review the installer source and install only from a trusted Ledgi source before using the skill. <br>


## Reference(s): <br>
- [Ledgi skill page](https://clawhub.ai/nelsongallardo/ledgi) <br>
- [Ledgi CLI command reference](artifact/commands.md) <br>
- [Ledgi bulk operation schemas](artifact/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary JSON files for bulk account or holding updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
