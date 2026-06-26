## Description: <br>
Interact with the Noya AI platform for crypto trading, prediction markets, token analysis, DCA strategies, and structured crypto data (prices, TVL, funding rates, on-chain analytics, sentiment, news) via curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noyadev00-gmailcom](https://clawhub.ai/user/noyadev00-gmailcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Noya crypto market data, inspect portfolios, manage DCA strategies, and hand off trading or prediction-market tasks to the Noya agent. It is scoped to crypto, wallet-connected, and prediction-market workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access crypto account context and wallet-connected workflows through Noya. <br>
Mitigation: Install only when the user trusts Noya with financial context, use a short-lived API key, and revoke the key if exposure is suspected. <br>
Risk: Trading, transfers, DCA changes, and prediction-market actions can have financial consequences. <br>
Mitigation: Do not auto-confirm actions; require explicit user approval for every transaction or strategy change and review DCA strategies regularly. <br>
Risk: The security summary flags broad sharing of conversation and financial profile data with other agent contexts without clear minimization. <br>
Mitigation: Share only the minimum task-specific context and avoid sending unrelated conversation history or full portfolio summaries unless the user explicitly approves that exact sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noyadev00-gmailcom/noya-agent-skill) <br>
- [Noya homepage](https://agent.noya.ai) <br>
- [Noya docs index](https://mcp.noya.ai/llms.txt) <br>
- [Noya Agent API reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash/curl examples and parsed text or JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external Noya HTTPS APIs; conversational agent endpoints require NOYA_API_KEY, while public data endpoints do not.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
