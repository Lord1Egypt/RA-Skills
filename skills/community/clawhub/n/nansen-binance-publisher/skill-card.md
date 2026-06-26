## Description: <br>
Automatically fetches Nansen on-chain data, drafts a Binance Square daily report, and can publish the approved content to Binance Square. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcii](https://clawhub.ai/user/0xcii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Crypto analysts and Binance Square creators use this skill to turn Nansen on-chain data into recurring market reports and optionally publish them from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Binance Square publishing key to post public content automatically or on a schedule. <br>
Mitigation: Prefer /nansen with preview and approval; use /nansen_auto and cron only when unattended public posting is intentional. <br>
Risk: Publishing and data-fetching credentials are required for normal operation. <br>
Mitigation: Store keys in secure environment variables or a secret manager, and keep a revocation path for the Binance publishing key. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xcii/nansen-binance-publisher) <br>
- [Nansen API key signup](https://nsn.ai/7LOuQVx1Jvh) <br>
- [Binance account setup](https://accounts.binance.com/zh-CN/register?ref=35266688) <br>
- [Publisher X profile](https://x.com/AntCaveClub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text reports and concise setup guidance, with shell commands for CLI installation or cron scheduling when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and X_SQUARE_OPENAPI_KEY; /nansen previews content before posting, while /nansen_auto is intended for explicit unattended publishing.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
