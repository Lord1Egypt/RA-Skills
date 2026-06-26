## Description: <br>
Query Hong Kong bus ETA/stop data and MTR heavy rail ETA from natural-language transport questions using official KMB/LWB, Citybus, and MTR open-data endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer Hong Kong public transport ETA questions in Cantonese, Chinese, or English by running a bundled helper script against official bus and MTR open-data endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make network requests to public transport APIs when answering ETA questions. <br>
Mitigation: Run it only in environments where outbound requests to the documented transport endpoints are expected. <br>
Risk: Nearest-stop matching can use exact live location coordinates. <br>
Mitigation: Share precise location only when nearest-stop matching is needed for the query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimpang8/jim-hk-bus-eta) <br>
- [KMB/LWB ETA open-data endpoint](https://data.etabus.gov.hk/v1/transport/kmb) <br>
- [Citybus ETA open-data endpoint](https://rt.data.gov.hk/v2/transport/citybus) <br>
- [MTR schedule open-data endpoint](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station}) <br>
- [MTR lines and stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Concise natural-language transit ETA answers, optional JSON, and shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stop or station names, selected operator or line, direction, ETA timing, platform details, and clarification prompts when a query is ambiguous.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
