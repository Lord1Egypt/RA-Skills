## Description: <br>
Interview a user and build a personalized health-record system around their goals, reports, and tracking needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsongra11](https://clawhub.ai/user/hsongra11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize sensitive health records into a durable local workspace with preserved raw files, readable notes, structured tracking data, and dashboard or history summaries. It supports ongoing ingestion of PDFs, screenshots, scans, wearable exports, doctor notes, and similar health materials while keeping privacy and consent decisions explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medical records and extracted health data. <br>
Mitigation: Use a private local folder by default, avoid cloud-synced storage unless intentional, and confirm storage, retention, and deletion expectations before processing files. <br>
Risk: External OCR, APIs, or cloud processing could disclose health files or extracted data. <br>
Mitigation: Keep processing local unless the user explicitly approves external processing for specific files and trusted services. <br>
Risk: Incomplete extraction or summary errors could make records misleading. <br>
Mitigation: Preserve raw files, keep summaries traceable to source paths, create recheck notes for unclear extractions, and state that outputs are not medical advice. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance, Files] <br>
**Output Format:** [Markdown notes, JSON and CSV tracking files, folder structures, and dashboard or history summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve raw source files, remain traceable to original paths, and avoid presenting extracted health content as medical advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
