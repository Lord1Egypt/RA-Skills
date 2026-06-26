## Description: <br>
Add password protection and encryption to a PDF. Supports AES-256, AES-128, RC4-128 encryption and granular permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to call PDF API Hub to encrypt PDFs, set open and owner passwords, and control permissions such as printing, copying, modifying, annotating, form filling, extraction, and assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF content, protection passwords, and the API key are sent to pdfapihub.com for processing. <br>
Mitigation: Use only documents and credentials appropriate for that provider, and verify privacy, retention, deletion, and compliance terms before processing regulated or highly confidential PDFs. <br>
Risk: The skill requires sensitive credentials through the CLIENT-API-KEY header. <br>
Mitigation: Store the API key in a secret manager or protected environment variable and avoid embedding real credentials in prompts, examples, logs, or committed files. <br>


## Reference(s): <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/lock-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Configuration instructions, Guidance] <br>
**Output Format:** [JSON request guidance and PDF output as file, URL, or base64] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header and sends PDF content, passwords, and options to pdfapihub.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
