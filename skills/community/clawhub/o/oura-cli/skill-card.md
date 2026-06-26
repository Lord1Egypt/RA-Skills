## Description: <br>
Retrieve health and biometric data from an Oura Ring account through CLI commands for sleep, activity, readiness, heart rate, workouts, stress, resilience, and related data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Supadoopa](https://clawhub.ai/user/Supadoopa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents with an active Oura account use this skill to authenticate with Oura, run targeted CLI queries, and summarize returned health and biometric JSON data in natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Oura health and profile data and stores OAuth credentials locally. <br>
Mitigation: Install only from a trusted source, use it on a single-user machine, keep ~/.config/oura-cli/config.json out of synced or shared locations, restrict the file to user-only access, and revoke the Oura token when the tool is no longer used. <br>
Risk: The OAuth scopes grant broad access to Oura health and account data. <br>
Mitigation: Authorize only an Oura application you control and review the requested scopes before completing authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Supadoopa/oura-cli) <br>
- [Oura Cloud Developer Portal](https://cloud.ouraring.com/oauth/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON responses for agent summarization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated Oura OAuth credentials and date arguments in YYYY-MM-DD format for most time-series queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
