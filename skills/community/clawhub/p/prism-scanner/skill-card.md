## Description:

Instant rug pull detection for crypto tokens using PRISM risk checks for holder concentration, liquidity, contract risks, and copycat signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to scan token symbols or contract addresses for rug-pull, copycat, holder concentration, liquidity, and contract-risk signals before acting on or surfacing token information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token symbols or contract addresses are sent to the configured PRISM service during scans.

Mitigation: Install and use the skill only when sharing those inputs with the configured PRISM service is acceptable.

Risk: Risk scores and scan details are advisory and may be incomplete or unsuitable for automated financial decisions.

Mitigation: Review text or JSON results before using them in automation and do not treat the output as financial advice.

Risk: Changing PRISM_URL can redirect scan requests to a different service.

Mitigation: Keep PRISM_URL explicit and trusted in deployment configuration, especially in shared agent environments.

## Reference(s):

- [ClawHub Prism Scanner skill page](https://clawhub.ai/nextfrontierbuilds/skills/prism-scanner)
- [Publisher profile: nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)
- [PRISM service endpoint](https://strykr-prism.up.railway.app)
- [NextXFrontier publisher link](https://x.com/NextXFrontier)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text report or JSON from shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a token symbol or contract address as input and may call the configured PRISM API service.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
