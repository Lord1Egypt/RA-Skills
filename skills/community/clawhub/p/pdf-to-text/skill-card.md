## Description: <br>
Extract plain text from PDF documents using the MinerU API and mineru-open-api CLI, including quick extraction for native PDFs and OCR-oriented extraction for scanned or image-based PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and knowledge workers use this skill to convert PDFs into readable text or Markdown for indexing, text mining, data processing, and NLP preprocessing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents may be sent to MinerU during extraction, which can expose confidential document text to an external service. <br>
Mitigation: Review MinerU handling requirements before use and avoid processing confidential PDFs unless that external handling is acceptable. <br>
Risk: Saved extraction output can retain sensitive text on disk. <br>
Mitigation: Prefer stdout when persistent files are not needed and delete output folders that contain sensitive extracted text. <br>
Risk: The workflow depends on the mineru-open-api package and CLI behavior. <br>
Mitigation: Review the package before installation and keep extraction commands scoped to trusted PDF inputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/veeicwgy/pdf-to-text) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Plain text or Markdown emitted to stdout or saved in an output directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flash extraction for smaller native PDFs and OCR extraction for scanned or image-based PDFs; batch mode writes to an output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
