## Description: <br>
Use https://tx.steer.fun to have a user execute a wallet action (send a transaction or sign a message) with their own wallet via a shareable URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephancill](https://clawhub.ai/user/stephancill) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate shareable tx.steer.fun URLs that let a user approve a JSON-RPC wallet request and return a transaction hash, signature, JSON result, or error. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wallet-action links can request signatures, transactions, contract calls, calldata, value transfer, or redirects that the user may not intend. <br>
Mitigation: Before approval, show the tx.steer.fun domain, chain, connected account, contract, value, calldata or message contents, requested method, and redirect destination in plain language. <br>
Risk: Overbroad or unnecessary wallet requests can expose users to avoidable approval risk. <br>
Mitigation: Use least-privilege requests and avoid permissions or methods that are not needed for the task. <br>


## Reference(s): <br>
- [Open Wallet on ClawHub](https://clawhub.ai/stephancill/open-wallet) <br>
- [tx.steer.fun wallet action service](https://tx.steer.fun/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with generated URLs and JSON-RPC parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redirect_url templates for returning wallet results to the agent.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
