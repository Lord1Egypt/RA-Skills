## Description: <br>
Pitstop helps agents answer Italy-specific fuel-station price and EV charging station lookup questions using MIMIT fuel data, OpenStreetMap Overpass, and ISTAT municipality coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galjos](https://clawhub.ai/user/galjos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Pitstop to find cheaper Italian fuel stations, compare station prices by place, brand, fuel, or coordinates, and locate nearby EV chargers. It is useful for Italy-focused travel, logistics, and route-planning assistance where daily public fuel data and public charger listings are sufficient. <br>

### Deployment Geography for Use: <br>
Italy <br>

## Known Risks and Mitigations: <br>
Risk: Fuel price data is daily public data and may not reflect live or intraday station prices. <br>
Mitigation: Tell users the data is not live and prefer recent results or freshness checks before recommending a station. <br>
Risk: EV charger results rely on public mapping services and do not include per-station kWh tariffs. <br>
Mitigation: Surface operator tariff links instead of estimating charging prices, and handle mapping service failures explicitly. <br>
Risk: The skill installs and runs an external pitstop CLI that may download or cache public datasets and call OpenStreetMap services. <br>
Mitigation: Install from the disclosed package path, review the CLI before deployment, and run it in an environment where network and cache behavior is acceptable. <br>


## Reference(s): <br>
- [Pitstop ClawHub page](https://clawhub.ai/galjos/skills/pitstop) <br>
- [Publisher profile](https://clawhub.ai/user/galjos) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON or GeoJSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents should request JSON or GeoJSON output when consuming pitstop programmatically and surface navigation or tariff links when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
