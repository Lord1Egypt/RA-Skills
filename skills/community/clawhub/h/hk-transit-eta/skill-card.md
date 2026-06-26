## Description: <br>
Query Hong Kong bus ETA and stop data and MTR heavy rail ETA from natural-language transport questions using official KMB/LWB, Citybus, and MTR open-data endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer Hong Kong public transit ETA questions in English, Cantonese, or Chinese by resolving route, stop, station, direction, and operator details before querying official transport endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transit route, stop, station, or lookup terms are sent to official Hong Kong transport data endpoints. <br>
Mitigation: Use the skill only for transit queries that are acceptable to share with those official endpoints; avoid adding sensitive personal context that is not needed for the lookup. <br>
Risk: Live ETA results can be unavailable, ambiguous, or incomplete for broad area names, unusual natural-language phrasing, unsupported operators, or out-of-scope services. <br>
Mitigation: Report missing or ambiguous ETA data clearly, list multiple likely matches when returned, and ask for a more specific stop, station, operator, or direction before presenting certainty. <br>


## Reference(s): <br>
- [HK Transit ETA on ClawHub](https://clawhub.ai/jimpang8/hk-transit-eta) <br>
- [KMB/LWB official ETA data endpoint](https://data.etabus.gov.hk/v1/transport/kmb) <br>
- [Citybus official ETA data endpoint](https://rt.data.gov.hk/v2/transport/citybus) <br>
- [MTR official schedule endpoint](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php) <br>
- [MTR official lines and stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Concise natural-language transit ETA answers, with optional JSON output from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route, operator, direction, stop or station name, sequence, destination, ETA, minutes until arrival, platform, and clarification requests for ambiguous queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
