## Description:

OpenStreetMap geocoding for forward and reverse geocoding and place lookups via the Nominatim API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert typed addresses into coordinates, reverse geocode coordinates into addresses, resolve ambiguous place names, and look up OpenStreetMap objects by ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an automatically resolved mcp-remote package, so installed code may differ from the reviewed artifact.

Mitigation: Pin mcp-remote to a reviewed version before installation and run it with least privilege.

Risk: Address and coordinate queries are sent to the Pipeworx gateway for processing.

Mitigation: Avoid submitting sensitive location data unless the gateway's handling is acceptable for the use case.

## Reference(s):

- [Pipeworx Nominatim homepage](https://pipeworx.io/packs/nominatim)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-nominatim)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Geocoding responses may include coordinates, bounding boxes, display names, addresses, and OpenStreetMap object identifiers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
