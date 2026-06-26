## Description: <br>
Temu Ads Global helps agents use LinkFox gateway scripts for Temu Global Partner Ads APIs covering ad creation, modification, ROAS prediction, reports, details, logs, and eligible-goods queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to manage Temu Global advertising workflows through LinkFox, including creating or modifying ads, checking eligible goods, predicting ROAS, and querying reports and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, delete, pause, or change budgets and ROAS for live Temu ads. <br>
Mitigation: Require explicit user confirmation and payload review before executing live ad-changing operations. <br>
Risk: The skill handles LinkFox and Temu credentials, including locally saved Temu access tokens. <br>
Mitigation: Use least-privilege, short-lived tokens; avoid saving production tokens on shared machines; keep token listings masked. <br>
Risk: The proxy scripts can send broad Temu API calls beyond a narrow ads-only workflow. <br>
Mitigation: Limit use to documented Partner Global Ads endpoints and review requested API types and parameters before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-temu-ads-global) <br>
- [API reference](references/api.md) <br>
- [Access token authorization guide](references/access-token.md) <br>
- [Partner Global Ads catalog](references/partner-global-catalog.md) <br>
- [Per-endpoint API index](references/apis/README.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON command examples and Python script invocations; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and a Temu access token or storeKey; scripts may call LinkFox and Temu gateway endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
