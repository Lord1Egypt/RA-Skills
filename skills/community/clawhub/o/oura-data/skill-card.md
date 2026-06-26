## Description: <br>
Fetches a user's personal Oura Ring sleep, readiness, activity, heart rate, workout, SpO2, stress, ring, and profile data through the official Oura API v2 using the local oura-cli tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqchris](https://clawhub.ai/user/zqchris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Oura Rings use this skill to query personal biometric history and ground sleep, recovery, activity, and wellness guidance in live Oura API results. It is useful for date-specific checks, trend comparisons, and setup guidance for the local helper CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Oura health and profile data through OAuth-authorized local commands. <br>
Mitigation: Grant only needed Oura scopes where possible, avoid the personal endpoint unless necessary, keep token and configuration files private, and treat chats containing Oura results as private. <br>
Risk: The skill depends on an external local helper CLI to retrieve Oura data. <br>
Mitigation: Review or pin the helper CLI before running it and keep execution local to the authorized machine. <br>
Risk: Wellness recommendations based on biometric signals could be mistaken for medical advice. <br>
Mitigation: Use the skill to report Oura data and trends, avoid diagnosis, and direct users to a clinician for medical questions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zqchris/oura-data) <br>
- [Oura API v2 docs](https://cloud.ouraring.com/v2/docs) <br>
- [oura-cli companion tool](https://github.com/zqchris/oura-cli) <br>
- [Oura API v2 Reference](references/api-reference.md) <br>
- [Example Outputs](references/example-outputs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and API-derived text or JSON summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local uv and an OAuth-authorized oura-cli checkout; may process sensitive health and profile data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
