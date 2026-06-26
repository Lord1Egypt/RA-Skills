## Description: <br>
Use when an agent needs to operate RapidX through MCP or CLI for portfolio reads, market reads, order preview, order submit/replace/cancel, position management, algo orders, or explicit live trading verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquiditytech](https://clawhub.ai/user/liquiditytech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through RapidX market, portfolio, order, position, algo-order, automation, and live-verification workflows after RapidX configuration has been verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent operating a real RapidX trading account. <br>
Mitigation: Use least-privilege API keys, start with read-only checks, and require exact preview confirmation before order, cancel, leverage, position-mode, close-position, or automation actions. <br>
Risk: Credentials could be exposed through chat, logs, or command output. <br>
Mitigation: Keep credentials in the agent host's secret store and do not echo secrets. <br>
Risk: Uncertain write results or timeouts could lead to duplicate or incorrect trading actions. <br>
Mitigation: Query account, order, position, or algo state before retrying and read back final state after each submitted write. <br>


## Reference(s): <br>
- [Capability Overview](references/capability-overview.md) <br>
- [Best Practices](references/best-practices.md) <br>
- [ClawHub release page](https://clawhub.ai/liquiditytech/ltp-rapidx-trading) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, text] <br>
**Output Format:** [Markdown guidance with inline MCP tool names, CLI commands, JSON response expectations, and final status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires observed tool or command evidence for trading claims; live writes require preview evidence, consent, and readback.] <br>

## Skill Version(s): <br>
1.0.14 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
