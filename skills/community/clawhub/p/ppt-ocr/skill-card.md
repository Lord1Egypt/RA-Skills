## Description: <br>
OCR for PowerPoint presentations with scanned or image-embedded slides, using MinerU to extract image-based presentation content into readable Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to OCR legacy, scanned, or image-heavy PowerPoint files and convert extracted slide content into searchable text or Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide decks and URLs processed through mineru-open-api may be sent to an external OCR service. <br>
Mitigation: Avoid confidential or regulated presentations unless MinerU is approved for that data and use case. <br>
Risk: The MINERU_TOKEN credential is required for extraction and could grant access to MinerU API usage. <br>
Mitigation: Store MINERU_TOKEN in approved secret storage, avoid committing it to files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [ClawHub skill page](https://clawhub.ai/mzlzyca/ppt-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/mzlzyca) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted OCR output to a chosen output directory when the MinerU CLI is run with -o.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
