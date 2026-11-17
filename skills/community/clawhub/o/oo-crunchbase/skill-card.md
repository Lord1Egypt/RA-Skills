## Description:

Search and read Crunchbase organization and acquisition data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Crunchbase data can search for organizations and acquisitions, look up organization or acquisition records, and retrieve linked IPO information through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote installer code and may introduce broader agent changes.

Mitigation: Review and approve CLI installation separately, verify the installer and release, check automatic skill synchronization, and connect only the intended Crunchbase account.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-crunchbase)
- [Crunchbase API documentation](https://data.crunchbase.com/docs/using-the-api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Crunchbase connector results returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results for organizations, acquisitions, and IPOs, plus entity suggestions.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
