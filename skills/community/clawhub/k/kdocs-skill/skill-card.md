## Description: <br>
This skill helps agents operate KDocs/WPS cloud documents, including creating, reading, editing, searching, sharing, organizing, summarizing, translating, generating presentations, handling forms, and managing knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kdocs-app](https://clawhub.ai/user/kdocs-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to let an agent work with KDocs/WPS cloud documents and related office workflows, including document creation, file search, content extraction, sharing, spreadsheet work, PDF handling, form generation, and knowledge-base organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update a local kdocs-cli executable. <br>
Mitigation: Install only from trusted publisher releases, review update prompts as privileged changes, and rely on checksum verification when available. <br>
Risk: The CLI can persist account credentials and access a user's KDocs account. <br>
Mitigation: Prefer browser-based login, avoid pasting tokens into chat or logs, and revoke or rotate credentials if exposure is suspected. <br>
Risk: The skill can perform broad cloud-document actions, including sharing and public-link operations. <br>
Mitigation: Review sharing, deletion, closing, and other irreversible operations before execution, and verify write results with an independent read. <br>
Risk: Sensitive documents may be processed through cloud and AI-assisted document flows. <br>
Mitigation: Avoid using the skill on sensitive documents unless the user understands the KDocs cloud-processing path and account permissions involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kdocs-app/skills/kdocs-skill) <br>
- [Publisher profile](https://clawhub.ai/user/kdocs-app) <br>
- [KDocs homepage and token URL](https://www.kdocs.cn/latest) <br>
- [Authentication reference](references/auth.md) <br>
- [Drive reference](references/drive.md) <br>
- [File locating guide](references/file-locating-guide.md) <br>
- [Sheet reference](references/sheet.md) <br>
- [WPS document reference](references/wps.md) <br>
- [Presentation reference](references/wpp.md) <br>
- [PDF reference](references/pdf.md) <br>
- [Knowledge-base reference](references/kwiki.md) <br>
- [Form reference](references/form.md) <br>
- [AI presentation reference](references/aippt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and generated office-document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include KDocs links, CLI commands, command results, JSON request bodies, and document or spreadsheet content generated for cloud-document workflows.] <br>

## Skill Version(s): <br>
2.5.13 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
