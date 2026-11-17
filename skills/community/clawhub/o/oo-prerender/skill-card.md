## Description:

Use Prerender to submit sitemaps, queue URLs for caching or recaching, check cache-clear status, and clear cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to manage Prerender caching by submitting sitemaps, queuing URLs, checking cache-clear jobs, and clearing cached pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup uses remote installers whose exact effects were unavailable for inspection, and documented defaults can add skills to other agent environments.

Mitigation: Review CLI installation separately, use a verified release, and disable startup skill synchronization if you only want this integration.

Risk: Wildcard cache clears may affect more URLs than intended.

Mitigation: Review the wildcard target carefully and obtain explicit approval before clearing cache.

Risk: Cache operations can change Prerender state.

Mitigation: Confirm the exact payload and effect with the user before running write actions.

## Reference(s):

- [Prerender API documentation](https://docs.prerender.io/docs/6-api)
- [Prerender](https://prerender.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Prerender account; action schemas are checked before submitting payloads.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
