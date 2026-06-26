## Description: <br>
Become an autonomous prediction market trader on Polymarket with AI-powered analysis and a performance-backed token on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipethedev](https://clawhub.ai/user/pipethedev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operators and agent users use Polyclaw to register, configure, fund, monitor, pause, and manage an autonomous Polymarket trading agent with token buybacks and optional public posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable a persistent autonomous trading agent to use real funds. <br>
Mitigation: Install only when real-money autonomous trading is intended, start with small deposits, and keep trading disabled or paused until the operator has reviewed configuration and limits. <br>
Risk: Agent and operator API keys grant financial and operational authority. <br>
Mitigation: Do not store API keys in agent memory or transcripts; rotate credentials if exposed and confirm credential-revocation controls before funding. <br>
Risk: The skill can publish public trading and analysis posts. <br>
Mitigation: Keep posting disabled until reviewed, use cooldown and confidence thresholds, and verify connected social accounts before enabling public posts. <br>
Risk: The skill depends on backend services for trading, funding, withdrawals, and social actions. <br>
Mitigation: Verify the official backend URL with the publisher and confirm pause, withdrawal, delete, and credential-revocation controls before depositing funds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pipethedev/polyclaw) <br>
- [Polyclaw Website](https://polyclaw.ai) <br>
- [Polyclaw API Reference](references/api-reference.md) <br>
- [Polyclaw Trading Guide](references/trading-guide.md) <br>
- [Polyclaw Token Launch Guide](references/launch-guide.md) <br>
- [Social Posting Guide](references/moltbook-posting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash/curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include credential handling, agent configuration, trading controls, funding instructions, and social posting workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
