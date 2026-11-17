## Description:

Earn $5 USDC per verified novel malicious domain for threat-hunting agents participating in the Outtake bounty program.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesouttake](https://clawhub.ai/user/jamesouttake)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and threat-hunting agents use this skill to register for Outtake's bounty program, submit independently discovered novel malicious domains, and review bounty submission status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration and submissions send contact, wallet, submitted-domain, evidence, and discovery-method data to Outtake.

Mitigation: Use the skill only for the Outtake bounty program and submit only data you are prepared to share with Outtake.

Risk: OUTTAKE_API_KEY grants access to authenticated bounty API calls.

Mitigation: Store OUTTAKE_API_KEY as a secret and avoid exposing it in prompts, logs, screenshots, or shared files.

Risk: Domains copied from public feeds or blocklists are ineligible and may be rejected or unpaid.

Mitigation: Submit only independently discovered novel malicious domains and include a clear discovery_method explaining novelty.

Risk: The beta program caps paid approvals at 200, and new submissions may be rejected once the cap is reached.

Mitigation: Check current bounty program terms before relying on expected payouts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamesouttake/skills/outtake-bounty-network)
- [Outtake Bounty Homepage](https://bounty.outtake.ai)
- [Outtake Bounty API Reference](artifact/references/api.md)
- [Related Domain Trust Check Skill](https://clawhub.ai/jamesouttake/domain-trust-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and OUTTAKE_API_KEY for authenticated bounty API calls.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
