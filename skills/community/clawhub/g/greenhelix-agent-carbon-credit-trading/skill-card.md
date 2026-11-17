## Description:

Agent-Powered Carbon Credit Trading & CBAM Compliance helps developers build autonomous carbon credit trading agents for credit discovery, MRV verification, escrow-protected trading, CBAM compliance automation, multi-agent portfolios, and dispute resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this guide to design OpenClaw-compatible agents that discover, verify, trade, retire, and audit carbon credits while supporting CBAM compliance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can create wallets, initiate trades, move funds, release escrow, or retire credits when pointed at production APIs.

Mitigation: Use sandbox endpoints and test credentials first, require explicit human approval for state-changing actions, and enforce transaction limits before any production use.

Risk: Escrow release or retirement workflows may rely on incorrect, stale, or incomplete carbon registry and verifier data.

Mitigation: Verify credit status, retirement confirmation, and MRV claims against authoritative registries and accredited verifier records before releasing escrow or reporting compliance.

Risk: The guide references both sandbox onboarding and production API behavior, which can confuse implementation posture.

Mitigation: Document the selected endpoint per deployment, separate sandbox and production credentials, and add dry-run checks for every trading workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mirni/skills/greenhelix-agent-carbon-credit-trading)
- [Publisher profile](https://clawhub.ai/user/mirni)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guide with inline Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GREENHELIX_API_KEY for authenticated GreenHelix API usage.]

## Skill Version(s):

1.3.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
