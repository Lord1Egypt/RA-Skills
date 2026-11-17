## Description:

Extract PDF content to Markdown using MinerU API. Supports formulas, tables, OCR. Provides both local file and online URL parsing methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-i-r](https://clawhub.ai/user/a-i-r)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to submit local or online PDFs to the MinerU API and retrieve structured extraction results, especially Markdown with extracted images and layout/content JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs, URLs, document metadata, and extracted results are sent through MinerU-controlled services.

Mitigation: Use the skill only for documents approved for third-party processing, and avoid sensitive or regulated content unless that use is explicitly approved.

Risk: The scripts require a MinerU API token and can use MINERU_BASE_URL from the environment.

Mitigation: Use a dedicated low-privilege MinerU token, store it in environment variables, and set MINERU_BASE_URL only from a trusted shell or leave it at the documented default.

Risk: The skill downloads and extracts remote ZIP results.

Mitigation: Run extraction in a controlled working directory and inspect downloaded ZIP contents before trusting generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a-i-r/skills/mineru-pdf-extractor)
- [MinerU Official Site](https://mineru.net/)
- [MinerU API Documentation](https://mineru.net/apiManage/docs)
- [Local File Parsing Guide](docs/Local_File_Parsing_Guide.md)
- [Online URL Parsing Guide](docs/Online_URL_Parsing_Guide.md)

## Skill Output:

**Output Type(s):** [markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands that produce extracted Markdown, images, content JSON, and layout JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MinerU token and network access to MinerU-controlled services; local-file parsing uploads PDFs, while online parsing submits public PDF URLs.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
