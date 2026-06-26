## Description: <br>
Word document manipulation with python-docx - handling split placeholders, headers/footers, nested tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows use this skill to implement reliable DOCX template filling for offer letters and other Word documents. It guides replacement of placeholders across document bodies, headers, footers, nested tables, and conditional sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted DOCX templates or JSON data can carry unexpected content or sensitive personal information into generated documents. <br>
Mitigation: Use trusted templates and data files, and review generated documents before sharing. <br>
Risk: Replacing placeholders by rebuilding runs can flatten run-level formatting around matched text. <br>
Mitigation: Test representative templates, including headers, footers, nested tables, and formatted placeholders, before using the workflow for production documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/offer-letter-generator-docx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for python-docx workflows; generated documents should be reviewed before sharing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
