## Description: <br>
Automates OAuth login flows through Telegram-mediated user selection and confirmation for Google, Apple, Microsoft, GitHub, Discord, WeChat, and QQ. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloliuyongsheng-bot](https://clawhub.ai/user/helloliuyongsheng-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to automate OAuth login for websites while routing provider choice and authorization confirmation through Telegram. It is intended for browser sessions where the user has already configured provider accounts and a Telegram channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate sensitive OAuth account authorization to an agent using logged-in browser sessions. <br>
Mitigation: Install only for intentional OAuth automation, use a dedicated browser profile, and verify the provider account, target site, and requested permissions before approval. <br>
Risk: Telegram approval messages and QR-code or screenshot sharing can expose sensitive login context. <br>
Mitigation: Use a private Telegram chat or channel and avoid sending QR codes or screenshots unless required for the flow. <br>
Risk: Approval safeguards are limited to user confirmation and timeout behavior. <br>
Mitigation: Require an explicit user confirmation for each authorization request and cancel flows when confirmation is missing or unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloliuyongsheng-bot/oauth-helper) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with browser command examples, provider detection patterns, and provider-specific selectors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Clawd browser profile and a configured Telegram confirmation channel.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
