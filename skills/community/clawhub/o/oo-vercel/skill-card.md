## Description:

This skill lets an agent read and manage Vercel projects, deployments, domains, environment variables, and webhooks through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Vercel projects, deployments, domains, environment variables, and webhooks through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI's startup behavior may add or refresh skills across agent installations.

Mitigation: Review and install the CLI separately; set OO_SKILLS_SYNC_DISABLED=1 if that synchronization is not wanted.

Risk: Vercel actions can change or delete projects, deployments, domains, environment variables, and webhooks, including production traffic.

Mitigation: Limit the connected Vercel account's permissions and retain explicit approval for production changes.

Risk: The remote installer contents and exact CLI binary are unverified.

Mitigation: Review and install the oo CLI separately before use.

## Reference(s):

- [Vercel](https://vercel.com)
- [Vercel REST API documentation](https://vercel.com/docs/rest-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Vercel action.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
