## Description: <br>
Track and add deliveries via Parcel API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to list recent or active Parcel deliveries, add new package tracking entries, and search supported carriers from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a Parcel API key and shipment data to Parcel API endpoints. <br>
Mitigation: Install only if comfortable sharing that data with Parcel, and rotate or remove PARCEL_API_KEY when the skill is no longer used. <br>
Risk: The add command changes the Parcel account by creating a new delivery and can request push confirmation. <br>
Mitigation: Confirm the tracking number, carrier, description, and --notify setting before running the add command. <br>


## Reference(s): <br>
- [Parcel web app](https://web.parcelapp.net) <br>
- [Parcel external API endpoint](https://api.parcel.app/external) <br>
- [Parcel supported carriers JSON](https://api.parcel.app/external/supported_carriers.json) <br>
- [ClawHub release page](https://clawhub.ai/gumadeiras/parcel-package-tracking) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARCEL_API_KEY and may print shipment descriptions, tracking numbers, status codes, expected dates, and latest delivery events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
