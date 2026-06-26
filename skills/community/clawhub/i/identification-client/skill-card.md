## Description: <br>
Identifies the client and transaction direction for already analyzed accounting documents by matching invoices, bank statements, and expense reports against a local client registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting agents use this skill after document analysis to attach a document to the right client dossier and determine whether an invoice is a purchase or sale. It updates the client registry only for high-confidence identifiers and asks for human review when both sides or neither side can be matched. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect OCR or ambiguous invoice parties can attach a document to the wrong client or direction. <br>
Mitigation: Review records where confidence is not high or needs_review is true, and answer the generated accountant question before filing or downstream reconciliation. <br>
Risk: The skill can modify the local accounting client registry. <br>
Mitigation: Run it with a deliberate --clients path and review newly created or auto-validated client records before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON object added to the input dossier, with optional human-facing review question text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads an analyzed document from standard input or a file path, uses a --clients registry path, and may write confirmed client metadata to local JSON registry files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
