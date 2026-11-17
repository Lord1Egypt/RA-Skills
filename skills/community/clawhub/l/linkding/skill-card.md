## Description:

Manage bookmarks with Linkding by listing, searching, creating, updating, archiving, deleting, tagging, checking URLs, and creating bundles through the Linkding REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage a Linkding bookmark collection through authenticated API calls, including bookmark search, creation, updates, archiving, deletion, tags, and bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent receives broad token-backed read, write, and delete access to the user's Linkding account.

Mitigation: Use this skill only with a Linkding account and token scope you are comfortable exposing to the agent, and rotate or revoke the token if access is no longer needed.

Risk: Destructive bookmark or bundle actions may remove saved data if the agent targets the wrong item.

Mitigation: Require the agent to show the target bookmark or bundle and get explicit confirmation before any delete operation.

Risk: Credentials may be exposed on shared machines or over insecure transport.

Mitigation: Use HTTPS only, store the credentials file with restrictive permissions, and avoid shared machines for this token.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Linkding base URL and API token supplied through a credentials file or environment variables.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
