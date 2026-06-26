## Description: <br>
Checks Pionex spot account balances and available funds using the Pionex CLI with user-provided API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pibrandon](https://clawhub.ai/user/pibrandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Pionex balance and available-funds questions, including account overviews and currency-specific balance checks such as USDT. The skill is limited to read-only account balance queries and routes market data or trading actions to other skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Pionex API credentials to read account balances. <br>
Mitigation: Use credentials with the minimum permissions needed for balance queries and avoid enabling trading permissions unless a separate trusted workflow requires them. <br>
Risk: The skill depends on the third-party Pionex npm package and CLI. <br>
Mitigation: Install only if the publisher and package are trusted, and review the installed CLI before using it with account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pibrandon/pionex-portfolio) <br>
- [Publisher profile](https://clawhub.ai/user/pibrandon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON balance output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Pionex CLI and API credentials; account balance command output is JSON that may be filtered by currency.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
