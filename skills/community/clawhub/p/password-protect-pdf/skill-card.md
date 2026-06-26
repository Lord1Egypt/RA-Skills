## Description: <br>
Add password protection to a PDF by uploading it to the Solutions API, polling until completion, then returning a download URL for the protected PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to password-protect PDF files through the Cross-Service-Solutions API and receive a download URL for the protected document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected PDF and document password to a third-party PDF-processing API. <br>
Mitigation: Use it only for PDFs and passwords that may be shared with Cross-Service-Solutions; prefer local or offline encryption for highly confidential documents. <br>
Risk: API keys and returned download URLs grant access to sensitive processing results. <br>
Mitigation: Keep the API key and returned download URL private, and avoid logging or sharing either value. <br>
Risk: A base URL override can redirect PDF content and credentials away from the default API endpoint. <br>
Mitigation: Verify any SOLUTIONS_BASE_URL or --base-url override before running the skill. <br>
Risk: Using an account password as the PDF password can expose unrelated accounts if the document password is shared with the API. <br>
Mitigation: Use a unique document password and do not reuse account passwords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/password-protect-pdf) <br>
- [CrossServiceSolutions publisher profile](https://clawhub.ai/user/CrossServiceSolutions) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Solutions API registration](https://login.cross-service-solutions.com/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command output from the bundled CLI script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns job status, job ID, download URL, file name, and raw API response data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
