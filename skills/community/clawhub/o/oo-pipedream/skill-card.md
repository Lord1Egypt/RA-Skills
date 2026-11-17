## Description:

Operate Pipedream through an OOMOL-connected account to search and read data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Pipedream apps and read account, workspace, workflow, and workflow event data through a connected Pipedream account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run remote installers and may introduce broader agent changes through automatic skill synchronization.

Mitigation: Review and verify the CLI installation, check its skill synchronization settings, and connect only the intended Pipedream account through OOMOL.

## Reference(s):

- [Pipedream REST API documentation](https://pipedream.com/docs/rest-api/overview)
- [Pipedream](https://pipedream.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance, Markdown]

**Output Format:** [JSON data and concise text or Markdown summaries, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inputs vary by Pipedream action; inspect the action schema before constructing a request.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
