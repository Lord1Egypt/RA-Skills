## Description:

BetterContact (bettercontact.rocks). Use this skill for ANY BetterContact request — reading, creating, and updating data. Whenever a task involves BetterContact, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve account credits and enrichment results, or submit leads for BetterContact waterfall enrichment through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback can run a downloaded CLI installer whose full effects were unavailable for inspection.

Mitigation: Require separate approval before running the installer and prefer a pinned, verified release.

Risk: OOMOL intermediates the connection and submitted lead data.

Mitigation: Review and understand OOMOL's handling of connection credentials and lead data before submitting leads.

## Reference(s):

- [BetterContact](https://bettercontact.rocks)
- [BetterContact API documentation](https://doc.bettercontact.rocks/api-reference/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields depend on the selected action; enrichment submissions return a request handle.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
