## Description: <br>
Google Docs API integration with managed OAuth via Maton for creating documents, reading full text, writing or appending content, search and replace, formatting text and paragraphs, and exporting documents to PDF or DOCX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate Google Docs workflows through Maton-managed OAuth, including creating, reading, editing, formatting, and exporting documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, overwrite, and export Google Docs content through Maton. <br>
Mitigation: Install only when Maton is trusted for the target documents and use append or narrow edits when possible. <br>
Risk: A wrong document ID or broad write, replace, or export command can affect unintended content. <br>
Mitigation: Verify document IDs before write, replace, or export operations and check replace counts or operation results after changes. <br>
Risk: The MATON_API_KEY grants access to routed Google Docs operations. <br>
Mitigation: Keep MATON_API_KEY out of source control, logs, and shared command histories. <br>
Risk: Exported documents may contain sensitive content. <br>
Mitigation: Avoid exporting sensitive documents to shared or temporary paths unless that location is approved. <br>


## Reference(s): <br>
- [ClawHub Google Docs skill page](https://clawhub.ai/tankeito/google-docs-operator) <br>
- [Google Docs API Overview](https://developers.google.com/workspace/docs/api/reference/rest) <br>
- [documents.get](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/get) <br>
- [documents.create](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/create) <br>
- [documents.batchUpdate](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate) <br>
- [Google Docs request types](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/request) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; CLI commands return JSON and exported document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access to Maton, Google Docs, and Google Drive APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
