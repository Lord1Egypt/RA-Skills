## Description: <br>
Structures Chinese outpatient follow-up medical records into fine-grained JSON fields such as history, diagnosis, and treatment plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical documentation teams and developers can use this skill to convert Chinese follow-up outpatient record text into structured JSON for downstream review, data extraction, or workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical record text may be sent to an external service, and the security evidence says claimed de-identification safeguards are not implemented in code. <br>
Mitigation: Use only when authorized to send the records to that service, remove patient identifiers before processing, and verify consent, retention, and compliance controls with the publisher. <br>
Risk: PDF, Office, spreadsheet, and image inputs may require parsing or external tools that expand the risk from untrusted files. <br>
Mitigation: Process untrusted documents only in a sandboxed, low-privilege environment, or pre-convert trusted inputs to plain text or JSON before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/med-followup-record-struct) <br>
- [External structuring service endpoint](https://shangbao.yunzhisheng.cn/skills/record-struct/gen_abstract_by_his) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [UTF-8 JSON file containing fine-grained medical record fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, JSON, CSV, Excel, Word, PDF, and image-derived inputs through the unified runner; optional dependencies and tools are needed for some formats.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
