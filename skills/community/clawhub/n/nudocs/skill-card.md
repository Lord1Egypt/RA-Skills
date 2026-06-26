## Description: <br>
Upload, edit, and export documents via Nudocs.ai for collaborative document editing, shareable document links, and pulling edited content back into the agent workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-focused users use this skill to send local documents to Nudocs.ai for rich editing, retrieve shareable links, list or delete cloud documents, and pull edited files back in formats such as DOCX, Markdown, or PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload, share, download, list, and delete cloud documents using a Nudocs API key. <br>
Mitigation: Use it only with documents intended for Nudocs.ai, treat returned links as sensitive, and confirm document IDs before pull, link, or delete operations. <br>
Risk: The skill depends on local Nudocs credentials in NUDOCS_API_KEY or ~/.config/nudocs/api_key. <br>
Mitigation: Store credentials securely, avoid exposing them in prompts or shared files, and rotate the API key if it may have been disclosed. <br>


## Reference(s): <br>
- [Nudocs](https://nudocs.ai) <br>
- [Nudocs CLI](https://github.com/PSPDFKit/nudocs-cli) <br>
- [Nudocs MCP Server](https://github.com/PSPDFKit/nudocs-mcp-server) <br>
- [Document Design Reference](references/document-design.md) <br>
- [Nudocs Format Reference](references/formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jdrhyne/nudocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local files, Nudocs document IDs, downloaded document files, and shareable Nudocs.ai links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
