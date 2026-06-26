## Description: <br>
Poc Validator replays supplied HTTP requests or payloads and analyzes response status codes and error snippets to help validate specific vulnerability proof-of-concept claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatyourname12345](https://clawhub.ai/user/whatyourname12345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and developers use this skill to replay a specific authorized HTTP request or payload and summarize whether the response contains evidence of a vulnerability such as SQL error-based injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replay vulnerability payloads against live HTTP endpoints. <br>
Mitigation: Use it only for systems where the operator has explicit authorization and avoid mass scanning or denial-of-service patterns. <br>
Risk: Raw requests may include Cookie, Authorization, API keys, CSRF tokens, or private body fields. <br>
Mitigation: Strip sensitive values before replay unless using controlled test credentials. <br>
Risk: HTTPS certificate validation is disabled by default in the replay helper. <br>
Mitigation: Review the target and network path before use, and prefer enabling certificate validation when testing systems with valid certificates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whatyourname12345/openclaw-poc-validator) <br>
- [Publisher profile](https://clawhub.ai/user/whatyourname12345) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown report with command guidance, HTTP response details, and selected evidence snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The replay helper emits JSON containing status code, response headers, and a response body snippet for agent analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
