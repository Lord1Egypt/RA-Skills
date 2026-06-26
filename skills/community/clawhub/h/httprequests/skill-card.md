## Description: <br>
Sends GET, POST, PUT, and DELETE HTTP requests with Python requests when curl quoting or escaping would be error-prone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pumpkinttl](https://clawhub.ai/user/pumpkinttl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make API calls, test webhooks, and inspect HTTP responses without hand-crafting fragile curl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send requests to arbitrary URLs and supports mutating HTTP methods. <br>
Mitigation: Double-check destination URLs, methods, headers, and bodies before execution, especially for POST, PUT, and DELETE requests. <br>
Risk: Secrets can be exposed if placed in query strings, inline examples, or local request summaries. <br>
Mitigation: Use least-privilege tokens, avoid secrets in URLs or shared command examples, and use --no-log for sensitive requests. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/pumpkinttl/httprequests) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output with HTTP method, final URL, status, elapsed time, optional headers, and response body.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Response bodies can be truncated with --max-body; daily JSONL request summaries are written unless --no-log is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
