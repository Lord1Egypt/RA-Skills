## Description: <br>
Eagle Doc helps agents use the Eagle Doc connector through OOMOL's oo CLI for usage reporting, quota checks, request logs, and Finance OCR document processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Eagle Doc through an OOMOL-connected account, including usage and quota reporting, request log review, and structured Finance OCR extraction from selected invoices, receipts, and PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Eagle Doc account and uses sensitive credentials through the connector. <br>
Mitigation: Install it only when comfortable connecting OOMOL to Eagle Doc, and use the OOMOL auth and connection flow without exposing raw API tokens. <br>
Risk: Finance OCR processing sends selected invoices, receipts, or PDFs to Eagle Doc. <br>
Mitigation: Process only documents intended for upload and confirm the target document before running OCR. <br>
Risk: Usage, quota, and request-log actions can expose account activity or billing-related information. <br>
Mitigation: Request only the reporting data needed for the task and avoid sharing returned logs outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-eagle-doc) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Eagle Doc APIs](https://www.eagle-doc.com/en/products/eagle-doc-apis/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action calls; selected invoices, receipts, or PDFs may be uploaded for OCR.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
