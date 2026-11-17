## Description:

Lexiang Knowledge Base helps agents search, read, create, edit, upload, synchronize, and manage Lexiang knowledge-base content through a Lexiang MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Employees, developers, and knowledge workers use this skill to connect an agent to Lexiang for retrieving existing knowledge, creating or updating pages, managing drafts, comments, and smartsheets, and uploading or synchronizing user-selected files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and upload user-selected local files through the Lexiang workflow.

Mitigation: Review the exact upload destination and file list before sending files, and use dry-run plans for bulk or folder sync operations.

Risk: The skill can modify or delete knowledge-base content.

Mitigation: Require a specific user-provided URL, ID, or explicit confirmation before write, move, rename, validity, draft publish, or delete operations.

Risk: Bearer tokens or MCP credentials may be configured for the Lexiang connection.

Mitigation: Prefer connector or OAuth setup and environment-backed secrets over plaintext token storage.

Risk: Helper scripts may rely on unpinned global dependencies.

Mitigation: Run scripts in a controlled environment, inspect generated plans before execution, and avoid installing unpinned global dependencies on shared systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaoxinghua09-cell/skills/lexiang-knowledge-base)
- [Publisher Profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [Reference Index](artifact/references/index.md)
- [Setup and Authentication](artifact/references/setup.md)
- [Search and Retrieval](artifact/references/search.md)
- [Document Writing](artifact/references/writer.md)
- [File Upload Management](artifact/references/files.md)
- [Core Data Model and Safety Rules](artifact/references/base.md)
- [Helper Scripts](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool-call arguments, upload plans, dry-run sync plans, and generated Lexiang page links.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
