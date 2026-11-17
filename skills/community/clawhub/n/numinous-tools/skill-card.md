## Description:

Access Numinous forecasting tools for AI probability predictions on binary events, real-time signals from news and prediction markets, and usage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juandbalbi](https://clawhub.ai/user/juandbalbi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to request Numinous forecasts, retrieve scored signals for prediction markets or free-text questions, inspect leaderboard and miner information, and check account balance or usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends forecast questions, market interests, and API-key-authenticated requests to Numinous services.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting confidential forecast questions or market interests.

Risk: The skill can use API keys and x402 wallet signing for paid forecast requests.

Mitigation: Prefer the API-key route, keep keys out of logs and committed files, and use a dedicated low-balance wallet if x402 payment is required.

Risk: Endpoint override environment variables can redirect requests away from the default Numinous services.

Mitigation: Leave override variables unset unless deliberately testing a trusted endpoint.

Risk: The x402 payment path depends on unpinned external Python packages.

Mitigation: Pin and review dependencies before running the wallet-based script.

Risk: Prediction IDs can grant access to unauthenticated polling results.

Mitigation: Treat prediction IDs as sensitive and keep them out of shared logs, screenshots, chats, and committed files.

## Reference(s):

- [Numinous API Reference](reference.md)
- [Numinous Forecast API](https://api.numinouslabs.io/api/docs)
- [Numinous Signals API](https://signals.numinouslabs.io/docs)
- [Numinous OpenAPI Specification](https://api.numinouslabs.io/api/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/juandbalbi/skills/numinous-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast jobs are asynchronous and may include probabilities, miner metadata, reasoning, signal rankings, source URLs, balance data, or usage records.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
