## Description: <br>
Profiles wallet balances, PnL, labels, transactions, counterparties, related wallets, batch jobs, traces, and wallet comparisons through the Nansen CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to ask an agent to run Nansen wallet profiler commands for a specific wallet address, multiple wallets, transaction history, PnL, labels, counterparties, related wallets, traces, and comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants the agent access to the whole nansen CLI while using a Nansen API key. <br>
Mitigation: Use a scoped or low-risk API key where possible and supervise commands before execution, especially in environments where the CLI has trading, wallet-management, or other sensitive functions configured. <br>
Risk: Profiler commands can consume API quota or credits, and trace commands may make many API calls. <br>
Mitigation: Keep trace width and depth conservative, review batch sizes before execution, and monitor Nansen API quota or credit usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-wallet-profiler) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>
- [Required environment variable: NANSEN_API_KEY](artifact/SKILL.md) <br>
- [Required CLI package: nansen-cli](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Nansen CLI commands and command-output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY; command results depend on Nansen API access, limits, and available wallet data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
