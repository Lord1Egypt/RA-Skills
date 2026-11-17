## Description:

Enables an agent to search and read HERE location data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of agent assistants can search HERE places and addresses, geocode queries, look up returned location identifiers, and reverse-geocode coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified software and introduce broader agent changes without clear approval.

Mitigation: Review and approve CLI installation separately before enabling automatic setup; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Locations submitted to HERE may be shared through OOMOL.

Mitigation: Submit only locations intended to be shared through OOMOL with HERE.

## Reference(s):

- [HERE Geocoding and Search documentation](https://www.here.com/docs/category/geocoding-search)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-here)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Connector responses as JSON, with Markdown guidance and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests use JSON action payloads; results include HERE location or address data.]

## Skill Version(s):

1.0.5 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
