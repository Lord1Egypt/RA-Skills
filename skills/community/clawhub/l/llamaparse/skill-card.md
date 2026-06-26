## Description: <br>
Parse, extract, and analyze documents using the LlamaParse API (LlamaCloud), including PDFs, images, spreadsheets, and other documents into markdown, text, or structured data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zli484](https://clawhub.ai/user/zli484) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to parse selected documents through LlamaParse and return LLM-ready markdown, plain text, structured page items, metadata, or screenshots for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to LlamaCloud for server-side parsing. <br>
Mitigation: Use only documents approved for external processing, and do not upload regulated or confidential files unless that use is approved. <br>
Risk: The skill requires a LlamaCloud API key. <br>
Mitigation: Use a revocable key scoped for this workflow and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Batch parsing broad folders may upload unintended files. <br>
Mitigation: Review input directories and extensions before running batch jobs, and keep batches limited to the intended document set. <br>
Risk: Using latest package or parser versions can reduce reproducibility. <br>
Mitigation: Pin the llama-cloud package version and use a dated LlamaParse version for production workflows. <br>


## Reference(s): <br>
- [LlamaParse API Reference](references/api-reference.md) <br>
- [LlamaCloud homepage](https://cloud.llamaindex.ai) <br>
- [LlamaIndex API documentation](https://developers.api.llamaindex.ai/) <br>
- [LlamaIndex Cloud documentation](https://developers.llamaindex.ai/python/cloud/) <br>
- [ClawHub skill page](https://clawhub.ai/zli484/llamaparse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown, text, JSON, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell examples; helper scripts can write Markdown, plain text, and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on requested LlamaParse expand views such as markdown, text, items, metadata, or images_content_metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
