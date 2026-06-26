## Description: <br>
Query Millimetric analytics for top sources, aggregate stats, raw events, and Facebook social-vs-paid splits from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soybelli](https://clawhub.ai/user/soybelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analytics users use this skill to assemble read-only Millimetric API queries for traffic sources, aggregate metrics, raw event debugging, and paid-versus-organic attribution checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Millimetric read key, and exposing that key in shared prompts, shell history, or logs could grant access to analytics data. <br>
Mitigation: Use a least-privilege read-only rk_live key, avoid echoing it in shared logs, and rotate the key if it is exposed. <br>
Risk: Raw event queries can expose privacy-sensitive user or anonymous activity. <br>
Mitigation: Prefer aggregate queries when possible and query raw user or anonymous IDs only for authorized debugging or support work. <br>


## Reference(s): <br>
- [Millimetric API homepage](https://api.millimetric.ai) <br>
- [ClawHub skill page](https://clawhub.ai/soybelli/millimetric-query) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MILLIMETRIC_RK plus curl and jq; Millimetric API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
