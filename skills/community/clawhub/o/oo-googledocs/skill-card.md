## Description: <br>
Google Docs (workspace.google.com). Use this skill for Google Docs requests, including reading, creating, updating, and deleting document data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, read, create, export, and edit Google Docs through an OOMOL-connected account. It is suited for document automation workflows where the agent should inspect live action schemas before running read, write, or destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Google Docs through Maton-managed OAuth and may read or modify connected documents. <br>
Mitigation: Install only for intended Google Docs accounts, use the narrowest suitable connection, and confirm account selection and document IDs before use. <br>
Risk: Write and destructive actions can create, overwrite, or remove document content and document structures. <br>
Mitigation: Review the exact action, target document, and JSON payload with the user before running write or destructive operations. <br>
Risk: Connector commands depend on the live action schema and current account connection state. <br>
Mitigation: Inspect the action schema before constructing payloads and use setup or reconnection steps only after an auth, scope, connection, or billing error occurs. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Google Docs](https://workspace.google.com/products/docs/) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return connector JSON responses, document metadata, plaintext document content, PDF export results, or guidance for confirming write and destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
