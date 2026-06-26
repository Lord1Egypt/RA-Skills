## Description: <br>
Httpstat provides readable HTTP response timing statistics with DNS, TCP, TLS, TTFB, transfer, header, redirect, and optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check URL response times, debug slow HTTP requests, measure TTFB, inspect redirect behavior, and capture readable timing breakdowns from live HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live HTTP requests can expose URLs, headers, request bodies, responses, and local command output to the target service or local observers. <br>
Mitigation: Use placeholder tokens in examples, avoid real secrets or private payloads unless the destination is trusted, and review command output before sharing it. <br>
Risk: The skill intentionally makes network requests for timing and debugging, which may contact external hosts from the agent environment. <br>
Mitigation: Confirm the intended URL and request method before execution, and limit use to endpoints the user is authorized to test. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce timing waterfalls, HTTP status details, selected response headers, TLS details, body size, redirect traces, and exit-code guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
