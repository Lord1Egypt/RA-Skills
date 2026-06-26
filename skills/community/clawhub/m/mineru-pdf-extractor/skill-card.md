## Description: <br>
Extract PDF content to Markdown using MinerU API. Supports formulas, tables, OCR. Provides both local file and online URL parsing methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[A-I-R](https://clawhub.ai/user/A-I-R) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and operations teams use this skill to convert local or publicly accessible PDF documents into Markdown and extracted assets through the MinerU API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs, PDF URLs, and the MinerU API token are sent to MinerU-controlled services. <br>
Mitigation: Use the skill only with documents approved for MinerU processing, avoid confidential or regulated documents unless approved, and provide tokens through environment variables. <br>
Risk: Changing the API base URL can route documents and credentials to an untrusted service. <br>
Mitigation: Keep the default MinerU endpoint unless the alternative endpoint is explicitly trusted. <br>
Risk: Downloaded extraction results may contain files that should not be trusted blindly. <br>
Mitigation: Run the skill from a dedicated working folder and inspect extracted files before using them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/A-I-R/mineru-pdf-extractor) <br>
- [MinerU Official Site](https://mineru.net/) <br>
- [MinerU API Documentation](https://mineru.net/apiManage/docs) <br>
- [Local File Parsing Guide](docs/Local_File_Parsing_Guide.md) <br>
- [Online URL Parsing Guide](docs/Online_URL_Parsing_Guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and downloaded result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted Markdown, images, content_list.json, layout.json, and ZIP archives from MinerU API responses.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
