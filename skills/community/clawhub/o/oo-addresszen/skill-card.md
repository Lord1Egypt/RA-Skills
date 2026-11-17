## Description:

Search and retrieve address data through AddressZen, including address suggestions, key availability, and formatted U.S. addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to search address suggestions, check key availability, and retrieve a formatted U.S. address through a connected AddressZen account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded installer software without a separate user approval step, and its exact effects are unverified.

Mitigation: Review and approve CLI installation separately, use a verified version, and review or disable automatic skill synchronization before running it.

Risk: Address queries are sent through OOMOL to AddressZen.

Mitigation: Send only address information that is appropriate to share with both services.

## Reference(s):

- [AddressZen](https://addresszen.com)
- [AddressZen API documentation](https://docs.addresszen.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [AddressZen ClawHub release](https://clawhub.ai/oomol/skills/oo-addresszen)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Address lookup results returned as JSON, with concise textual summaries when presented to the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI, a signed-in OOMOL account, and an active AddressZen connection.]

## Skill Version(s):

1.0.5 (source: skill metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
