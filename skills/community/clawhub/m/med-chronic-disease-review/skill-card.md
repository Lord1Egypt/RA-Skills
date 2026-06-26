## Description: <br>
Reviews outpatient chronic disease records for diabetes or hypertension and returns a raw JSON review result plus a natural-language decision summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations and review teams can use this skill to prepare OCR-derived medical record text, submit diabetes or hypertension review requests, and receive decision-oriented summaries for administrative review. It is an aid for document review and does not provide medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive OCR medical text may be sent to a remote or user-selected endpoint. <br>
Mitigation: Use only de-identified records, verify the endpoint operator and privacy terms, and avoid overriding the service base URL unless the endpoint is trusted. <br>
Risk: Raw PDFs and Office files can carry parsing and document-handling risk before review. <br>
Mitigation: Prefer JSON OCR input for untrusted sources and process other file types only in a controlled environment. <br>
Risk: The default HTTP timeout can wait indefinitely. <br>
Mitigation: Set a finite timeout for operational use. <br>
Risk: Generated review outputs and prepared OCR files may contain sensitive medical information. <br>
Mitigation: Delete generated output and prepared OCR files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/med-chronic-disease-review) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON files and natural-language text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include raw review JSON, a human-readable decision summary, and optional prepared OCR JSON for debugging.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
