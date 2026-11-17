## Description:

Beaconcha.in (beaconcha.in). Use this skill for ANY Beaconcha.in request — searching and reading data. Whenever a task involves Beaconcha.in, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve Beaconcha.in network performance, staking queue, validator, and consensus reward data through the user's OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing oo CLI can prompt installation of unverified external software.

Mitigation: Review the setup before installing, use a verified CLI release, and require approval before installation or changes to agent skills.

Risk: Requests pass through the OOMOL-connected account and may consume credit.

Mitigation: Keep requests scoped to the user's task and consider the account's credit usage when making repeated queries.

## Reference(s):

- [Beaconcha.in](https://beaconcha.in)
- [Beaconcha.in API documentation](https://docs.beaconcha.in/)
- [oo CLI source and documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [OOMOL Beaconcha.in connection setup](https://console.oomol.com/connections/beaconchain)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-beaconchain)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Beaconcha.in query results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only data for supported network, staking queue, validator, and consensus reward queries.]

## Skill Version(s):

1.0.5 (source: frontmatter; corroborated by server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
