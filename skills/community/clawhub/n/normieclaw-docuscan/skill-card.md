## Description: <br>
DocuScan turns photos of receipts, contracts, whiteboards, handwritten notes, and tables into reconstructed, searchable documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use DocuScan to extract, reconstruct, and save document content from images as searchable PDFs, Markdown, or plain text. It is suited for receipts, contracts, handwritten notes, whiteboards, spreadsheets, and multi-page document scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes security-verification and privacy claims that the server security evidence marks as unsupported. <br>
Mitigation: Treat those claims as unverified, review the skill before installation, and make an independent decision about whether its handling of documents fits the intended use. <br>
Risk: Document images and extracted text may contain sensitive financial, medical, legal, or personal information. <br>
Mitigation: Use the skill only if sending images through the configured AI provider and storing extracted text locally is acceptable for the documents being scanned. <br>
Risk: Generated filenames are derived from document content and may be unsafe or misleading if not reviewed. <br>
Mitigation: Review generated filenames before saving and keep outputs confined to the local documents directory. <br>
Risk: The optional dashboard can expose scanned documents and extracted text if deployed without access controls. <br>
Mitigation: Use authentication, private storage, encryption, row-level access controls, and environment variables before deploying any dashboard. <br>
Risk: PDF generation depends on Playwright and Chromium running locally. <br>
Mitigation: Install Playwright and Chromium from trusted sources and keep the documents directory private. <br>


## Reference(s): <br>
- [DocuScan ClawHub release page](https://clawhub.ai/nollio/normieclaw-docuscan) <br>
- [README](artifact/README.md) <br>
- [Security Guidance](artifact/SECURITY.md) <br>
- [PDF Templates](artifact/config/pdf-templates.md) <br>
- [Dashboard Companion Kit](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, generated local PDF files, optional plain text, and scan metadata JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be saved under a local documents directory and may include extracted document text, filenames, PDF paths, tags, and scan-log metadata.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
