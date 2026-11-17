## Description:

Use the connected Fivetran account to search and read data through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve hybrid deployment agent, external log service, and transformation project information from their connected Fivetran account. It guides them to inspect each action's schema and returns the action results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded code; the remote installer and hosted connector implementation remain unverified.

Mitigation: Install a verified oo CLI release yourself and review the permissions granted through OOMOL.

Risk: The required CLI has undisclosed effects on other agents’ skills through startup synchronization.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

## Reference(s):

- [Fivetran REST API documentation](https://fivetran.com/docs/rest-api/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON action results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Fivetran account and selected read action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
