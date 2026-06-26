## Description: <br>
Builds K3 blockchain automation workflows from natural language requests, including on-chain data retrieval, AI analysis, and delivery through email, Telegram, or Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexgrankinukr-hash](https://clawhub.ai/user/alexgrankinukr-hash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and blockchain operators use this skill to create, test, deploy, and verify K3 workflows for DeFi monitoring, wallet alerts, token tracking, protocol reporting, Telegram bots, and automated on-chain actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workflows can trade, transfer tokens, use exchange integrations, write smart contracts, or post to external services. <br>
Mitigation: Require explicit final approval before enabling those actions, including exact chain, contracts, wallet addresses, recipients, amounts, limits, trigger conditions, and a pause or disable path. <br>
Risk: Connected integrations may expose unnecessary account access or credentials. <br>
Mitigation: Use least-privilege integrations and avoid connecting services that are not required for the workflow. <br>
Risk: Incorrect API endpoints, subgraphs, contract addresses, or authentication settings can produce empty or misleading workflow data. <br>
Mitigation: Test the data source with a minimal workflow and inspect run output before deploying the full automation. <br>


## Reference(s): <br>
- [K3 Data Sources Discovery Guide](artifact/references/data-sources.md) <br>
- [K3 Node Types Reference](artifact/references/node-types.md) <br>
- [K3 Workflow Patterns](artifact/references/workflow-patterns.md) <br>
- [K3 Workflow Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with workflow prompts, configuration details, commands, and code snippets as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include deployed workflow configuration details, test results, and delivery-channel setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
