## Description: <br>
Use when parsing PDFs, DOCX, PPTX, XLSX, or images locally, with support for text extraction, JSON output with bounding boxes, batch processing, and page screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to parse local documents into text, structured JSON, or page screenshots for downstream review and processing without cloud or LLM dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the local parser through Homebrew can depend on the resolved package source. <br>
Mitigation: Verify the Homebrew package source before installation. <br>
Risk: Batch parsing broad directories can create local output files containing extracted sensitive document content. <br>
Mitigation: Limit input directories to intended documents and protect generated output files according to the document sensitivity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ricanwarfare/liteparse-docs) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct local commands that write parsed text, JSON, or screenshots to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
