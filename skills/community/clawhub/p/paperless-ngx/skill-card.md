## Description:

Interact with Paperless-ngx document management system via REST API. Use when users want to search, upload, download, organize documents, manage tags, correspondents, or document types in their Paperless-ngx instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oskarstark](https://clawhub.ai/user/oskarstark)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage documents in a Paperless-ngx instance through REST API requests, including search, upload, download, metadata organization, task status checks, and pagination-aware response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes document deletion and bulk edit operations that can delete, reprocess, or change metadata for multiple documents.

Mitigation: Require the agent to show exact document IDs and obtain explicit confirmation before deletion, reprocessing, or bulk metadata changes.

Risk: A broad Paperless-ngx API token could expose sensitive or business-critical documents.

Mitigation: Use the narrowest available API token and review the skill before installing it for sensitive document repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oskarstark/skills/paperless-ngx)
- [Publisher profile](https://clawhub.ai/user/oskarstark)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
