## Description: <br>
TypeScript library and CLI for Monarch Money budget management that can search transactions, update categories, list accounts and budgets, and manage authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davideasaf](https://clawhub.ai/user/davideasaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to authenticate to Monarch Money, inspect financial accounts and transactions, and automate transaction categorization or budget workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authenticate to Monarch Money with a password and MFA seed and read sensitive financial data. <br>
Mitigation: Use a dedicated environment, avoid passing secrets on the command line, and keep debug logging off. <br>
Risk: The skill can save reusable session tokens locally. <br>
Mitigation: Protect the local session file and clear ~/.mm/session.json when work is complete. <br>
Risk: Mutating commands can change financial records such as transactions, categories, accounts, or rules. <br>
Mitigation: Verify the exact transaction, category, account, or rule before running write operations. <br>


## Reference(s): <br>
- [Monarch Money API Reference](references/API.md) <br>
- [Troubleshooting Guide](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce CLI output in table or JSON form and requires Monarch Money credentials plus an MFA secret for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
