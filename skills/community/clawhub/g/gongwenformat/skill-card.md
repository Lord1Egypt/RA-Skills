## Description: <br>
Format, review, or rewrite Chinese official documents according to the requirements in GB/T 9704-2012 and the local file `公文标准格式.doc`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johamwon](https://clawhub.ai/user/johamwon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and document-preparation agents use this skill to check, rewrite, or format Chinese official documents, including notices, reports, requests, replies, letters, meeting minutes, and orders. It can also produce a Word/WPS formatting checklist when direct binary editing is not practical. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled converter can silently replace the document title or omit later content. <br>
Mitigation: Run scripts only on copies, provide an explicit title, use a fresh output filename, and compare the result against the source before relying on it. <br>
Risk: Generated formatting guidance or DOCX output may still require human judgment for official-document compliance. <br>
Mitigation: Review the final document against the bundled formatting guidelines and resolve any missing metadata such as document number, signatory, seal, copied units, or issuance date. <br>


## Reference(s): <br>
- [Gongwen Formatting Guidelines](references/formatting_guidelines.md) <br>
- [ClawHub release page](https://clawhub.ai/johamwon/gongwenformat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, normalized document text, checklist items, and optional DOCX output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve factual content, flag missing document metadata, and identify assumptions or manual Word/WPS steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
