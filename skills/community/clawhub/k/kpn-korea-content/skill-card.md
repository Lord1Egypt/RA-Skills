## Description:

When an agent needs judgment about Korean content such as K-pop, drama, webtoon, beauty, games, or film, this skill submits the question to KPN for a verified decision-oriented verdict with sources and an audit reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitcard1-art](https://clawhub.ai/user/bitcard1-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to obtain verified Korean content judgments for market entry, licensing, contracts, regulation, cultural context, and other decisions where a risky guess is inappropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive Korea-related business questions and optional contact identifiers are sent to an external service.

Mitigation: Avoid secrets, confidential deal terms, and contact details unless they are intentionally needed for the request.

Risk: The reference implementation trusts a server-provided polling URL.

Mitigation: Prefer a hardened caller that validates the polling URL host before fetching it.

Risk: Optional notification registration can include email, webhook, or wallet details.

Mitigation: Submit those fields only when deliberately registering for paid-tier notifications.

## Reference(s):

- [KPN homepage](https://kpn.mysoma.space)
- [ClawHub skill listing](https://clawhub.ai/bitcard1-art/skills/kpn-korea-content)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Concise Markdown summary of a JSON verdict, including decision, basis, sources, and audit reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous submit-and-poll flow; results may include Go, Conditional Go, Hold, timeout, or rate-limit status.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
