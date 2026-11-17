## Description:

Google Docs API integration with managed OAuth via Maton for creating documents, reading text, writing or appending content, search and replace, applying basic formatting, and exporting documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and end users use this skill to automate Google Docs workflows through Maton, including document creation, reading, editing, formatting, connection management, and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite, delete ranges, replace all matching text, and export Google Docs content without built-in confirmation controls.

Mitigation: Use it only with documents the agent is allowed to modify, keep backups or Google Docs version history available, and require explicit human approval before overwrite, delete, replace-all, or export operations.

Risk: The MATON_API_KEY grants access to Maton-mediated Google Docs operations.

Mitigation: Protect MATON_API_KEY as a credential, avoid committing it to source control, and scope deployment environments so only approved agents can read it.

Risk: The dependency declaration allows newer requests releases than the version used during review.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tankeito/skills/google-docs-operator)
- [Publisher profile](https://clawhub.ai/user/tankeito)
- [Maton](https://maton.ai)
- [Google Docs API REST reference](https://developers.google.com/workspace/docs/api/reference/rest)
- [documents.get](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/get)
- [documents.create](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/create)
- [documents.batchUpdate](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate)
- [Google Docs request types](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/request)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON responses, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an authorized Google Docs connection.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, _meta.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
