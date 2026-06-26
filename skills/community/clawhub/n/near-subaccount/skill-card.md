## Description: <br>
Create, list, delete, and manage NEAR subaccounts with bulk distribution operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NEAR account operators use this skill to create, list, delete, and fund NEAR subaccounts from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete NEAR accounts and send funds without an explicit confirmation step. <br>
Mitigation: Use only a low-value or test account, verify each account ID and amount before execution, and avoid automated delete or distribute workflows unless confirmation or dry-run controls are added. <br>
Risk: Shell commands are built from user-provided account IDs, file paths, and amounts. <br>
Mitigation: Inspect inputs manually and limit use to trusted recipient files and known NEAR account IDs until stronger input validation and safer command execution are added. <br>


## Reference(s): <br>
- [NEAR CLI documentation](https://docs.near.org/tools/near-cli) <br>
- [NEAR subaccount documentation](https://docs.near.org/concepts/account/subaccounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke NEAR CLI operations that create accounts, delete accounts, or send funds when run by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
