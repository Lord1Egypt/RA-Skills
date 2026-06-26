## Description: <br>
Convert unstructured documents into LLM-ready structured data. Supports PDF, Word, PPT, and images; extracts paragraphs, formulas, tables, charts, and other elements in one step; generates up to 8 levels of headings; and outputs Markdown organized in reading order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sube-py](https://clawhub.ai/user/sube-py) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to convert local PDF, Word, PPT, image, or similar documents into Markdown through the PaodingAI/PDRouter PDFlux service. It is suitable when downstream work needs parsed document text, tables, or selected fields for summarization, comparison, validation, retrieval, or question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to PaodingAI/PDRouter for processing. <br>
Mitigation: Use the skill only for documents whose sensitivity is acceptable under the provider's terms and your data-handling requirements. <br>
Risk: The PD_ROUTER_API_KEY is required for authentication. <br>
Mitigation: Keep the API key private, provide it through the environment, and avoid printing or committing it. <br>
Risk: Supply-chain control depends on the installed release source. <br>
Mitigation: Prefer a reviewed or pinned install source when deploying the skill in controlled environments. <br>


## Reference(s): <br>
- [PDFlux Test on ClawHub](https://clawhub.ai/sube-py/pdflux-test) <br>
- [PDRouter Platform](https://platform.paodingai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files, shell commands, guidance] <br>
**Output Format:** [Markdown printed to stdout and optionally written to a user-provided Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and PD_ROUTER_API_KEY; optional PDFLUX_INCLUDE_IMAGES can include image data in Markdown output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
