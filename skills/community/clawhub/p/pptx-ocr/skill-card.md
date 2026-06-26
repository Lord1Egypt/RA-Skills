## Description: <br>
Pptx Ocr helps agents extract OCR text from PowerPoint (.pptx) presentations with scanned or image-embedded slide content using MinerU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and run MinerU OCR extraction for image-heavy, scanned, or screenshot-based PowerPoint presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint content may be processed by an external MinerU/OpenDataLab service. <br>
Mitigation: Do not process confidential presentations unless the service privacy, retention, and compliance terms are acceptable for the intended use. <br>
Risk: The OCR workflow requires a MINERU_TOKEN credential. <br>
Mitigation: Use a minimally scoped token when available, keep it out of logs and shared files, and configure it through the declared authentication flow or environment variable. <br>
Risk: Installing or invoking an unexpected package could change the trust boundary of the workflow. <br>
Mitigation: Install only the declared mineru-open-api package or the declared Go source, and test first with non-sensitive files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/pptx-ocr) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mineru-open-api with local .pptx files or presentation URLs, a MINERU_TOKEN credential, optional language hints, optional page ranges, and output directories.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
