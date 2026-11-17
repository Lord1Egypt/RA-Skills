## Description:

Fetch recent GitHub activity from the Nom feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lws803](https://clawhub.ai/user/lws803)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to query recent GitHub repository or organization activity from Nom and receive concise summaries of pull requests, issues, releases, or pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to beta.nomit.dev and may include repository names, organization names, date filters, or search terms supplied by the user.

Mitigation: Review query content before use and avoid sending sensitive or private repository information to the external feed service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lws803/skills/nom-feed)
- [Nom feed service](https://beta.nomit.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summaries with links, or RSS XML when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl to request public feed data from beta.nomit.dev; supports filters for repository, organization, event type, search text, date range, result limit, and RSS output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
