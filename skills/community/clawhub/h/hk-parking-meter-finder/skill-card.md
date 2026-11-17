## Description:

Find Hong Kong roadside parking meter locations and live vacancy using official Transport Department / DATA.GOV.HK datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby Hong Kong roadside metered parking by street, district, landmark, or station, then summarize current vacant, occupied, and unknown counts from official datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Python script that makes outbound network requests to retrieve current parking-meter information.

Mitigation: Allow network access only to the documented DATA.GOV.HK resource endpoints when operating in restricted environments.

Risk: Live occupancy may be incomplete where the official feed lacks sensor records for some metered spaces.

Mitigation: Present unknown counts separately and avoid claiming availability for spaces without live occupancy records.

Risk: Keyword and fuzzy matching can return nearby or likely street clusters rather than an exact address match.

Mitigation: Tell users when exact streets are absent and ask for a more specific street, district, station, or landmark when needed.

## Reference(s):

- [Transport Department metered parking space inventory](https://resource.data.one.gov.hk/td/psiparkingspaces/spaceinfo/parkingspaces.csv)
- [Transport Department live parking occupancy status](https://resource.data.one.gov.hk/td/psiparkingspaces/occupancystatus/occupancystatus.csv)
- [DATA.GOV.HK](https://data.gov.hk/)
- [ClawHub skill page](https://clawhub.ai/jimpang8/skills/hk-parking-meter-finder)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes parking cluster labels, vacancy counts, approximate coordinates, Google Maps links, and occupancy timestamps when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
