## Description: <br>
Searches a configured Prowlarr instance for media resources and returns matching torrents, magnet links, and related result details as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhxyz](https://clawhub.ai/user/pengzhxyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to query their own Prowlarr instance for movie, TV, or music resources, including season and episode searches for TV series. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Prowlarr API key to query a configured Prowlarr instance. <br>
Mitigation: Treat PROWLARR_API_KEY as sensitive, avoid exposing it in logs, and rotate it if it may have been disclosed. <br>
Risk: Search requests are sent to the configured PROWLARR_BASE_URL. <br>
Mitigation: Use a trusted local or HTTPS Prowlarr endpoint and avoid routing requests through untrusted proxies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengzhxyz/prowlarr-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions] <br>
**Output Format:** [Markdown usage guidance with JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus PROWLARR_BASE_URL and PROWLARR_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
