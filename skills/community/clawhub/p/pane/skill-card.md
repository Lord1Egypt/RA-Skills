## Description: <br>
Access personal finance data (bank accounts, transactions, balances, spending, investments, crypto) via Pane's hosted MCP server using mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darnfish](https://clawhub.ai/user/darnfish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to configure Pane's hosted MCP server and query linked financial accounts for balances, transactions, spending summaries, recurring payments, investments, liabilities, crypto holdings, and annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive financial account, transaction, balance, investment, liability, crypto, and annotation data. <br>
Mitigation: Install only if the user trusts Pane and the mcporter dependency, rely on Pane privacy scopes, and avoid requesting or sharing unnecessary personal financial details. <br>
Risk: The Pane API key grants access to personal financial data through the hosted MCP server. <br>
Mitigation: Store PANE_API_KEY only in an environment variable and do not paste it directly into commands, files, or conversation content. <br>
Risk: Persistent annotations can save user-provided context server-side for future tool results. <br>
Mitigation: Do not store passwords, full account numbers, secrets, or unnecessary personal details in annotations, and periodically review or delete saved annotations. <br>


## Reference(s): <br>
- [Pane homepage](https://pane.money) <br>
- [Pane API key dashboard](https://pane.money/dashboard/connect) <br>
- [Pane MCP server endpoint](https://mcp.pane.money) <br>
- [ClawHub skill page](https://clawhub.ai/darnfish/pane) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-capable MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PANE_API_KEY, mcporter, and a Pane account with linked financial accounts; returned data may include sensitive personal financial information.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
