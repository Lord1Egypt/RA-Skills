## Description:

Crack and identify hashes by attempting to match them against known hash databases and common plaintext values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security professionals, penetration testers, incident responders, and developers use this skill to submit hashes for lookup and receive possible plaintext matches, detected hash type, found status, and confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted hashes are sent to the provider's external API and may be sensitive.

Mitigation: Submit only hashes you are authorized to share, and avoid production password hashes, customer data, regulated evidence, or secrets unless the provider's data-handling practices are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/hash-finder)
- [API Docs](https://api.mkkpro.com:8008/docs)
- [Hash Finder API Route](https://api.mkkpro.com/security/hash-finder)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the queried hash, plaintext when found, hash type, found status, and confidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
