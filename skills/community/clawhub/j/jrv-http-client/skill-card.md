## Description: <br>
Make HTTP requests from the command line with support for auth (Bearer, Basic, API key), custom headers, JSON/form body, response formatting, timing, and history logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to make HTTP requests for API testing, health checks, authentication testing, webhook debugging, and CI automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials supplied through Bearer, Basic, or API key options can be exposed to unintended endpoints when redirects are followed. <br>
Mitigation: Avoid real tokens or passwords with URLs that may redirect, and inspect redirect behavior before using authenticated requests. <br>
Risk: The --no-verify option disables TLS certificate verification and can make HTTPS requests vulnerable to interception. <br>
Mitigation: Use --no-verify only in controlled testing environments and keep certificate verification enabled for normal use. <br>
Risk: Mutating HTTP methods can perform remote actions with the full privileges of the supplied credentials. <br>
Mitigation: Review target URLs, methods, headers, and request bodies before running POST, PUT, PATCH, or DELETE requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/jrv-http-client) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API responses, Text, JSON, Files] <br>
**Output Format:** [Command-line text, optional JSON response envelopes, HTTP status codes, and optional response body files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish successful HTTP responses, HTTP errors, and network or usage errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
