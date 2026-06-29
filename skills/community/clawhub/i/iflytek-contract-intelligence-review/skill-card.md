## Description: <br>
Reviews contracts from PDFs, images, Word documents, Markdown, or text using OCR/text extraction, clause analysis, risk detection, compliance checks, bilingual consistency checks, and Markdown or JSON reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, procurement, and operations teams use this skill to review scanned, image, bilingual, or editable contracts for clause-level risks and compliance issues. The output is a review aid and not a formal legal opinion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential contract content may be sent to the configured OCR, translation, or LLM providers. <br>
Mitigation: Use approved private or on-prem endpoints for confidential documents and confirm provider data-handling terms before use. <br>
Risk: Generated reports and optional intermediate files may contain sensitive contract text or extracted clauses. <br>
Mitigation: Write outputs only to protected directories, avoid --save-intermediate unless needed, and redact reports before sharing. <br>
Risk: Risk findings and compliance suggestions are review aids, not formal legal advice. <br>
Mitigation: Require qualified human review before relying on the output for legal or commercial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-contract-intelligence-review) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Sample review report](artifact/examples/sample_review_report.md) <br>
- [Review output JSON template](artifact/templates/review_output.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON contract review reports, with CLI commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit Markdown, JSON, or both; optional intermediate files may be saved under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
