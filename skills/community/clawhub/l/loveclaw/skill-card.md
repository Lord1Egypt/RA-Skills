## Description: <br>
LoveClaw provides conversational dating registration, same-city Bazi-based matching, optional photo handling, daily matching, and evening match reports through a cloud backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackysly88](https://clawhub.ai/user/jackysly88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to register for matchmaking through chat, manage profile and notification preferences, and receive daily match reports. OpenClaw workspace operators install it with the required token and scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive dating data, photos, birth details, city, preferences, match results, and contact details. <br>
Mitigation: Install only if the LoveClaw backend is trusted and users accept sharing this data with that backend. <br>
Risk: Workspace secrets and local session data may affect the skill's runtime behavior. <br>
Mitigation: Use a dedicated OpenClaw workspace and keep only LoveClaw-related secrets in the workspace .env. <br>
Risk: Photo handling can involve local files or URLs. <br>
Mitigation: Do not paste local file paths as photos; prefer normal channel photo upload flows. <br>
Risk: Persistent scheduled jobs can continue sending match reports after setup. <br>
Mitigation: Verify how to remove LoveClaw cron jobs and local session files when canceling registration or disabling push notifications. <br>


## Reference(s): <br>
- [LoveClaw ClawHub Page](https://clawhub.ai/jackysly88/loveclaw) <br>
- [LoveClaw README](artifact/README.md) <br>
- [LoveClaw Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text chat replies, JSON delivery payloads for scheduled reports, and cron configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and LOVECLAW_API_TOKEN; optional LOVECLAW_API_BASE and OPENCLAW_BIN can alter backend or CLI routing.] <br>

## Skill Version(s): <br>
21.21.21 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
