## Description:

Use Cuttly to retrieve short-link analytics and create short URLs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Cuttly can ask an agent to retrieve click analytics for a short URL or create a shortened URL through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback can run downloaded installer code, and its exact local changes could not be verified.

Mitigation: Review and approve CLI setup separately; prefer a verified, pinned installation and check whether it installs or updates other agent skills.

## Reference(s):

- [Cuttly API documentation](https://cutt.ly/api-documentation/cuttly-links-api)
- [Cuttly](https://cutt.ly)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON API responses with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analytics data or a newly created short URL, depending on the requested action.]

## Skill Version(s):

1.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
