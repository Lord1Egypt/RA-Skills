## Description: <br>
ProductClank helps agents create Boost and Discover campaigns that amplify social posts with community engagement or find relevant Twitter/X conversations for AI-generated replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xCovariance](https://clawhub.ai/user/0xCovariance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External builders, founders, marketers, and developer agents use this skill to run ProductClank campaigns that boost existing social posts or discover Twitter/X conversations for community-powered replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend ProductClank credits and manage public marketing campaigns. <br>
Mitigation: Require explicit approval before credit spend, post generation, deletion, delegation, or recurring runs. <br>
Risk: Generated promotional replies can be misleading if they imply undisclosed sponsorship, incentives, or personal experience. <br>
Mitigation: Review and rewrite campaign prompts and public replies so they are truthful and disclose sponsorship, incentives, or agent-generated participation when applicable. <br>
Risk: A leaked or overbroad ProductClank API key could allow unauthorized campaign actions. <br>
Mitigation: Use a dedicated limited API key, store it securely, and rotate it when access changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xCovariance/productclank-community-growth) <br>
- [ProductClank Website](https://www.productclank.com) <br>
- [ProductClank Communiply Web UI](https://app.productclank.com/communiply/) <br>
- [ProductClank Agent API Endpoint](https://app.productclank.com/api/v1/agents) <br>
- [Communiply CLI](https://github.com/covariance-network/communiply-cli) <br>
- [README](README.md) <br>
- [API Reference](references/API_REFERENCE.md) <br>
- [Code Examples](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API payloads, TypeScript examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ProductClank APIs that require PRODUCTCLANK_API_KEY and spend ProductClank credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
