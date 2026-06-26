## Description: <br>
Polymarket prediction markets: analytics, trading, hot markets, price movements, top traders, and market search. Powered by prob.trade. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query prob.trade prediction market analytics and trade on Polymarket through an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel live Polymarket orders. <br>
Mitigation: Require human review and approval before every order placement or cancellation. <br>
Risk: The skill requires prob.trade API credentials in environment variables or a local config file. <br>
Mitigation: Use revocable or least-privilege API keys where available and protect ~/.openclaw/skills/probtrade/config.yaml with appropriate local file permissions. <br>
Risk: The server-resolved release name differs from the artifact's probtrade skill name. <br>
Mitigation: Verify the ClawHub publisher handle and intended package before installing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vlprosvirkin/openclaw-skill-publish) <br>
- [prob.trade Dashboard](https://app.prob.trade) <br>
- [prob.trade Public API](https://api.prob.trade/api/public/overview) <br>
- [prob.trade API Docs](https://prob.trade/docs/public-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call external prob.trade APIs and may require PROBTRADE_API_KEY, PROBTRADE_API_SECRET, or ~/.openclaw/skills/probtrade/config.yaml.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
