## Description:

Use the openclaw_paid_action tool to list actions, generate USDC invoices, and execute only after manual payment confirmation on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icetroll](https://clawhub.ai/user/icetroll)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to gate configured OpenClaw actions behind USDC invoice creation, payment confirmation, and post-payment execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured paid actions can execute external commands after payment confirmation.

Mitigation: Review the installed openclaw-paid-actions plugin separately and verify every configured paid action command before enabling autonomous execution.

Risk: Payment-gated execution depends on trusted invoice, payment confirmation, and storage configuration.

Mitigation: Require a persistent invoice secret and invoice store path, and only allow autonomous execution for commands that are acceptable after payment confirmation.

## Reference(s):

- [OpenClaw Paid Actions on ClawHub](https://clawhub.ai/icetroll/skills/openclaw-paid-actions)
- [icetroll publisher profile](https://clawhub.ai/user/icetroll)

## Skill Output:

**Output Type(s):** [guidance, API Calls, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with JSON configuration examples and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured paid-action commands; command output may be truncated by the plugin.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
