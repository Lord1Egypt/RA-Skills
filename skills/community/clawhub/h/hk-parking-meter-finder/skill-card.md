## Description: <br>
Find Hong Kong roadside parking meter locations and live vacancy using official Transport Department and DATA.GOV.HK datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and agents use this skill to search official Hong Kong roadside metered parking inventory and live vacancy by street, district, station, landmark, or area phrase. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python script contacts official Hong Kong public-data endpoints during use. <br>
Mitigation: Install and run the skill only when outbound requests to those public DATA.GOV.HK endpoints are acceptable. <br>
Risk: Live parking availability depends on the completeness and freshness of official occupancy data. <br>
Mitigation: Present results as official feed status at query time and avoid treating unknown or missing occupancy values as confirmed availability. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jimpang8/hk-parking-meter-finder) <br>
- [DATA.GOV.HK](https://data.gov.hk/) <br>
- [Parking space inventory CSV](https://resource.data.one.gov.hk/td/psiparkingspaces/spaceinfo/parkingspaces.csv) <br>
- [Parking occupancy status CSV](https://resource.data.one.gov.hk/td/psiparkingspaces/occupancystatus/occupancystatus.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary or JSON results from the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes vacant, occupied, and unknown counts, approximate cluster centers, Google Maps links, and per-space status details when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
