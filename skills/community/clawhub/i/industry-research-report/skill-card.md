## Description: <br>
Generates industry research reports for a requested industry using the Eastmoney data service and saves report files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts and external users use this skill to turn a natural-language industry topic into a structured research report with a preview, PDF/DOCX attachments, and a share link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the requested industry topic to the Eastmoney API under the configured EM_API_KEY. <br>
Mitigation: Use a dedicated API key, keep it in environment variables, and avoid including confidential business details in prompts. <br>
Risk: The skill writes generated PDF and DOCX report files locally. <br>
Mitigation: Set an appropriate output directory and confirm it is writable and suitable for the report contents. <br>
Risk: The service may return an external share link for the generated report. <br>
Mitigation: Open returned links only in trusted network environments and check the destination before sharing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown response with report preview text, local PDF/DOCX file paths, and a share URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and may write generated report files to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
