## Description:

Discover NEAR airdrops, check eligibility, claim rewards, and track claimed airdrops across multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

External users and crypto developers can use this skill to list NEAR ecosystem airdrop links, review manual eligibility guidance, and track local claim status for NEAR accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill overstates airdrop checking and claiming, and records manual, unverified actions as claimed.

Mitigation: Treat the skill output as URL and local tracking guidance only; independently verify eligibility, claim pages, wallet prompts, and signed transactions before acting.

Risk: Claim flows require external wallet interaction and signing outside the skill.

Mitigation: Review every destination URL and wallet prompt directly with the relevant NEAR protocol before connecting a wallet or signing.

## Reference(s):

- [NEAR Ecosystem](https://near.org/ecosystem/)
- [NEAR Airdrops](https://near.org/airdrops/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with URLs and local tracking records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local tracking data to ~/.near-airdrop/tracking.json.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
