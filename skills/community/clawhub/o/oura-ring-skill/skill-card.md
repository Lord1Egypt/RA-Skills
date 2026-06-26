## Description: <br>
Fetch Oura Ring readiness/sleep + 7-day readiness trends via Oura Cloud API V2, and generate a Morning Readiness Brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sameerbajaj](https://clawhub.ai/user/sameerbajaj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch Oura readiness, sleep, stress, and resilience data and turn it into JSON, text output, or a morning readiness brief for personal health and recovery planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Oura tokens and health data may be exposed if local .env files or debug probe scripts are mishandled. <br>
Mitigation: Use a least-privilege Oura token, keep .env files private, and avoid running the probe scripts unless they have been reviewed and cleaned for the target environment. <br>
Risk: Documented controls for mock mode and environment-file overrides may not behave as described. <br>
Mitigation: Review the scripts before installation and do not rely on morning_brief.sh mock or env-file override behavior until those controls are fixed and verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sameerbajaj/oura-ring-skill) <br>
- [Oura Cloud API applications](https://cloud.ouraring.com/oauth/applications) <br>
- [Oura API V2 usercollection endpoint](https://api.ouraring.com/v2/usercollection) <br>
- [Oura OAuth token endpoint](https://api.ouraring.com/oauth/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, plain text, and Markdown-style morning brief output with shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Oura API bearer-token configuration from environment variables or a local .env file; mock mode can emit example payloads without network access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
