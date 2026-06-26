## Description: <br>
M10 OneSource Blockchain Agent lets agents ask natural-language questions about blockchain data and receive structured analysis from historical indexes, live chain state, and smart contract bytecode analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnwollenberg](https://clawhub.ai/user/shawnwollenberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to submit paid natural-language blockchain questions and present concise summaries or Markdown analyses for on-chain activity, live chain state, and contract interface inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain questions and included wallet addresses are sent to OneSource for processing. <br>
Mitigation: Avoid sending private keys, seed phrases, sensitive identity details, or unnecessary addresses in prompts. <br>
Risk: Queries use a paid endpoint through HTTP 402 and x402 payment handling. <br>
Mitigation: Use client-side payment confirmation or spending limits before submitting requests. <br>
Risk: Response query traces may echo parts of the user's request or internal lookups. <br>
Mitigation: Omit query traces from user-facing output unless they are needed for review or debugging. <br>


## Reference(s): <br>
- [OneSource](https://onesource.io) <br>
- [M10 OneSource Blockchain Agent on ClawHub](https://clawhub.ai/shawnwollenberg/m10-blockchain-agent) <br>
- [x402 protocol](https://github.com/coinbase/x402) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Plain text summaries and Markdown analysis returned from a JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include query traces, step status, token usage, estimated cost, and payment-related HTTP errors.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
