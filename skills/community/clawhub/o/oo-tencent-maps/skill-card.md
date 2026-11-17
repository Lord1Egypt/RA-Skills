## Description:

Search Tencent Maps and retrieve place, address, route, district, weather, and location data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to search Tencent Maps, look up addresses and places, plan routes, inspect districts, and retrieve weather or location data. The agent uses the connected OOMOL account to make the requested map queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified downloads, and supporting software can change other agents’ installed skills; downloaded installers and hosted connector code remain unverified.

Mitigation: Review supporting software before proceeding, use a verified CLI release, set OO_SKILLS_SYNC_DISABLED=1 before running it, and share only the location details needed for the request.

## Reference(s):

- [Tencent Maps API documentation](https://lbs.qq.com/docs-square/)
- [Tencent Maps](https://lbs.qq.com)
- [OO CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON map-action results with concise text responses and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No output file is specified.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
