## Description:

Geoapify (geoapify.com). Use this skill for ANY Geoapify request — searching and reading data. Whenever a task involves Geoapify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Geoapify address suggestions, geocoding results, routes, and travel matrices through a connected Geoapify account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may persistently change other agents’ skills without the skill explaining those wider effects.

Mitigation: Review the CLI’s installation effects, prefer a reviewed and pinned installation, and set OO_SKILLS_SYNC_DISABLED before invoking it if automatic skill changes are unwanted.

Risk: Location details submitted through this skill may be processed by OOMOL and Geoapify.

Mitigation: Submit only location details that you intend OOMOL and Geoapify to process.

## Reference(s):

- [Geoapify API documentation](https://apidocs.geoapify.com/)
- [Geoapify](https://www.geoapify.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action inputs and Geoapify results, with text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected geocoding, autocomplete, routing, or matrix action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
