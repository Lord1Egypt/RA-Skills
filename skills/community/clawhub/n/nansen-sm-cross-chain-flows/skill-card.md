## Description:

Is SM buying this token on one chain but selling on another? Detect capital rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto analysts use this skill to compare smart-money net flows for a token across selected chains and identify possible capital rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls may trigger x402 payments from the configured wallet, and each call in a loop can incur a charge.

Mitigation: Review wallet authorization, payment policy, and spending limits before running research calls; keep loops and chain selections scoped to the intended analysis.

Risk: Net-flow results omit activity below the reporting threshold, which could be mistaken for unsupported chains or no activity.

Mitigation: Interpret missing results as below-threshold activity, not proof that a chain is unsupported; use the documented limit when seeking mid-tier tokens.

Risk: The workflow requires an explicitly selected authenticated API key or saved browser session.

Mitigation: Check authentication status before research and stop if selection or renewal fails; do not switch to anonymous access to retry.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-sm-cross-chain-flows)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with inline Bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares net-flow observations across chains; uses 24h and 7d divergence as rotation signals.]

## Skill Version(s):

0.1.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
