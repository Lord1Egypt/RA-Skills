## Description: <br>
Adds centered text watermarks to PDF documents, with automatic page-orientation-aware angle and font sizing and support for Chinese text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zss04124586](https://clawhub.ai/user/zss04124586) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People working with PDF documents use this skill to add a supplied text watermark to local PDFs, or to PDFs downloaded from a user-provided URL, before returning the watermarked file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing an untrusted PDF or URL could expose the agent environment to unsafe or unintended content. <br>
Mitigation: Use only PDFs and URLs the user intends the agent to process, and prefer trusted PDF sources. <br>
Risk: Choosing an output path that matches an existing document could overwrite a file. <br>
Mitigation: Use a distinct output filename, or rely on the default watermarked filename when appropriate. <br>
Risk: Missing or untrusted Python dependencies could prevent reliable PDF processing. <br>
Mitigation: Install pypdf and reportlab from trusted package sources before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zss04124586/pdf-watermark) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Watermarked PDF file plus concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The watermark text is user supplied; output defaults to a new PDF filename based on the input path unless the user specifies an output path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
