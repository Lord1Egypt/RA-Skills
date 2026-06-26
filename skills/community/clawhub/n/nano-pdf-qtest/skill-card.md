## Description: <br>
Edit PDFs with natural-language instructions using the nano-pdf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinqdw](https://clawhub.ai/user/qinqdw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document editors use this skill to invoke the nano-pdf CLI for natural-language edits to a selected PDF page and review the generated output before sharing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page images, prompts, document text, or style-reference pages may be sent to Google Gemini. <br>
Mitigation: Use the skill only with documents approved for that provider workflow, especially when handling private, regulated, or business-sensitive PDFs. <br>
Risk: Google Search may be enabled by the underlying tool unless disabled. <br>
Mitigation: Disable search in the tool options when confidentiality, data minimization, or deterministic behavior is required. <br>
Risk: The installed package and source need verification before execution. <br>
Mitigation: Verify the nano-pdf PyPI package, source, and Gemini API key requirements before installing or running the CLI. <br>
Risk: PDF page numbering can vary by tool version or configuration, which may edit the wrong page. <br>
Mitigation: Check the output PDF before sharing it and retry with the alternate page numbering convention if the edit is off by one. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qinqdw/nano-pdf-qtest) <br>
- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nano-pdf CLI binary from the nano-pdf package.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
