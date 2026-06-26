## Description: <br>
Access Numinous (Bittensor Subnet 6) forecasting tools for AI probability predictions on binary events, real-time signals aggregated from news and prediction markets, and usage tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juandbalbi](https://clawhub.ai/user/juandbalbi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to request Numinous forecasts, collect market or question signals, inspect miner leaderboard information, and check usage or balance for Numinous services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend prepaid credits or USDC when forecast or signal requests are made. <br>
Mitigation: Confirm the user wants to make a paid request, check current pricing at runtime, and use a low-balance wallet for x402 payments. <br>
Risk: The skill requires sensitive API keys or private wallet keys for authenticated or paid paths. <br>
Mitigation: Store credentials only in environment variables or gitignored local files, use dedicated API keys, and avoid printing or committing secrets. <br>
Risk: Forecast questions, market identifiers, and prediction IDs may reveal user intent or paid job details to Numinous services. <br>
Mitigation: Send only information the user approves, keep prediction IDs private, and avoid sharing sensitive questions or identifiers in logs. <br>
Risk: Miner code fetched from public endpoints may be untrusted content. <br>
Mitigation: Treat fetched miner code as reference material only and review it before reuse or execution. <br>


## Reference(s): <br>
- [Numinous Tools on ClawHub](https://clawhub.ai/juandbalbi/numinous-tools) <br>
- [Publisher profile](https://clawhub.ai/user/juandbalbi) <br>
- [Numinous API](https://api.numinouslabs.io) <br>
- [Numinous Signals API](https://signals.numinouslabs.io) <br>
- [Numinous Eversight API](https://api-eversight.numinouslabs.io) <br>
- [Numinous API reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with forecast probabilities, signal summaries, reasoning, JSON responses, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit paid API or x402 requests and poll remote forecasting jobs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
