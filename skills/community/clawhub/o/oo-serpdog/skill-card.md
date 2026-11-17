## Description:

Use Serpdog to search Google and retrieve account information through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve connected Serpdog account details and Google autocomplete, web, news, and video search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup immediately executes downloaded installer code, and the hosted connector implementation is outside the verified artifact.

Mitigation: Review and approve CLI installation separately, use a verified fixed release, and consider disabling automatic skill synchronization.

Risk: Queries and connected account access pass through OOMOL.

Mitigation: Avoid sending sensitive information unless that data flow is acceptable.

## Reference(s):

- [Serpdog API documentation](https://docs.serpdog.io/)
- [Serpdog](https://serpdog.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured Serpdog response data (JSON)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and its input schema.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
