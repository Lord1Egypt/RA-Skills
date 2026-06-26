## Description: <br>
Automatically routes AI requests to cost-optimal models based on task complexity, budget, and learned usage patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce model spend by automatically selecting lower-cost or higher-capability models based on request complexity, budget settings, and observed routing outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Pro/x402 workflow promotes autonomous payment for subscriptions without clear approval controls. <br>
Mitigation: Keep autonomous payments disabled unless wallet approval policies and spending limits are configured and reviewed. <br>
Risk: Payment verification is not suitable for real billing because the artifact accepts valid-looking transaction hashes instead of verifying recipient, amount, token, and confirmations on-chain. <br>
Mitigation: Use the free tier or test environments until on-chain verification is implemented, tested, and reviewed for billing use. <br>
Risk: The local database stores wallet-linked routing, performance, quota, and transaction history. <br>
Mitigation: Treat the SQLite database as sensitive local data; restrict file access and avoid sharing database exports unless wallet-linked history has been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AtlasPA/openclaw-smart-router) <br>
- [README](README.md) <br>
- [Routing Guide](ROUTING-GUIDE.md) <br>
- [API Reference](API-REFERENCE.md) <br>
- [Database Implementation](DATABASE-IMPLEMENTATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, CLI/API responses, configuration examples, and routing decision data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces model-selection recommendations, cost and quota summaries, routing history, and dashboard/API views backed by local SQLite storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
