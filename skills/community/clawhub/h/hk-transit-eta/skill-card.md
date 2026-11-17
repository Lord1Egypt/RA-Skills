## Description:

Queries Hong Kong bus and MTR heavy rail arrival estimates from Cantonese, Chinese, or English transit questions using official KMB/LWB, Citybus, and MTR open-data endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong bus and MTR arrival questions from route, stop, station, or direction details in Cantonese, Chinese, or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python script makes live outbound requests to disclosed Hong Kong public transport data services.

Mitigation: Install only where outbound requests to the KMB/LWB, Citybus, and MTR endpoints are acceptable, and review script and network permissions before use.

Risk: Arrival estimates can be unavailable, delayed, or ambiguous when public data services return no ETA or when user prompts identify broad areas or interchange stations.

Mitigation: Have the agent state uncertainty, list multiple matches, and ask for a more specific route, stop, station, or direction when needed.

## Reference(s):

- [KMB/LWB ETA API](https://data.etabus.gov.hk/v1/transport/kmb)
- [Citybus Real-Time API](https://rt.data.gov.hk/v2/transport/citybus)
- [MTR Schedule API](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station})
- [MTR Lines and Stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Concise natural-language transit ETA summaries, with optional JSON output from the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live public transport data and may return multiple matches when a route, stop, station, or direction is ambiguous.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
