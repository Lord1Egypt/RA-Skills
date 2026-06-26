## Description: <br>
Fetch and summarize Oura Ring v2 sleep, readiness, and activity data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silas-agent573](https://clawhub.ai/user/silas-agent573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch Oura Ring v2 sleep, readiness, activity, HRV, temperature, and recovery metrics, then turn them into a concise daily health briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Oura API token and returns health metrics that may be sensitive. <br>
Mitigation: Store OURA_API_TOKEN in a protected environment or secret manager, avoid sharing raw outputs in logs or transcripts, and revoke the token when access is no longer needed. <br>
Risk: Passing --token on the command line can expose the token through shell history or process listings. <br>
Mitigation: Prefer OURA_API_TOKEN over --token and avoid pasting tokens into shared agent sessions. <br>


## Reference(s): <br>
- [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens) <br>
- [Oura API v2 user collection endpoint](https://api.ouraring.com/v2/usercollection) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain-text briefing or JSON from a shell script, with agent guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an Oura API token supplied through OURA_API_TOKEN or --token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
