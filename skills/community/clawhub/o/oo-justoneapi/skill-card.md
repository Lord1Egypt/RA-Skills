## Description:

Search and read data from Just One API through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use the skill to search and retrieve data from Just One API sources through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run an unverified remote installer; the installer and CLI implementation were not included in the review.

Mitigation: Install and verify a fixed oo CLI release yourself, and require the agent to stop if it is missing. Review OOMOL connection scopes and billing before use.

## Reference(s):

- [Just One API documentation](https://docs.justoneapi.com/)
- [Just One API homepage](https://justoneapi.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API responses with brief textual task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data and available fields depend on the selected service and action.]

## Skill Version(s):

1.0.2 (source: frontmatter metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
