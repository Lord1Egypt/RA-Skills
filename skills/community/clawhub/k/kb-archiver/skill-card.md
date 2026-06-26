## Description: <br>
知识库归档系统 archives local documents into a categorized knowledge base with optional AI classification, plaintext indexing, search, and statistics for common office and text formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[141553](https://clawhub.ai/user/141553) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to archive files or folders into a local knowledge base, extract searchable indexes, classify documents, and report collection statistics. It is suited for managing work documents such as spreadsheets, office files, PDFs, text files, and structured text data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The archiver can duplicate sensitive local documents and persist searchable plaintext indexes and manifests. <br>
Mitigation: Use it only on files approved for local duplication, protect the generated knowledge-base directory, and treat _index files and _manifest.json as sensitive. <br>
Risk: AI classification and optional cloud storage may send document names or content-derived text to external model or storage providers. <br>
Mitigation: Do not enable AI classification or cloud storage for confidential or regulated files unless the endpoint and storage account are trusted and credentials are narrowly scoped. <br>
Risk: The security review reports unsafe shell command construction and warns against untrusted filenames or documents. <br>
Mitigation: Review before installing or running, avoid untrusted paths and filenames, and run in a restricted environment when processing unfamiliar documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/141553/kb-archiver) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JavaScript snippets; runtime output is console text plus copied documents, plaintext index files, and a JSON manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create categorized local copies, _index text files, and _manifest.json entries; optional AI classification and cloud storage depend on user configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
