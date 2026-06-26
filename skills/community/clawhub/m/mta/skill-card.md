## Description: <br>
NYC MTA Transit provides real-time subway arrivals, bus predictions, service alerts, route details, stop lookup, vehicle locations, and GTFS data refresh support for the New York City subway and bus system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer NYC public transit questions, including next subway or bus arrivals, service alerts, nearby stops, route details, and live vehicle locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bus commands send the configured MTA BusTime API key to MTA endpoints. <br>
Mitigation: Use a dedicated MTA BusTime key, keep unrelated secrets out of the skill .env file, and run bus commands only when sharing that key with MTA is acceptable. <br>
Risk: Installation uses npm to install protobufjs. <br>
Mitigation: Review the package lock and install dependencies only in environments where npm dependency installation is allowed. <br>
Risk: The GTFS refresh command downloads and extracts public transit data into a local cache. <br>
Mitigation: Run refresh-gtfs intentionally and monitor the ~/.mta/gtfs cache according to local storage and cleanup policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianleach/mta) <br>
- [MTA Developer Resources](https://api.mta.info/) <br>
- [MTA BusTime API](https://bustime.mta.info/wiki/Developers/Index) <br>
- [MTA Bus API key registration](https://register.developer.obanyc.com/) <br>
- [GTFS Reference](https://gtfs.org) <br>
- [GTFS Realtime Reference](https://gtfs.org/realtime/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with transit lookup results, command examples, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bus commands require MTA_BUS_API_KEY; GTFS refresh downloads and extracts public transit data into ~/.mta/gtfs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
