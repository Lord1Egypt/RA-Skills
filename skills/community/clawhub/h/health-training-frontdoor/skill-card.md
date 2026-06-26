## Description: <br>
Narrow first-class front door for live Fitbit/training retrieval via stable JSON actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaodriessen](https://clawhub.ai/user/joaodriessen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting a user's health and training workflow use this skill to retrieve recent Fitbit recovery, sleep, quality, and training-window data through stable read-only JSON actions. The skill also directs programming advice back to the user's training references before recommendations are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive health, sleep, recovery, and training data to the agent. <br>
Mitigation: Install only when the agent is intended to access this data, and handle returned data as sensitive user information. <br>
Risk: The skill depends on a local Fitbit connector and training context that may be misconfigured or untrusted. <br>
Mitigation: Verify the local connector, authentication state, and referenced training context before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joaodriessen/health-training-frontdoor) <br>
- [Practical Programming reading guide](reference/practical-programming/INDEX.md) <br>
- [Training continuity context](memory/training-continuity.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Compact JSON responses with Markdown usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only actions; optional fields include days, ensureFresh, and source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
