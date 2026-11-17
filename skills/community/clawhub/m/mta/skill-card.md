## Description:

NYC MTA Transit provides real-time subway arrivals, bus predictions, vehicle locations, service alerts, route details, stop lookup, and transit reference guidance for New York City subway and bus questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to answer NYC public transit questions, including next-train and bus arrival times, service disruptions, vehicle locations, route details, and nearby stop discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bus features use an MTA BusTime API key and the security guidance notes credential-handling concerns around unredacted error logging.

Mitigation: Use a dedicated MTA BusTime key, avoid shared or sensitive credentials, and review logs and errors for accidental key exposure before broad deployment.

Risk: Nearby bus-stop searches send latitude and longitude coordinates to MTA services.

Mitigation: Use approximate locations when exact coordinates are not needed and disclose this external request behavior to users.

Risk: The GTFS refresh command downloads and extracts a ZIP file, and the security guidance recommends ZIP validation before extraction.

Mitigation: Run refreshes only from trusted networks and prefer a version that validates archive contents before extraction.

Risk: The security guidance recommends updating protobufjs.

Mitigation: Review and update dependencies during installation or release review, then run dependency auditing appropriate for the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brianleach/skills/mta)
- [Publisher Profile](https://clawhub.ai/user/brianleach)
- [MTA Developer Resources](https://api.mta.info/)
- [MTA BusTime API](https://bustime.mta.info/wiki/Developers/Index)
- [GTFS Reference](https://gtfs.org)
- [GTFS Realtime Reference](https://gtfs.org/realtime/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text transit summaries with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subway and alert features work without credentials; bus features require MTA_BUS_API_KEY; GTFS static data may be cached locally under ~/.mta/gtfs/.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
