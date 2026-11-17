## Description:

Immortal helps agents assess crypto asset vitality by calling the Majestify API for risk metrics such as Sharpe ratio, Sortino ratio, value at risk, drawdown, and vitality classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majestyatenkhu](https://clawhub.ai/user/majestyatenkhu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to request crypto asset risk metrics and receive human-readable and machine-readable vitality assessments for resource management workflows. The generated classifications can support analysis, but should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be directed to use arbitrary API hosts.

Mitigation: Use only the default Majestify endpoint or another trusted HTTPS endpoint, especially in environments with access to private networks or sensitive internal services.

Risk: Coin and API arguments may come from untrusted prompts.

Mitigation: Validate requested assets and endpoint values before execution, and avoid running prompt-supplied arguments without review.

Risk: Vitality classifications may be mistaken for investment recommendations.

Mitigation: Treat the output as risk-analysis support only and do not rely on classifications as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/majestyatenkhu/skills/immortal)
- [Majestify](https://majestify.io)
- [Default Majestify API endpoint](https://crypto-health-hub.onrender.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable stdout with machine-readable JSON emitted to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-asset vitality status, rationale, and risk metrics from a live HTTPS API.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
