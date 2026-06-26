## Description: <br>
Oura Health lets an agent query Oura Ring sleep, readiness, activity, heart rate, trends, and health alerts through the Oura API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Oura users and their agents use this skill to check sleep, readiness, activity, recent heart rate, multi-day trends, and daily health alerts from local command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Oura health, profile, and account data that may appear in agent responses, shared chats, or logs. <br>
Mitigation: Use it only in trusted sessions, avoid sharing status or alert output in public channels, and limit command use to data the user intends to disclose. <br>
Risk: The skill depends on a local Oura personal access token and configurable API base URL. <br>
Mitigation: Keep the credentials file private, leave the base URL pointed at the official Oura API unless intentionally testing, and revoke the token if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jarvis563/oura-health) <br>
- [Oura personal access tokens](https://cloud.ouraring.com/personal-access-tokens) <br>
- [Oura API v2 endpoint](https://api.ouraring.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Human-readable text from Python scripts, with setup guidance in Markdown and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Oura personal access token; reads Oura account data and does not write to the account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
