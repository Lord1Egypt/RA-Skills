## Description: <br>
Extract text, search inside PDFs, and produce summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyeque](https://clawhub.ai/user/iyeque) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read user-supplied PDF files, extract plain text, and inspect document metadata during document analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted PDF text and metadata may contain sensitive information. <br>
Mitigation: Run the skill only on PDFs the user intends the agent to read, and handle extracted output according to the workspace's data policy. <br>
Risk: Unpinned PyMuPDF installation can reduce reproducibility or complicate high-security deployments. <br>
Mitigation: Pin and review the PyMuPDF package version in controlled or security-sensitive environments. <br>
Risk: Encrypted PDFs that require a password will not be processed successfully by the current command interface. <br>
Mitigation: Use accessible PDF files or decrypt password-protected documents through an approved workflow before invoking the skill. <br>


## Reference(s): <br>
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io) <br>
- [ClawHub skill page](https://clawhub.ai/iyeque/iyeque-pdf-reader) <br>
- [Publisher profile](https://clawhub.ai/user/iyeque) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text for extracted PDF content or JSON for document metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The extract command can limit output by maximum page count.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
