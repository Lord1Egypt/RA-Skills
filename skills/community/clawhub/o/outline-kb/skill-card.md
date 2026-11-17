## Description:

Helps agents interact with an Outline knowledge base API to search, create, edit, export, and administer documents, collections, users, comments, shares, groups, and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1944876825](https://clawhub.ai/user/1944876825)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent work with a configured Outline workspace through its API, including document search, content creation, collection management, exports, invitations, and permission changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through broad Outline read, write, admin, sharing, export, and OAuth-management operations using the provided API key.

Mitigation: Install only for intended Outline workspaces and prefer a least-privilege or read-only API key whenever the workflow does not require writes or administration.

Risk: Exports, sharing changes, invitations, permission edits, user or group administration, trash deletion, and OAuth client or secret operations can disclose data or alter workspace access.

Mitigation: Require explicit human confirmation before these sensitive actions and review the target document, collection, user, group, or OAuth object before execution.

Risk: A misconfigured Outline base URL could send requests or bearer tokens to an unintended endpoint.

Mitigation: Set OUTLINE_BASE_URL only to a trusted Outline API URL and avoid exposing OUTLINE_API_KEY in logs, shared prompts, or command output.

## Reference(s):

- [Outline API Endpoints Reference](references/api-endpoints.md)
- [Outline OpenAPI Specification](https://github.com/outline/openapi/blob/main/spec3.yml)
- [ClawHub Skill Page](https://clawhub.ai/1944876825/skills/outline-kb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and API endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OUTLINE_BASE_URL and OUTLINE_API_KEY; Outline API responses are JSON.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
