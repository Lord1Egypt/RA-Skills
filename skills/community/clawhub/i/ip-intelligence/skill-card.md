## Description: <br>
Queries IP security intelligence and threat-IP data, including geolocation, risk scores, proxy/VPN/Tor detection, blacklist context, and daily, weekly, monthly, or threat-report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanzx3](https://clawhub.ai/user/yanzx3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, operations teams, and developers use this skill to query IP threat intelligence, inspect high-risk IPs, and draft operational security reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried IPs, threat-intelligence context, and report data to an external API provider. <br>
Mitigation: Install only when the API provider is trusted and the user is allowed to share the relevant security data with that provider. <br>
Risk: The skill requires a sensitive API key. <br>
Mitigation: Store IP_INTELLIGENCE_API_KEY securely, pass it through the documented header, and do not hardcode it in code or configuration files. <br>
Risk: Generated security reports or blocking recommendations may be incomplete or incorrect. <br>
Mitigation: Validate reports and high-risk IP findings before using them for blocking or other operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanzx3/ip-intelligence) <br>
- [IP intelligence API endpoint](https://ai2api.top/api/v1/security/ip-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown reports and structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IP_INTELLIGENCE_API_KEY and may include IP risk scores, threat summaries, tables, and remediation suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
