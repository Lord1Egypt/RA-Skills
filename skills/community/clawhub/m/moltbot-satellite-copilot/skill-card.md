## Description: <br>
Predict satellite passes for NOAA APT, METEOR LRPT, and ISS over a configured latitude and longitude, then send WhatsApp alerts with manual dish alignment details and optional SDR capture/decode hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davestarling](https://clawhub.ai/user/davestarling) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and SDR operators use this skill to configure a local satellite-pass scheduler, receive WhatsApp pass alerts, and prepare optional Raspberry Pi capture and Jetson/SatDump decode workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron scheduling can repeatedly send alerts or run local workflow steps if the configuration is wrong. <br>
Mitigation: Review the observer location, satellite list, alert lead time, repeat interval, and WhatsApp target before enabling the cron entry. <br>
Risk: The pass predictor depends on external TLE data over the network, so stale or unavailable TLE data can affect pass timing. <br>
Mitigation: Confirm dependency sources and TLE/network behavior before relying on the scheduler for operational reception windows. <br>
Risk: Optional capture and decode hooks can execute configured commands with the local user's privileges. <br>
Mitigation: Leave capture and decode hooks disabled unless the commands are written or fully trusted by the operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davestarling/moltbot-satellite-copilot) <br>
- [Publisher profile](https://clawhub.ai/user/davestarling) <br>
- [TLE API endpoint used by the pass predictor](https://tle.ivanstanojevic.me/api/tle/${norad}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and JSONL pass-prediction output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes local scheduler state and per-pass run metadata when configured and enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
