## Description:

Netlify (netlify.com). Use this skill for ANY Netlify request — reading, creating, updating, and deleting data. Whenever a task involves Netlify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage Netlify sites, deployments, forms, and submissions through a connected Netlify account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can execute unverified remote code and broaden changes to agent tools.

Mitigation: Review and install the oo CLI separately before setup; consider disabling bundled-skill synchronization with OO_SKILLS_SYNC_DISABLED, and retain approval checks for changes and deletions.

## Reference(s):

- [Netlify](https://www.netlify.com)
- [Netlify API documentation](https://open-api.netlify.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Netlify account and its permissions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
