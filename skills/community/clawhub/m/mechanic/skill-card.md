## Description:

Mechanic helps agents track vehicle maintenance, service intervals, mileage, fuel economy, costs, warranties, recalls, and related reminders across cars, trucks, motorcycles, RVs, ATVs, boats, and other vehicles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottfo](https://clawhub.ai/user/scottfo)

### License/Terms of Use:

MIT

## Use Case:

External users and vehicle owners use this skill to maintain vehicle records, research service schedules, monitor recalls and warranties, estimate maintenance costs, and receive reminders for upcoming or overdue service. It is suitable for agents helping users organize maintenance decisions, but users should verify safety-critical repair advice with qualified mechanics or official manufacturer sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores vehicle history, VINs, insurance policy details, warranty data, fuel logs, provider history, and business-use expense information in workspace files.

Mitigation: Use it only in a private workspace, store only information needed for maintenance workflows, avoid full insurance policy numbers unless emergency-card access is required, and restrict file access.

Risk: VIN decode and recall checks may send VINs or vehicle identifiers to NHTSA services.

Mitigation: Confirm that the user is comfortable with NHTSA lookups before running VIN decode or recall checks, and skip or disable those workflows when the user does not want external lookup.

Risk: The skill can create recurring weekly check-ins and monthly recall checks.

Mitigation: Review the cron configuration before enabling it, document how to disable it, and remove the job when the skill or tracked vehicle data is no longer needed.

## Reference(s):

- [Mechanic on ClawHub](https://clawhub.ai/scottfo/skills/mechanic)
- [NHTSA VPIC VIN Decoder API](https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json)
- [NHTSA Recalls by Vehicle API](https://api.nhtsa.dot.gov/recalls/recallsByVehicle?make=Ford&model=F-350&modelYear=2021)
- [NHTSA Recalls by VIN API](https://api.nhtsa.dot.gov/recalls/recallsByVin?vin=XXXXX)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data structures, service summaries, checklists, and optional shell or cron setup instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace vehicle state, schedule files, service records, and recurring check-in configuration when requested by the user.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
