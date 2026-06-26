## Description: <br>
Edit PDFs with natural-language instructions using the nano-pdf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[v585](https://clawhub.ai/user/v585) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document editors use this skill to ask an agent to edit a specific PDF page with a natural-language instruction through the nano-pdf CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page content, prompts, and related document context may be sent to Gemini, and Google Search may be used by the installed tool. <br>
Mitigation: Review before installing for confidential, regulated, client, or business-sensitive PDFs; use copies of files and disable Google Search or context features where possible. <br>
Risk: PDF edits may target the wrong page if page numbering differs between tool versions or configuration. <br>
Mitigation: Sanity-check the output PDF and retry with the alternate page number convention if the result appears off by one. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/v585/nano-pdf-cn) <br>
- [nano-pdf on PyPI](https://pypi.org/project/nano-pdf/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run nano-pdf against local PDF files and review the output PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
