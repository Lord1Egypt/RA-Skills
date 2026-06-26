## Description: <br>
Extracts text and images from PDF files and sends selected content to MiniMax models for analysis, summarization, or custom PDF-processing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghanwanghan](https://clawhub.ai/user/wanghanwanghan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract PDF text and embedded images, then analyze or summarize that content with MiniMax models. It is useful for converting PDF contents into page-level analyses or structured downstream results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF text, extracted images, and prompts may be sent to MiniMax for analysis. <br>
Mitigation: Use the skill only with PDFs whose contents are approved for MiniMax processing, and avoid confidential documents unless MiniMax's data handling terms meet your requirements. <br>
Risk: The workflow depends on a MiniMax API key and Python packages for PDF parsing, image handling, and API access. <br>
Mitigation: Use a dedicated API key where possible and review or pin the required Python dependencies before running the workflow. <br>
Risk: Large PDFs or many embedded images can increase API cost, hit rate limits, or cause timeouts. <br>
Mitigation: Batch pages, resize large images before submission, and add retry, timeout, and rate-limit handling around API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghanwanghan/pdf-processor-for-minimax) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include page-level text analysis and image analysis produced by MiniMax API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
