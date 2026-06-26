## Description: <br>
Operates Kdocs and WPS Cloud documents through kdocs-cli, including creating, reading, editing, searching, sharing, organizing, summarizing, translating, generating presentations, processing PDFs, and managing knowledge-base content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kdocs-app](https://clawhub.ai/user/kdocs-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to automate cloud-document workflows in Kdocs and WPS Cloud, including file creation, retrieval, edits, sharing, form generation, spreadsheet work, PDF handling, presentations, web clipping, and knowledge organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive a local CLI with broad authority over cloud documents, including reading, writing, sharing, organizing, overwriting, deleting, and saving web content. <br>
Mitigation: Install only from a trusted Kdocs publisher and require explicit user confirmation before public links, webhooks, public knowledge bases, comments, overwrites, deletes, or automatic webpage saving. <br>
Risk: Authentication token handling can expose sensitive credentials if tokens are pasted into chat, logs, command output, comments, or files. <br>
Mitigation: Prefer browser or device login and store tokens only through kdocs-cli authentication commands backed by the system keychain. <br>
Risk: The release includes install, upgrade, and self-update behavior that changes local tooling. <br>
Mitigation: Review install and upgrade behavior before execution, use the documented rollback path when upgrades fail, and keep human review in place because the security verdict is suspicious. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kdocs-app/kdocs-skill) <br>
- [Kdocs latest](https://www.kdocs.cn/latest) <br>
- [Authentication](references/auth.md) <br>
- [File locating guide](references/file-locating-guide.md) <br>
- [Drive operations](references/drive.md) <br>
- [Smart document operations](references/otl.md) <br>
- [Spreadsheet operations](references/sheet.md) <br>
- [Multidimensional table operations](references/dbsheet.md) <br>
- [Form operations](references/form.md) <br>
- [PDF operations](references/pdf.md) <br>
- [Word document operations](references/wps.md) <br>
- [Presentation operations](references/wpp.md) <br>
- [AI presentation generation](references/aippt.md) <br>
- [Knowledge-base operations](references/kwiki.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON payload examples, and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local CLI commands and cloud-document links after successful creation or retrieval.] <br>

## Skill Version(s): <br>
2.5.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
