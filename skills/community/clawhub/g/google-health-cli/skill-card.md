## Description: <br>
Google Health is a read-only CLI skill that authenticates with Google Health through OAuth2, lists raw health data points and daily rollups, parses exercise sessions, and emits JSON for agents or scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stozo04](https://clawhub.ai/user/stozo04) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve Google Health data through a local, read-only CLI for analysis or workflow automation. It is intended for use only with an account owner who has knowingly consented and in environments that can handle sensitive health data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill emits sensitive personal health data, and agent or CI environments may log, persist, summarize, or forward stdout. <br>
Mitigation: Use the skill only in trusted environments, request the narrowest useful data type and date range, and avoid persisting or forwarding output beyond the immediate task. <br>
Risk: OAuth client credentials and cached tokens are sensitive local secrets. <br>
Mitigation: Keep config.json and token.json private, do not commit or share them, and rotate credentials or run auth logout if exposure is suspected. <br>
Risk: Raw read-only API access can expose profile, account, and settings data beyond typed health metrics. <br>
Mitigation: Prefer typed data, rollup, and sessions commands; use api get only when a typed command cannot answer the request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stozo04/google-health-cli) <br>
- [Repository homepage](https://github.com/stozo04/google-health-cli) <br>
- [README](README.md) <br>
- [Agent contract](AGENTS.md) <br>
- [OAuth setup guide](OAUTH_SETUP.md) <br>
- [Google Health API endpoint](https://health.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON on stdout with human-readable notices, counts, and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Data-emitting commands return personal health data; doctor and status commands can return local configuration and account metadata.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
