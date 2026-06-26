## Description: <br>
Use LI.FI API guidance for cross-chain and same-chain swaps, bridges, contract calls, route quotes, token and chain validation, transaction preparation, and status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent request LI.FI quotes, prepare swap or bridge transactions, route ERC-20 approval flows through wallet tools, and check transfer status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help approve and submit real crypto swap or bridge transactions, which may move funds or grant token allowances. <br>
Mitigation: Before broadcasting or approving, verify chain, token, amount, recipient, slippage, approval amount, and explorer link, and prefer explicit user confirmation. <br>
Risk: Broad swap defaults, including slippage, can materially affect the received amount. <br>
Mitigation: Confirm the intended slippage and present estimated output, minimum output, fees, and slippage before execution. <br>


## Reference(s): <br>
- [LI.FI Documentation](https://docs.li.fi/) <br>
- [LI.FI LLM Documentation](https://docs.li.fi/llms.txt) <br>
- [LI.FI OpenAPI Specification](https://gist.githubusercontent.com/kenny-io/7fede47200a757195000bfbe14c5baee/raw/725cf9d4a6920d5b930925b0412d766aa53c701c/lifi-openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples, transaction guidance, and explorer links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIFI_API_KEY; quotes, approvals, and transaction requests depend on LI.FI API responses and wallet tools.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
