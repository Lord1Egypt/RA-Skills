## Description: <br>
Run speed tests to multiple endpoints, log results, and detect ISP throttling patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Consumers, support-focused users, and network engineers use this skill to collect repeated multi-endpoint speed measurements, analyze peak/off-peak and CDN differences, and generate evidence reports for ISP support conversations or plan decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs active bandwidth tests that download and upload data to configured endpoints. <br>
Mitigation: Review endpoint URLs, byte limits, timeouts, and any cron or launchd schedule before running, especially on metered or constrained connections. <br>
Risk: Local logs and reports retain timestamps and network performance history. <br>
Mitigation: Limit, rotate, or delete the ~/.isp-throttle-detective log and report directory when that history should not be retained. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Example Configuration](assets/config.example.json) <br>
- [ClawHub Release Page](https://clawhub.ai/newageinvestments25-byte/isp-throttle-detective) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local JSONL logs, machine-readable JSON summaries, and Markdown evidence reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
