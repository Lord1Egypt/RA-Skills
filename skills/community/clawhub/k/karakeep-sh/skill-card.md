## Description:

Karakeep bookmark manager with full native RESTful API support including notes, updates, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vandeefeng](https://clawhub.ai/user/vandeefeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage Karakeep bookmarks from an agent workflow, including creating, searching, listing, tagging, updating notes, and deleting bookmarks through REST API helper commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured API key can read, create, update, tag, list, and delete bookmark data.

Mitigation: Install only for trusted Karakeep endpoints, use HTTPS, and prefer a limited-scope API key when available.

Risk: Bookmark deletion can remove account data and the helper script does not enforce confirmation.

Mitigation: Require explicit user confirmation before running delete commands and verify the target bookmark ID before execution.

Risk: The security verdict requires review because the helper can change bookmark account data.

Mitigation: Review commands and arguments before execution, especially create, update, tag, list membership, and delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vandeefeng/skills/karakeep-sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KARAKEEP_SERVER_URL, KARAKEEP_API_KEY, jq, and a reachable Karakeep server.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
