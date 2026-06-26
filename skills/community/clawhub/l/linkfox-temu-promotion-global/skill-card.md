## Description: <br>
Helps agents call LinkFox-gatewayed Temu Global promotion APIs for querying campaigns, finding candidate goods, enrolling goods, checking operation results, and updating enrolled promotion goods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, commerce operators, and developers use this skill to manage Temu Global promotion workflows through scripted API calls, including campaign lookup, goods enrollment, enrolled goods queries, operation polling, and updates to promotion goods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive LinkFox API keys and Temu access tokens, including optional local plaintext token storage. <br>
Mitigation: Treat tokens as passwords, avoid exposing them in logs or shared chats, and restrict permissions on the local token store. <br>
Risk: Promotion enrollment, update, and deactivation operations can change live commerce listings or campaign participation. <br>
Mitigation: Review request payloads and confirm intended store, site, token purpose, goods, prices, quantities, and operation type before execution. <br>
Risk: Requests are sent through the LinkFox gateway before reaching Temu APIs. <br>
Mitigation: Install only if the publisher and gateway are trusted for the relevant Temu seller account and commercial workflow. <br>
Risk: Broad proxy and file-download tools may access more Temu API surface area than the promotion-specific wrappers. <br>
Mitigation: Prefer the specific promotion scripts when possible and review arbitrary proxy types or file-download requests before running them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/linkfox-ai/linkfox-temu-promotion-global) <br>
- [API reference](references/api.md) <br>
- [Temu access token authorization](references/access-token.md) <br>
- [Partner Global promotion catalog](references/partner-global-catalog.md) <br>
- [Promotion API index](references/apis/README.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON command examples and Python script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and either a Temu access token or a saved store key; some scripts can download files or modify promotion goods.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
