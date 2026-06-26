## Description: <br>
Use CallMyCall API to start, end, and check AI phone calls, and return results in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenjaminWaye](https://clawhub.ai/user/BenjaminWaye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to operate CallMyCall from chat: preparing outbound call briefs, placing or ending calls after confirmation, checking recent call status, and retrieving results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place and end real phone calls through a user's CallMyCall account, and its repeated-calling workflow needs explicit operational limits. <br>
Mitigation: Require human confirmation before placing calls, use a limited API key where possible, verify the API endpoint, and set maximum attempts and intervals for retry-until-answered requests. <br>
Risk: Call briefs, transcripts, and recording URLs may contain sensitive information. <br>
Mitigation: Avoid unnecessary sensitive details in call briefs, show transcript excerpts only when explicitly requested, and warn users before sharing recording URLs. <br>
Risk: API keys could be exposed or persisted unintentionally if handled outside the documented flow. <br>
Mitigation: Resolve keys from the environment, user config, or a one-time prompt; never echo keys; do not write config automatically; and do not store keys in call state. <br>


## Reference(s): <br>
- [CallMyCall API Reference](references/api.md) <br>
- [Auth and Config](docs/auth-config.md) <br>
- [Event Updates for Pull-Based CallMyCall](docs/event-updates.md) <br>
- [CallMyCall API homepage](https://api.callmycall.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API call results, Configuration guidance] <br>
**Output Format:** [Markdown chat responses with call IDs, statuses, summaries, transcript excerpts, recording links, and configuration instructions when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a recent-calls state list for in-session follow-up and fetches transcripts or recordings only when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
