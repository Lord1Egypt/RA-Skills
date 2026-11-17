## Description:

Open interest divergence from price - detects smart-money positioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to request a paid open-interest divergence signal for crypto market-positioning analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent invocations may spend funds automatically through a reusable wallet private key.

Mitigation: Use a dedicated low-balance wallet, require explicit confirmation where possible, and configure payment caps or rate limits before unattended use.

Risk: The integration depends on EVM_PRIVATE_KEY, which is sensitive credential material.

Mitigation: Store the key only in the agent's secret-management path, scope it to payment use, and avoid using a primary wallet.

Risk: The skill provides a paid crypto market signal that may be misread as complete trading guidance.

Mitigation: Treat the response as one signal for analysis, validate it independently, and avoid delegating trading decisions solely to this output.

## Reference(s):

- [Oi Divergence Signal](https://apexrunner.ai/signals/oi-divergence)
- [Oi Divergence ClawHub Listing](https://clawhub.ai/kynto2001-ctrl/skills/oi-divergence)
- [Publisher Profile](https://clawhub.ai/user/kynto2001-ctrl)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration]

**Output Format:** [Markdown instructions with a Python API-call example and JSON signal response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
