## Description: <br>
Personal knowledge base for PDFs, papers, and documents with cross-document Q&A and concept retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WIREC-yzx](https://clawhub.ai/user/WIREC-yzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-heavy users use this skill to ingest local PDFs, search stored document text, and summarize concepts across a personal knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ingest workflow can store extracted PDF text and source paths persistently in plaintext. <br>
Mitigation: Set KB_ROOT deliberately, treat the knowledge base directory as sensitive local storage, and delete it when retained documents are no longer needed. <br>
Risk: The ingest script has an unsafe fallback path when used with untrusted filenames or folders, especially on systems without pdftotext. <br>
Mitigation: Review or patch scripts/ingest.sh before using it with untrusted inputs. <br>


## Reference(s): <br>
- [Knowledge Base Index Schema](references/schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/WIREC-yzx/private-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and local text or JSON files created by scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores extracted document text and metadata locally under the configured knowledge base root.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
