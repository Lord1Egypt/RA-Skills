## Description: <br>
Query the public MyIPChecker IP information API and summarize geolocation and network metadata for a specific IPv4 address or the caller IP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanzhengyang](https://clawhub.ai/user/tanzhengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run live IP metadata lookups, inspect caller-IP information, and explain or troubleshoot MyIPChecker JSON responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live lookups send supplied IP addresses to MyIPChecker, and caller-IP lookups disclose the runtime public IP to the service. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and avoid sending sensitive or unnecessary IP addresses. <br>
Risk: The helper supports a custom base URL, which could send lookup data to an alternate endpoint. <br>
Mitigation: Use the default MyIPChecker endpoint unless the alternate service is intentionally trusted. <br>
Risk: The upstream service can return HTTP errors, empty bodies, or non-JSON responses instead of successful lookup data. <br>
Mitigation: Treat transport and HTTP failures as lookup failures and avoid relying on incomplete responses. <br>


## Reference(s): <br>
- [MyIPChecker API Reference](references/myipchecker-api.md) <br>
- [MyIPChecker IP API](https://myipchecker.ai/api/ip) <br>
- [ClawHub skill page](https://clawhub.ai/tanzhengyang/my-ip-checker-iplookup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands or raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make live unauthenticated HTTPS requests to MyIPChecker and return upstream transport or HTTP error details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
