## Description: <br>
Fetch and report Peloton cycling workout statistics, including recent ride counts, duration, calories, output, power, resistance, cadence, and instructor data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niemesrw](https://clawhub.ai/user/niemesrw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve a weekly Peloton cycling workout summary for a user account. It is useful when the user asks for recent Peloton ride history, training totals, or cycling performance metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Peloton account credentials. <br>
Mitigation: Use the OpenClaw credential flow, protect the auth profile and environment variables, and rotate the Peloton password if the environment is later shared or untrusted. <br>
Risk: Recent workout stats may be printed into the agent conversation. <br>
Mitigation: Run the skill only in contexts where sharing Peloton workout history and performance metrics is acceptable. <br>


## Reference(s): <br>
- [Peloton Stats ClawHub page](https://clawhub.ai/niemesrw/peloton-stats) <br>
- [Peloton API endpoint](https://api.onepeloton.com) <br>
- [Peloton OAuth token endpoint](https://auth.onepeloton.com/oauth/token) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with summary metrics and a recent rides table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Looks back 7 days, reports cycling workouts only, and requires Peloton credentials from OpenClaw auth profile or PELOTON_USERNAME and PELOTON_PASSWORD.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
