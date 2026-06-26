## Description: <br>
Vehicle maintenance tracker and mechanic advisor that tracks mileage, service intervals, fuel economy, costs, warranties, recalls, VIN decode data, service providers, and proactive reminders across cars, trucks, motorcycles, RVs, ATVs, boats, and other vehicles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScotTFO](https://clawhub.ai/user/ScotTFO) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and vehicle owners use this skill to maintain vehicle records, build service schedules, monitor recalls, project upcoming maintenance, and receive mechanic-oriented guidance for routine and seasonal care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle records can include sensitive VINs, mileage, service history, provider details, warranty information, and optional insurance or policy details stored in the workspace. <br>
Mitigation: Keep the data/mechanic folder private and avoid storing insurance or policy details unless they are needed. <br>
Risk: VINs or vehicle details may be sent to NHTSA for decoding and recall checks. <br>
Mitigation: Provide a VIN only when comfortable with that lookup, or use manual vehicle details when VIN-based features are not needed. <br>
Risk: The skill can set up scheduled recall and mileage checks. <br>
Mitigation: Review the weekly cron reminder and disable or adjust scheduled background checks if they are not wanted. <br>


## Reference(s): <br>
- [Mechanic ClawHub page](https://clawhub.ai/ScotTFO/mechanic) <br>
- [NHTSA VPIC VIN decoder API](https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json) <br>
- [NHTSA recalls by vehicle API](https://api.nhtsa.dot.gov/recalls/recallsByVehicle?make=Ford&model=F-350&modelYear=2021) <br>
- [NHTSA recalls by VIN API](https://api.nhtsa.dot.gov/recalls/recallsByVin?vin=XXXXX) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON vehicle records, service schedules, and optional cron setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain workspace vehicle data under data/mechanic and use public NHTSA endpoints for VIN decoding and recall checks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
