## Description:

Fetch recent GitHub activity from the Nom feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lws803](https://clawhub.ai/user/lws803)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to search and summarize recent public GitHub activity across repositories or the global Nom feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, repository names, organization filters, and date filters are sent to the third-party Nom service at beta.nomit.dev.

Mitigation: Use the skill only with information appropriate to share with that service, and avoid sensitive private repository or organization details.

Risk: Invalid or overly broad user input could produce malformed requests or unexpectedly large result sets.

Mitigation: Apply the documented validation, URL encoding, and limit clamping before fetching results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lws803/skills/nom)
- [Nom Feed Service](https://beta.nomit.dev)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with links and timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches may send search terms, repository names, organization filters, and date filters to the third-party Nom service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
