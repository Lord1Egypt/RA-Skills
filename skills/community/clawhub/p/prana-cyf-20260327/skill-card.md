## Description: <br>
Provides 24/7 real-time financial news retrieval and display, including support for Jin10 and other financial news sources with second-level WebSocket updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-monitoring users can use this skill to request live financial-news updates from a remote Prana-backed service and present the returned results directly to end users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to a default remote backend unless the base URL is changed. <br>
Mitigation: Use the skill only with a trusted backend and override the base URL when routing to an approved service. <br>
Risk: The client may automatically retrieve API credentials and store reusable credentials in config/api_key.txt. <br>
Mitigation: Set PRANA_SKILL_NO_AUTO_API_KEY=1 and PRANA_SKILL_SKIP_WRITE_API_KEY=1 when tighter credential control is required. <br>
Risk: Remote server responses are passed through directly to the final user. <br>
Mitigation: Review the backend and response-handling policy before deployment, especially where raw financial-news output could affect user decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyffeifeifei/prana-cyf-20260327) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Raw server JSON and text returned from the remote agent-run or agent-result service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The client passes server responses through directly and may poll for asynchronous results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
