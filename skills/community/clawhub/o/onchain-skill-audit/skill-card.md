## Description: <br>
On-chain skill provenance registry for checking, registering, auditing, and vouching for agent skills on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Emanz1](https://clawhub.ai/user/Emanz1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect on-chain provenance before installation and to register, audit, or vouch for agent skills on Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration, audit, and vouch operations can create permanent public on-chain records and may require wallet signing. <br>
Mitigation: Verify npm package behavior and transaction details before signing; use a low-risk wallet where possible and publish only content safe to be permanent and public. <br>
Risk: Audit writes require IQ tokens and on-chain transaction costs may apply. <br>
Mitigation: Confirm token requirements, wallet balance, and transaction intent before submitting audits or other writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Emanz1/onchain-skill-audit) <br>
- [@rocketlabs/skill-audit npm package](https://www.npmjs.com/package/@rocketlabs/skill-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command-oriented guidance and provenance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only checks are available; registration, audit, and vouch operations may write public on-chain records.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
