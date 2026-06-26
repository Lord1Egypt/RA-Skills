## Description: <br>
OpenClaw PDF extraction skill using OpenDataLoader. Use when the user wants to extract and process PDF content for RAG, embeddings, or coordinate-based citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[secondport](https://clawhub.ai/user/secondport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide local PDF extraction with OpenDataLoader for clean text, JSON, Markdown, RAG preparation, embeddings, OCR, table handling, and coordinate-based citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or upgrading the external opendataloader-pdf package without verification can introduce supply-chain risk. <br>
Mitigation: Install only a verified, pinned package version inside a virtual environment, container, or disposable VM, then freeze dependencies for reproducibility. <br>
Risk: PDF conversion can produce JSON or Markdown containing sensitive source-document content. <br>
Mitigation: Process only intended PDF folders and keep generated outputs private when source PDFs are sensitive. <br>
Risk: Hybrid OCR and image-description mode starts a local backend that could expose document-processing behavior if bound incorrectly. <br>
Mitigation: Bind or verify the hybrid backend as localhost-only before processing documents. <br>


## Reference(s): <br>
- [OpenDataLoader](https://opendataloader.org/) <br>
- [OpenDataLoader Documentation](https://opendataloader.org/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/secondport/pdf-extract-skill) <br>
- [Quickstart CLI](docs/quickstart-cli.md) <br>
- [Security Checklist Before Install](docs/security-before-install.md) <br>
- [Hybrid Mode + OCR](docs/hybrid-mode-ocr.md) <br>
- [RAG + Citations](docs/rag-citations.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward local PDF conversion outputs such as JSON and Markdown, with optional OCR and image-description modes.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
