## Description: <br>
POWPOW 简化版 helps OpenClaw users create and manage POWPOW digital humans, including account registration, digital-human creation, location selection, avatar upload, renewal, and badge management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durenzidu](https://clawhub.ai/user/durenzidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to manage a POWPOW account and complete the interactive flow for creating, viewing, renewing, and locating POWPOW digital humans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles POWPOW account credentials and sends them to the configured POWPOW service. <br>
Mitigation: Use a POWPOW-specific password and verify the configured POWPOW base URL before registering or logging in. <br>
Risk: Avatar uploads and location searches may disclose local file choices, images, or location interests to external services. <br>
Mitigation: Review avatar file paths before upload and treat AMap location search terms as data shared with a third-party map service. <br>
Risk: Logs and feedback files may remain under ~/.powpow-simple on the local machine. <br>
Mitigation: Delete local logs or feedback files if they contain information you do not want retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/durenzidu/powpow-simple) <br>
- [POWPOW website](https://global.powpow.online) <br>
- [POWPOW map](https://global.powpow.online/map) <br>
- [POWPOW Simple npm package](https://www.npmjs.com/package/powpow-simple) <br>
- [AMap geocoding API](https://restapi.amap.com/v3/geocode/geo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Files, Configuration] <br>
**Output Format:** [JSON-like command responses and concise user-facing messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local logs and feedback files under ~/.powpow-simple and send account, avatar, and location data to configured POWPOW and AMap services.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, skill.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
