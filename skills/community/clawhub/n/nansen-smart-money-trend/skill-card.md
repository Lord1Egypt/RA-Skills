## Description: <br>
Helps an agent use the Nansen CLI to assess whether smart-money wallets have recently entered, continued accumulating, or started distributing a token on Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run Nansen smart-money research commands for token netflow, holder balance changes, flow intelligence, and DEX trade history. It supports market research workflows that compare short- and long-window smart-money activity to classify accumulation, fresh entry, reduction, or distribution signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Nansen API key for CLI queries. <br>
Mitigation: Use a dedicated or limited API key when available and avoid exposing the key in prompts, logs, or shared command output. <br>
Risk: A proposed nansen command could move beyond the intended read-only token analytics workflow. <br>
Mitigation: Review any command before execution and only run commands that are clearly Nansen research queries for the target token and chain. <br>
Risk: Smart-money flow signals can be misread as investment advice or treated as conclusive market direction. <br>
Mitigation: Treat outputs as research signals only and corroborate them with additional analysis before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-smart-money-trend) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>
- [Nansen CLI package](https://www.npmjs.com/package/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY; commands are intended for read-only token analytics queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
