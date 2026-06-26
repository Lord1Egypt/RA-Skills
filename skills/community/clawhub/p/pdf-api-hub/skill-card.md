## Description: <br>
Provides reference material and examples for integrating with PDF API Hub REST APIs for document automation, including HTML or URL to PDF conversion, PDF operations, OCR, watermarking, signing, and file management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a concise reference when building integrations with PDF API Hub for HTML-to-PDF generation, document conversion, OCR, PDF editing, signing, and related file workflows. It supplies endpoint contracts, authentication notes, error handling guidance, and code examples without executing API calls itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF API Hub processes documents and URLs outside the local environment, which can expose confidential PDFs, internal URLs, customer data, signatures, or passwords if used without approval. <br>
Mitigation: Use approved data only, review the service's retention and deletion terms, and avoid sending sensitive documents or secrets unless the external data flow is authorized. <br>
Risk: The API requires a CLIENT-API-KEY, and examples could be adapted in ways that hardcode or expose credentials. <br>
Mitigation: Store API keys outside source code, preferably in environment variables or a secrets manager, and review generated code before use. <br>
Risk: Delete-file and delete-template operations can remove remote resources. <br>
Mitigation: Require explicit user confirmation before implementing calls to deleteFile or deleteTemplate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/pdf-api-hub) <br>
- [PDF API Hub homepage](https://pdfapihub.com/) <br>
- [PDF API Hub documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub signup](https://pdfapihub.com/signup) <br>
- [Endpoint reference](endpoints.md) <br>
- [Code examples](examples.md) <br>
- [Advanced workflows](advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API reference tables and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may include API request patterns but the skill does not execute API calls or store credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
