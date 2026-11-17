## Description:

Transfers data from PCS pages into EPBP by exporting table data to an Excel file and uploading it to EBP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shandongwill](https://clawhub.ai/user/shandongwill)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized internal operations employees or automation operators use this skill to move PCS table records into EBP through an Excel transfer workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically transfers internal operational data from PCS to EBP.

Mitigation: Run it only in the intended internal environment with authorization for both PCS export and EBP import.

Risk: The configured endpoints use plaintext HTTP.

Mitigation: Prefer HTTPS endpoints and verify the destination before allowing upload.

Risk: The generated Excel file may contain internal operational data.

Mitigation: Delete or protect the generated file after use.

Risk: Scheduled execution can repeat uploads without human review.

Mitigation: Avoid enabling cron until logging, validation, approval, and rollback procedures are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shandongwill/skills/pcs-epbp)
- [ClawHub publisher profile](https://clawhub.ai/user/shandongwill)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Terminal status text, Python execution commands, and an Excel file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates pcs_data.xlsx from PCS table rows and uploads it to the configured EBP page when run.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
