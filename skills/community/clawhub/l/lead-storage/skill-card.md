## Description: <br>
Persists validated lead records to write-only storage after supervisor confirmation, preserving normalized location, record type, and priority fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and business teams use this skill at the end of a supervised lead workflow to save approved real-estate lead records to Google Sheets or a database without parsing or self-approving new leads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured destination or over-broad credential could write approved leads to the wrong sheet or database. <br>
Mitigation: Confirm the exact storage destination before installation and use least-privilege credentials scoped only to that destination. <br>
Risk: Lead records could be saved without the intended review if confirmation tokens are issued too broadly. <br>
Mitigation: Use a trusted supervisor workflow to issue confirmation tokens only for the specific leads being saved and reject missing or invalid tokens. <br>


## Reference(s): <br>
- [Lead Storage ClawHub Page](https://clawhub.ai/vishalgojha/lead-storage) <br>
- [LeadStorageInput schema](references/storage-input.schema.json) <br>
- [LeadStorageOutput schema](references/storage-output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON status object matching references/storage-output.schema.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a non-empty confirmation_token; returns stored_ids on success and error_message on failure.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
