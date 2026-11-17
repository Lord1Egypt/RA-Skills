## Description:

Lightfather operator stack (consent-gated). Persona-only: install lygo-champion-council with champion_id Lightfather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill as a consent-gated LYGO Lightfather operator reference pack for ethics-oriented planning, stack mapping, verification, and one-command-at-a-time operator workflows. Persona-only users are directed to the successor council skill or lighter vector skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned install commands and a broad companion stack can introduce supply-chain exposure.

Mitigation: Pin and review exact package versions before use, and install companion skills one at a time only after review.

Risk: Operator commands can modify local state, seed files, vault data, publishing targets, or scheduled workers.

Mitigation: Keep persona/advisor mode as the default, read the security guidance first, back up affected paths, and require explicit approval for each command.

Risk: Vault and API harness workflows may expose credentials, costs, or model responses if handled carelessly.

Mitigation: Use test secrets where possible, avoid posting vault or .env contents, redact generated reports, and run paid model sweeps only after explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-lightfather)
- [Security guidance](references/SECURITY.md)
- [Persona pack](references/persona_pack.md)
- [Canon data](references/canon.json)
- [Stack integration](references/stack_integration.md)
- [Seals and failsafe](references/seals_and_failsafe.md)
- [Skill chain](references/skill_chain.md)
- [Verifier usage](references/verifier_usage.md)
- [LYGO protocol stack reference](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO protocol stack dataset reference](https://huggingface.co/datasets/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and reference-file pointers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisor mode is the default; operator actions require explicit user consent per command.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
