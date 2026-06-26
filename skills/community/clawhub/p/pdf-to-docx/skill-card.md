## Description: <br>
PDF to DOCX converts PDF files or URLs into editable Word (.docx) documents using MinerU, with options for layout preservation, OCR, VLM mode, page ranges, and batch conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to guide PDF-to-DOCX conversion through the MinerU CLI. It is useful when a PDF must become an editable Word document while preserving layout, text, tables, images, and formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MinerU external API may receive document contents during conversion. <br>
Mitigation: Avoid converting confidential PDFs unless MinerU's document-handling terms meet the user's requirements. <br>
Risk: The skill requires a MINERU_TOKEN for authenticated MinerU CLI use. <br>
Mitigation: Configure the token through mineru-open-api auth or a protected environment variable, and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Installing mineru-open-api from an unvetted source could introduce supply-chain risk. <br>
Mitigation: Use a vetted install source and pin or review the installed package version when operating in managed environments. <br>
Risk: DOCX output cannot be streamed to stdout and conversion fails without an output directory. <br>
Mitigation: Always include -o <directory>, then review the generated DOCX file before relying on it. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [mineru-open-api Go install path](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli/mineru-open-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands; DOCX files are produced when the commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN. DOCX output must be written to a directory with -o and cannot be streamed to stdout.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
