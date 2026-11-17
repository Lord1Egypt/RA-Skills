## Description:

Work with Metabase by searching and querying data, and creating or updating questions, dashboards, collections, and metrics through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Metabase users and analysts use this skill to discover data, run queries, and work with saved questions, dashboards, collections, and metrics through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes a remote CLI installer that has not been verified.

Mitigation: Review and install a pinned, verified CLI release before enabling the skill.

Risk: The connected account can perform writes and SQL execution, while the hosted connector has not been verified.

Mitigation: Use a narrowly scoped Metabase API key, assess trust in OOMOL, and retain explicit approval for writes and SQL execution. Decide whether to disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Metabase](https://www.metabase.com)
- [Metabase API documentation](https://www.metabase.com/docs/latest/api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis]

**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and Metabase results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific permissions and limits apply.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
