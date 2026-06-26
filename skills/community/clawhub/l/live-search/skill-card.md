## Description: <br>
Real-time answers from the public web via the host app's local search gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an assistant needs current web information, such as recent news, prices, scores, rates, weather, or fact checks after the model's knowledge cutoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may contain sensitive or confidential information sent through the host app's search gateway. <br>
Mitigation: Keep queries concise and do not include secrets, credentials, or confidential data. <br>
Risk: Live web results can be incomplete, outdated, or misleading for important decisions. <br>
Mitigation: Verify important results at the linked sources before relying on them. <br>


## Reference(s): <br>
- [Live Search on ClawHub](https://clawhub.ai/codenova58/live-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and verbatim search result blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies the search API message field verbatim before any optional grounded summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
