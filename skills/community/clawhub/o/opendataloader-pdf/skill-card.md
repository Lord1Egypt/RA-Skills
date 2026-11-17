## Description:

Use this skill when parsing PDFs for RAG pipelines, extracting structured data from PDFs, or converting PDFs to Markdown, JSON, or HTML with bounding boxes for AI processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emptyguo](https://clawhub.ai/user/emptyguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers building RAG or document-processing pipelines use this skill to install and run OpenDataLoader PDF, choose the appropriate processing mode, and convert PDFs into AI-ready Markdown, JSON, or HTML outputs with element metadata and bounding boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing parser packages and processing untrusted PDFs expands the file-processing and dependency surface.

Mitigation: Install only trusted, pinned packages in a locked environment and process sensitive or untrusted PDFs in a least-privileged workspace.

Risk: Optional OCR and hybrid modes add runtime dependencies beyond the default local parser path.

Mitigation: Enable hybrid or OCR modes only when needed and isolate those dependencies from unrelated workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emptyguo/skills/opendataloader-pdf)
- [OpenDataLoader PDF repository](https://github.com/opendataloader-project/opendataloader-pdf)
- [OpenDataLoader quick start](https://opendataloader.org/docs/quick-start-python)
- [OpenDataLoader hybrid mode guide](https://opendataloader.org/docs/hybrid-mode)
- [OpenDataLoader JSON schema](https://opendataloader.org/docs/json-schema)
- [LangChain OpenDataLoader PDF integration](https://docs.langchain.com/oss/python/integrations/document_loaders/opendataloader_pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python, Node.js, CLI, hybrid mode, OCR, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
