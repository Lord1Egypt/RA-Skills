## Description:

TomTom (developer.tomtom.com). Use this skill for ANY TomTom request — searching and reading data. Whenever a task involves TomTom, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can search for places, addresses, and nearby points of interest, convert addresses to coordinates, and convert coordinates to address candidates through an OOMOL-connected TomTom account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and may add bundled agent skills without clear user control.

Mitigation: Install a verified oo CLI release yourself and explicitly control its bundled-skill synchronization.

Risk: Addresses and coordinates are passed through OOMOL to TomTom.

Mitigation: Avoid submitting sensitive location data and use the skill only when that data flow is acceptable.

## Reference(s):

- [TomTom Search API documentation](https://developer.tomtom.com/search-api/documentation/search-service/fuzzy-search)
- [TomTom Developer Portal](https://developer.tomtom.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Structured TomTom search results with concise text guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and geocoding results depend on the connected TomTom account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
