## Description:

Queries Hong Kong KMB/LWB, Citybus, and MTR heavy rail ETA and stop data from Cantonese, Chinese, or English transit questions using public transport open-data endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong transit ETA questions by extracting a bus route and stop, or an MTR origin and destination, then running the bundled helper script and summarizing arrival times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transit lookup details, including route numbers, station codes, stop names, and optional precise live-location coordinates, may be sent to documented public transport data services.

Mitigation: Use route, stop, or station names when sufficient; share precise live-location coordinates only when needed for nearest-stop selection.

Risk: ETA answers depend on the availability and freshness of public KMB/LWB, Citybus, and MTR open-data endpoints.

Mitigation: Present unavailable or ambiguous ETA results clearly and ask for a more specific stop, station, direction, or live location when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimpang8/skills/jim-hk-bus-eta)
- [KMB/LWB ETA API base](https://data.etabus.gov.hk/v1/transport/kmb)
- [Citybus transport data endpoint](https://rt.data.gov.hk/v2/transport/citybus)
- [MTR schedule endpoint](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station})
- [MTR lines and stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Natural-language transit ETA answers or JSON returned by a local Python command, often summarized in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operator, route, direction, stop or station candidates, ETA minutes, destination, platform, and timestamp depending on the query mode.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
