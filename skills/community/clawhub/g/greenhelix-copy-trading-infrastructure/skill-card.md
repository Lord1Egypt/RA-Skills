## Description: <br>
Build copy trading infrastructure with verified leader performance, follower allocation models, slippage handling, performance escrow, and revenue sharing, using detailed Python code examples with marketplace and escrow integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to design protocol-agnostic copy trading infrastructure with GreenHelix marketplace registration, signed leader metrics, follower allocation controls, slippage handling, performance escrow, and revenue sharing. The skill is instruction-only and provides illustrative Markdown, Python, and shell examples rather than an executable trading system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples involve sensitive financial automation, trading permissions, and credentials. <br>
Mitigation: Use sandbox endpoints and test credentials first; do not provide production API keys, signing keys, wallet credentials, or exchange access until the implementation is audited and constrained. <br>
Risk: The guide includes under-scoped safety checks and verification claims for copy-trading workflows. <br>
Mitigation: Add real signature verification, period-bounded metric checks, webhook authentication, replay protection, and explicit audit logging before relying on any leader performance data. <br>
Risk: Automated follower execution can create financial loss through bad signals, slippage, or correlated order flow. <br>
Mitigation: Require manual approval gates, dry-run or paper-trading defaults, strict allocation caps, and slippage monitoring before allowing live order execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-copy-trading-infrastructure) <br>
- [GreenHelix sandbox endpoint](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guide; no executable install step.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
