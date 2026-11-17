## Description:

Ima Notes Toolkit helps agents use the IMA OpenAPI to manage personal notes and knowledge-base content, including search, browsing, note creation, note appends, file uploads, webpage imports, and knowledge-base lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to their own IMA account for personal note management and knowledge-base operations. It is suited for workflows that need authenticated IMA note search, note writing, document upload, webpage import, and knowledge-base retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify private IMA notes and knowledge-base content.

Mitigation: Confirm the user's intent and target note or knowledge base before any read, append, create, upload, import, or linking operation.

Risk: Persistent IMA credentials and temporary upload credentials could expose account access if mishandled.

Mitigation: Store credentials with strict file permissions, send them only to ima.qq.com as required by the artifact, and avoid logging credential values or temporary COS credentials.

Risk: Bundled debug scripts may expose account identifiers, private note data, or credential-handling details.

Mitigation: Review before installing, avoid running the debug scripts in normal use, and remove them when they are not needed.

Risk: Appending to existing notes and uploading to a knowledge base can be hard to reverse.

Mitigation: Require clear user confirmation for ambiguous append requests, duplicate file handling, and the exact destination knowledge base before writing or uploading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruiyongwang/skills/ima-notes-toolkit)
- [IMA homepage](https://ima.qq.com)
- [IMA OpenAPI credentials page](https://ima.qq.com/agent-interface)
- [Knowledge Base API reference](artifact/knowledge-base/references/api.md)
- [Notes API reference](artifact/notes/references/api.md)
- [Tencent Cloud COS request signature reference](https://cloud.tencent.com/document/product/436/7778)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Markdown]

**Output Format:** [Markdown guidance with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces authenticated IMA API call guidance and user-facing summaries; requires user-provided IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter and auto changelog mention 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
