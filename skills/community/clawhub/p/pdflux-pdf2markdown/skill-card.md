## Description: <br>
Convert unstructured documents into LLM-ready structured data, including Markdown from PDF, Word, PPT, and image files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paodingai](https://clawhub.ai/user/paodingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert user-selected local documents into Markdown before summarization, table extraction, field extraction, comparison, validation, knowledge retrieval, or question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads a user-selected document to the PaodingAI/PDFlux SaaS API for conversion. <br>
Mitigation: Use it only for documents the user is permitted to send to that service, and confirm account terms, data-handling requirements, and user consent before processing confidential, regulated, or customer material. <br>
Risk: Optional image output can return embedded image data and increase exposure and token usage. <br>
Mitigation: Keep image/base64 output disabled unless the task requires it, and review the exact input file and output path before running the conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paodingai/pdflux-pdf2markdown) <br>
- [PaodingAI platform](https://platform.paodingai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files] <br>
**Output Format:** [Markdown text, or JSON text when the API response does not contain Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print converted content to stdout and optionally write the same output to a file.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
