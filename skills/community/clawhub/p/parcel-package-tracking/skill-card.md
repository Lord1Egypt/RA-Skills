## Description:

Track and add deliveries via Parcel API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to list recent or active Parcel deliveries, add package tracking records, and search supported carriers from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Parcel API key to access delivery data and add delivery records.

Mitigation: Install it only when Parcel API access is intended, store PARCEL_API_KEY securely, and rotate the key if it may have been exposed.

Risk: Tracking numbers and package descriptions are private shipment data sent to Parcel's service.

Mitigation: Avoid placing sensitive personal details in package descriptions and review outputs before sharing them.

Risk: Malformed add-command arguments can submit an incorrect delivery record.

Mitigation: Confirm tracking number, carrier code, and description before running the add command, especially when automation fills those values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/parcel-package-tracking)
- [Parcel Web](https://web.parcelapp.net)
- [Parcel external API](https://api.parcel.app/external)
- [Parcel supported carriers](https://api.parcel.app/external/supported_carriers.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Plain text CLI output and guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARCEL_API_KEY and sends tracking numbers and package descriptions to Parcel's external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
