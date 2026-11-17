## Description:

Get calibrated probabilities from Numinous (Bittensor Subnet 6) with metadata/provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juandbalbi](https://clawhub.ai/user/juandbalbi)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to request paid Numinous forecasts for natural-language questions or structured event definitions, then receive a calibrated probability with provenance metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically sign x402 payments from a configured wallet key.

Mitigation: Use a dedicated low-balance wallet key and review or add local payment limits for amount, recipient, network, and asset before use.

Risk: Forecasting questions and event details are submitted to the Numinous remote API.

Mitigation: Avoid sending confidential forecasting questions, private business plans, or sensitive event descriptions.

Risk: Runtime dependencies control wallet signing and HTTP payment behavior.

Mitigation: Pin dependencies where possible and review dependency updates before running the skill with funded wallet credentials.

## Reference(s):

- [Numinous homepage](https://numinouslabs.io/)
- [Numinous forecasting API endpoint](https://api.numinouslabs.io)
- [ClawHub skill page](https://clawhub.ai/juandbalbi/skills/numinous-forecast)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON printed by command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prediction probability, forecast timestamp, forecaster identifier, metadata, parsed query fields in query mode, and error status.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
