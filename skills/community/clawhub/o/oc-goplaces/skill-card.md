## Description:

Query Google Places for text search, place details, resolve, reviews, or scriptable JSON via goplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use the goplaces command-line tool to search for places, resolve locations, retrieve place details and reviews, and obtain JSON results for scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires GOOGLE_PLACES_API_KEY, so commands depend on a credential.

Mitigation: Provide the key through a protected environment or secret manager, and avoid placing it in prompts, shell history, or generated output.

Risk: The optional GOOGLE_PLACES_BASE_URL setting can route requests through a proxy or alternate endpoint.

Mitigation: Set it only to an endpoint you trust.

## Reference(s):

- [Goplaces skill page](https://clawhub.ai/hillstreet-ph/skills/oc-goplaces)
- [Goplaces project homepage](https://github.com/steipete/goplaces)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [CLI text output or JSON, with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports scriptable JSON output; pagination and search filters are available.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
