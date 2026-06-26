## Description: <br>
Use when parsing PDFs for RAG pipelines, extracting structured data from PDFs, or converting PDFs to Markdown/JSON with bounding boxes for AI processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emptyguo](https://clawhub.ai/user/emptyguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to parse PDFs for RAG pipelines, extract structured content, and convert documents to Markdown, JSON, or HTML with page and bounding-box metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing unpinned external Python or npm packages can expose production workflows to unexpected package changes. <br>
Mitigation: Verify package sources before installation and pin package versions in production environments. <br>
Risk: Extracted Markdown, JSON, or HTML can contain sensitive text from source PDFs. <br>
Mitigation: Process only intended documents and handle generated outputs with the same sensitivity controls as the original PDFs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emptyguo/opendataloader-pdf) <br>
- [OpenDataLoader PDF GitHub Repository](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [OpenDataLoader Quick Start](https://opendataloader.org/docs/quick-start-python) <br>
- [OpenDataLoader Hybrid Mode Guide](https://opendataloader.org/docs/hybrid-mode) <br>
- [OpenDataLoader JSON Schema](https://opendataloader.org/docs/json-schema) <br>
- [LangChain OpenDataLoader PDF Integration](https://docs.langchain.com/oss/python/integrations/document_loaders/opendataloader_pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with shell commands and Python or TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of OpenDataLoader PDF outputs such as Markdown, JSON, HTML, bounding boxes, page numbers, and extracted element metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
