## Description:

Converts parcel boundaries into OvitalMap-compatible CSV files, assigns stable parcel codes, and maintains deduplicated country and master archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeromeex](https://clawhub.ai/user/jeromeex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, survey operations teams, and land-record workflows use this skill to convert confirmed WGS84, DMS, or UTM parcel coordinates into OvitalMap boundary or vertex CSV exports while preserving parcel codes and local archives. It is not cadastral or legal validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted provider names or notes can be persisted into generated CSV archives in a form spreadsheet software may interpret as formulas.

Mitigation: Review and sanitize provider-supplied text before opening generated CSVs in spreadsheet software; keep generated exports in a dedicated workspace.

Risk: The skill creates and updates local CSV exports, country archives, master archives, and backups.

Mitigation: Set OVITALMAP_WORKSPACE to a dedicated folder and review coordinates, country codes, provider names, and parcel codes before approving writes.

## Reference(s):

- [OvitalMap Parcel CSV on ClawHub](https://clawhub.ai/jeromeex/skills/ovitalmap-parcel-csv)
- [CSV Compatibility Contract](references/csv-contract.md)
- [Workflow Contract](references/workflow-contract.md)
- [Interaction and Edge Cases](references/interaction-and-edge-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, CSV files]

**Output Format:** [Markdown guidance with JSON stdin examples and generated UTF-8 CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; OVITALMAP_WORKSPACE can be set to a dedicated folder for generated exports and archives.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
