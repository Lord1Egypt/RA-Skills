## Description: <br>
Monitor Polymarket prediction market wallets and detect new trades in real-time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to monitor Polymarket wallets for new orders, changed positions, and larger trades through the CLOB API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitoring script currently uses a hardcoded public wallet address rather than the wallet address shown in the usage command. <br>
Mitigation: Review scripts/monitor.sh before execution and update or confirm the wallet address to match the intended monitoring target. <br>
Risk: The shell helper makes external CLOB API requests and writes local log and state files. <br>
Mitigation: Run it only in an appropriate workspace, review the log paths, and ensure curl and jq behavior is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dagangtj/prediction-market-sentinel) <br>
- [Polymarket CLOB orders endpoint](https://clob.polymarket.com/orders?maker=$WALLET_ADDRESS&limit=1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Text] <br>
**Output Format:** [Markdown with inline bash commands and shell log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq, writes local log and state files, and reports newly observed order identifiers and details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
